# -*- coding: UTF-8 -*-
import requests
import shutil
import logging

log = logging.getLogger(__name__)


def log_scope(log):
    def outer_d_f(f):
        def d_f(*args, **kargs):
            kn = f.__name__
            log.info("*** %s() is entering ..." % (kn))
            if args:
                log.info("args: {}".format(args))
            if kargs:
                log.info("kargs: {}".format(kargs))
            r = f(*args, **kargs)
            log.info("*** %s() is leaving ..." % (kn))
            return r
        d_f.__doc__ = f.__doc__
        return d_f
    return outer_d_f


def download(path, url):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        log.error(e)
