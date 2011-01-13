def install_hg(sources):
    """
    - sources : dict of hg sources to install: {'package': 'http://hg...'}
    """
    try:
        from subprocess import check_call as call
    except:
        from subprocess import call

    # see if you can find site-packages
    import site
    site_dir = os.path.abspath(os.path.dirname(site.__file__))
    site_packages = os.path.join(site_dir, 'site-packages')
    if not (os.path.exists(site_packages) and os.path.isdir(site_packages)):
        raise IOError("Cannot find site-packages directory")

    # figure out what you need to install
    missing = set()
    for source in sources:
        try:
            __import__(source)
        except ImportError:
            missing.add(source)

    # install it
    for source in missing:
        call(['hg', 'clone', sources[source],
              os.path.join(site_packages, source)])

### install unpackaged dependencies
if set(['install', 'develop']).intersection(sys.argv[1:]):
    try:
        install_hg(source)
    except:
        print 'Please make sure the source is installed:'
        print source
