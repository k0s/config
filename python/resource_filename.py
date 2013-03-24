#!/usr/bin/env python

# example code

import os

def resource_path(path):
    """
    getting a resource filename (absolute path)
    - path: relative path
    """

    try:
        # use pkg_resources if available
        # http://pythonhosted.org/distribute/setuptools.html#non-package-data-files
        from pkg_resources import Requirement, resource_filename
        return resource_filename(Requirement.parse("MyProject"),path)
    except ImportError:
        # assume file lives relative to this file
        here = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(here, path)
