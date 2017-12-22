import os
if os.getenv('REDIS_GEVENT', '').lower() == 'true':
    USE_GEVENT = True
else:
    USE_GEVENT = False


if USE_GEVENT:
    from gevent.socket import *
else:
    from socket import *
