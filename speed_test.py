import timeit


def ctime(method):
    def timed(*args, **kw):
        ts = timeit.default_timer()
        result = method(*args, **kw)
        te = timeit.default_timer()

        print('%r (%r, %r) %.4f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed