from prometheus_client import make_wsgi_app, Gauge
from wsgiref.simple_server import make_server
from redis.sentinel import Sentinel
import redis,sys,os

APP_HOSTNAME = os.getenv('APP_HOSTNAME', '127.0.0.1')
APP_PORT = os.getenv('APP_PORT', 9000)
REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME', '127.0.0.1')
REDIS_PORT = os.getenv('PORT', 6379)
REDIS_PASS = os.getenv('REDIS_PASS', 'none')
ENV = os.getenv('ENV', 'local')
QLIST = os.getenv('QLIST').split(' ')
SENTINEL_HOST = os.getenv('SENTINEL_HOST', 'none')
SENTINEL_REDIS_NAME = os.getenv('SENTINEL_REDIS_NAME', 'none')                            
SENTINEL_PORT = os.getenv('SENTINEL_PORT', 26379)
SENTINEL_REDIS_PASSWORD = os.getenv('SENTINEL_REDIS_PASSWORD', 'none')

if QLIST is None:
    sys.exit('Please set env: QLIST')

g = Gauge('redis_queue_length', 'Length of queues', ['env','queue_name'])

def get_metrics():
    if SENTINEL_HOST == 'none':
        r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, password=REDIS_PASS)
    else:
        hosts = [SENTINEL_HOST]
        sentinel = Sentinel([(h, SENTINEL_port) for h in hosts], socket_timeout=0.1)
        r = sentinel.master_for(SENTINEL_REDIS_NAME, password=SENTINEL_REDIS_PASSWORD)
    try:
        r.ping()
    except redis.ConnectionError:
        print("Cannot make connection to redis")
        pass
    for q in QLIST:
        qlen = r.llen(q)
        g.labels(ENV,q).set(qlen)

metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        get_metrics()
        return metrics_app(environ, start_fn)

httpd = make_server(APP_HOSTNAME, APP_PORT, my_app)
httpd.serve_forever()
