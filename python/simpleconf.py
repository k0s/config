def simpleconf(filename, sep='='):
    assert os.path.exists(filename)
    lines = [line.strip() for line in file(filename).readlines()]
    lines = [line for line in lines if line and not line.startswith('#')]
    assert not [line for line in lines if sep not in line]
    return dict([line.split(sep, 1) for line in lines])
