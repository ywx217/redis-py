from __future__ import with_statement
import binascii
import datetime
import time
import os
import sys
os.environ['REDIS_GEVENT'] = 'true'
sys.path.append(os.path.abspath('../'))
import redis
from redis._compat import (unichr, u, b)


class Stat(object):
    def __init__(self):
        self.finish_count = 0


def test_get_and_set(stat, r):
    # get and set can't be tested independently of each other
    byte_string = b('value')
    integer = 5
    unicode_string = unichr(3456) + u('abcd') + unichr(3421)
    assert r.set('byte_string', byte_string)
    assert r.set('integer', 5)
    assert r.set('unicode_string', unicode_string)
    assert r.get('byte_string') == byte_string
    assert r.get('integer') == b(str(integer))
    assert r.get('unicode_string').decode('utf-8') == unicode_string
    stat.finish_count += 1


def test_main(count):
    import gevent
    import gevent.queue
    import redis.socket_patch

    if redis.socket_patch.USE_GEVENT:
        connection_pool = redis.BlockingConnectionPool(
            max_connections=50,
            queue_class=gevent.queue.Queue,
            host='192.168.46.126', port=6379, db=9
        )
    else:
        connection_pool = redis.BlockingConnectionPool(
            max_connections=50,
            host='192.168.46.126', port=6379, db=9
        )
    client = redis.StrictRedis(connection_pool=connection_pool)

    stat = Stat()
    f = lambda i: gevent.spawn(lambda: test_get_and_set(stat, client))
    begin = time.time()
    crs = map(f, xrange(count))
    gevent.joinall(crs)
    print '%d 3get-3set-case used %.2fms' % (count, (time.time() - begin) * 1000)


if __name__ == '__main__':
    test_main(1000)
