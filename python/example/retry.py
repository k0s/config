def retry(f, retries=5, args=(), kw=None, exceptions=()):

    kw = kw or {}
    for index in range(retries):
        try:
            return f(*args, **kw)
        except Exception as e:
            if isinstance(e, exceptions):
                print ("something bad happen")
            else:
                raise
    raise RetryTimeout("Tries a bunch of times :(")