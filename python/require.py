def require(url):
    """
    import a module from the web
    url should be like scheme://host.name/path/to/module.py
    """
    import imp
    import os
    import tempfile
    import urllib2
    contents = urllib2.urlopen(url).read()
    filename = url.rsplit('/', 1)[-1]
    module = filename.rsplit('.', 1)[0]
    dest = tempfile.mkstemp(suffix='.py', prefix=module)
    f = file(dest, 'w')
    f.write(contents)
    f.close()
    return imp.load_source(module, dest)

# TODO: make an equivalent method for a tarball
