# redis_queue_length_exporter

Requires global variables:

* QLIST = "queue1 queue2 queue3 ..."

Optional global variables:

* APP_HOSTNAME: (default: 127.0.0.1)
* APP_PORT: (default: 9000)
* REDIS_HOSTNAME = (default: 127.0.0.1)
* REDIS_PORT = (default: 6379)
* REDIS_PASS = (default: none)
* ENV = (default: local)

* SENTINEL_HOST (default: none)
* SENTINEL_REDIS_NAME (default: none)
* SENTINEL_PORT (default: 26379)
* SENTINEL_REDIS_PASSWORD (default: none)

