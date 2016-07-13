#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
monitor custom endpoints form a JSON file
"""

# imports
import argparse
import json
import os
import requests
import statuspage
import sys
import time

# What we want but I'm not sure if it works in python 2.6
# http://stackoverflow.com/questions/6921699/can-i-get-json-to-load-into-an-ordereddict-in-python


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',
                        type=argparse.FileType('r'),
                        help="input JSON file")
    parser.add_argument('--customer', dest='customer', nargs='+',
                        help="customer to act on")
    parser.add_argument('--list-customers', dest='list_customers',
                        action='store_true', default=False,
                        help="list customers and return")
    parser.add_argument('--list-endpoints', dest='list_endpoints',
                        action='store_true', default=False,
                        help="list endpoints and exit")
    parser.add_argument('--failures', dest='output_failures',
                        action='store_true', default=False,
                        help="output failures only")
    parser.add_argument('--successes', dest='output_successes',
                        action='store_true', default=False,
                        help="output successes only")
    parser.add_argument('--timeout', dest='timeout',
                        type=float, default=60,
                        help="request timeout in seconds [DEFAULT: %(default)s]")
    parser.add_argument('--verify', dest='verify',
                        action='store_true', default=False,
                        help="verify HTTPS requests")
    parser.add_argument('--statuspage', '--statuspage-io', dest='statuspage_io',
                        nargs=2, metavar=('PAGE_ID', 'API_KEY'),
                        help="post status to statuspage.io")
    options = parser.parse_args(args)

    # sanity
    if options.output_failures and options.output_successes:
        parser.error("Cannot use both --failures and --successes")

    if not options.verify:
        # disable insecure warnings:
        # http://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
        requests.packages.urllib3.disable_warnings()

    # load input file JSON
    data = json.load(options.input)

    # check for conformity
    message = "Expected a dict with a list of URLs"
    if not isinstance(data, dict):
        parser.error(message)
    if not all([isinstance(value, list)
                for value in data.values()]):
        parser.error(message)

    if options.list_customers:
        # list customers and exit
        print (json.dumps(sorted(data.keys()),
                          indent=2))
        return

    if options.customer:
        # choose data only for subset of customers
        missing = [customer for customer in options.customer
                   if customer not in data]
        if missing:
            parser.error("Customers not found: {0}".format(', '.join(missing)))
        data = dict([(customer, data[customer])
                     for customer in options.customer])

    if options.list_endpoints:
        # list all endpoints and exit
        print (json.dumps(sorted(sum(data.values(), [])), indent=2))
        return

    # hit endpoints
    results = {}
    for customer, endpoints in data.items():
        results[customer] = []
        for endpoint in endpoints:
            data = {'url': endpoint, 'success': False}
            try:
                start = time.time()
                response = requests.get(endpoint,
                                        verify=options.verify,
                                        timeout=options.timeout)
                end = time.time()
                data['status_code'] = response.status_code
                data['reason'] = response.reason
                response.raise_for_status()
                data['success'] = True
            except requests.HTTPError as e:
                end = time.time()
                pass  # we already have the data we need
            except requests.exceptions.SSLError as e:
                end = time.time()
                data['reason'] = "SSL Error: {0}".format(e)
            except (requests.ConnectionError, requests.Timeout) as e:
                # despite what it says at
                # http://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
                # both `requests.Timeout` and `requests.ConnectionError` seem to fall to this point
                # so we descriminate for either
                end = time.time()

                try:
                    args = e.args[0].reason.args
                    if len(args) == 2:
                        message = args[-1]
                    elif len(args) == 1:
                        message = args[0].split(':', 1)[-1]
                except AttributeError:
                    # Protocol error
                    message = "{0} {1}".format(e.args[0].args[0],
                                               e.args[0].args[-1].args[-1])
                data['reason'] = message
            data['duration'] = end - start
            results[customer].append(data)

    # obtain successes + failures
    failures = {}
    successes = {}
    for customer, result in results.items():
        for item in result:
            append_to = successes if item['success'] else failures
            append_to.setdefault(customer, []).append(item)

    # serialize results
    if options.statuspage_io:
        api = statuspage.StatuspageIO(*options.statuspage_io)

        # get existing components
        components = api.components()

        # figure out what components we need to make
        # we use the customer name as a key so we will go from there
        name_map = dict([(component['name'], component)
                       for component in components])
        id_map = {}
        for customer, data in results.items():

            for item in data:
                name = item['url']
                if 'code' in item:
                    description = "{code} {reason}".format(**item)
                else:
                    description = item['reason']
                endpoint_component = name_map.get(name)
                if endpoint_component is None:
                    try:
                        endpoint_component = api.create_component(name, description)
                    except Exception as e:
                        import pdb; pdb.set_trace()

                # determine status
                if item['success']:
                    status = "operational"
                else:
                    status = "operational" # TODO: you could be better
                api.update_component(endpoint_component['id'],
                                     description=description,
                                     status=status)
    else:
        if options.output_failures:
            output_data = failures
        elif options.output_successes:
            output_data = successes
        else:
            output_data = results
        print (json.dumps(output_data, sort_keys=True, indent=2))

    # exit with appropriate code
    sys.exit(1 if failures else 0)

if __name__ == '__main__':
    main()
