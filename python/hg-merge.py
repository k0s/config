#!/usr/bin/env python

"""
merge mercurial repositories

Example:
hg-merge.py --master http://hg.mozilla.org/build/talos http://hg.mozilla.org/build/pageloader#talos/pageloader
"""

import optparse
import os
import shutil
import subprocess
import sys
import tempfile
import urlparse
try:
    from subprocess import check_call as call
except:
    from subprocess import call

def url2filename(url):
    """gets a filename from a url"""
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    path = path.rstrip('/')
    assert path and '/' in path
    return path.split('/')[-1]

def manifest(hgrepo):
    """manifest of a local hg repository"""
    process = subprocess.Popen(['hg', 'manifest'], cwd=hgrepo, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert not process.returncode
    manifest = stdout.strip().splitlines()
    return set(manifest)

def merge(hgroot, repo, subpath=None):
    """merge repo to hgroot at subpath (None for repository root)"""

    # get a manifest of the current repository
    root_manifest = manifest(hgroot)
    toplevel_contents = os.listdir(hgroot)

    # staging area
    tempdir = tempfile.mkdtemp()
    fd, tmpfile = tempfile.mkstemp()
    os.close(fd)

    exception = None
    try:

        # clone the repository to be merged in
        call(['hg', 'clone', repo, tempdir])

        # check manifest for conflicts
        repo_manifest = manifest(tempdir)
        assert repo_manifest, "Empty repository: %s" % repo
        intersection = root_manifest.intersection(repo_manifest)
        assert not intersection, "Overlap between %s and %s: %s" % (hgroot, repo, intersection)

        # create a bundle
        call(['hg', 'bundle', tmpfile, '--all'], cwd=tempdir)

        # apply the bundle
        call(['hg', 'unbundle', tmpfile], cwd=hgroot)
        call(['hg', 'merge'], cwd=hgroot)

        if subpath:
            # move the new files to their new locations
            for item in repo_manifest:
                path = os.path.join(subpath, item)
                fullpath = os.path.join(hgroot, path)
                assert not os.path.exists(fullpath), "%s already exists" % fullpath
                subdirectory = os.path.dirname(fullpath)
                if not os.path.exists(subdirectory):
                    os.makedirs(subdirectory)
                call(['hg', 'mv', item, path], cwd=hgroot)
            call(['hg', 'commit', '-m', 'merge %s to %s' % (repo, subpath)], cwd=hgroot)
        else:
            call(['hg', 'commit', '-m', 'merge in %s' % repo], cwd=hgroot)

    except Exception, exception:
        pass # reraise on cleanup

    # cleanup
    shutil.rmtree(tempdir)
    os.remove(tmpfile)
    if exception is not None:
        raise exception

def main(args=sys.argv[1:]):

    # parse command line options
    usage = "%prog [options] http://hg.example.com/repository/path#destination/path [...]"
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option('-m', '--master', dest='master',
                      help="use this as the master repository (new clone, otherwise use CWD)")
    options, args = parser.parse_args(args)
    if not args:
        parser.print_help()
        parser.exit()

    if options.master:
        # clone the new repository
        directory = url2filename(options.master)
        if os.path.exists(directory):
            shutil.rmtree(directory)
        call(['hg', 'clone', options.master])
        hgroot = os.path.join(os.getcwd(), directory)
    else:
        # get the root of the repository
        process = subprocess.Popen(['hg', 'root'], stdout=subprocess.PIPE)
        hgroot, stderr = process.communicate()
        hgroot = hgroot.strip()
        if process.returncode:
            sys.exit(1)
    assert os.path.exists(hgroot) and os.path.isdir(hgroot), "%s not found" % hgroot

    # get the other repos to add
    for repo in args:
        subpath = None
        if '#' in repo:
            repo, subpath = repo.rsplit('#', 1)
        merge(hgroot, repo, subpath)

if __name__ == '__main__':
    main()
