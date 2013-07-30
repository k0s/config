def load(resource):
    """
    open a file or URL for reading.  If the passed resource string is not a URL,
    or begins with 'file://', return a ``file``.  Otherwise, return the
    result of urllib2.urlopen()
    """

    # handle file URLs separately due to python stdlib limitations
    if resource.startswith('file://'):
        resource = resource[len('file://'):]

    if not is_url(resource):
        # if no scheme is given, it is a file path
        return file(resource)

    return urllib2.urlopen(resource)