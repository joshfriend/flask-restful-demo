#!/bin/bash

# Gunicorn settings
# http://gunicorn-docs.readthedocs.org/en/latest/settings.html

# Heroku router timeout is 30 sec
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-30}

## Concurrency Settings
# The number of worker processes for handling requests.
WEB_CONCURRENCY=${WEB_CONCURRENCY:-3}
# The maximum number of pending connections.
GUNIDORN_BACKLOG=${GUNICORN_BACKLOG:-2048}
# The maximum number of requests a worker will process before restarting.
GUNICORN_WORKER_CONNECTIONS=${GUNICORN_WORKER_CONNECTIONS:-2000}
# The type of workers to use.
# Valid options are:
#   sync, gevent, eventlet, tornado
# Python 3 may also use:
#   gthread, gaiohttp
# http://gunicorn-docs.readthedocs.org/en/latest/design.html#server-model
GUNICORN_WORKER_CLASS=${GUNICORN_WORKER_CLASS:-sync}
# Run each worker with the specified number of threads.
# Only valid for sync worker types
GUNICORN_WORKER_THREADS=${GUNICORN_WORKER_THREADS:-1}

# The maximum number of requests a worker will process before restarting.
GUNICORN_MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-0}
# The maximum jitter to add to the max_requests setting.
GUNICORN_MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-0}

## Debug settings
# Restart workers when code changes.
if [ "$GUNICORN_RELOAD" ]; then
    EXTRA_ARGS="--reload"
fi
# Load application code before the worker processes are forked.
if [ "$GUNICORN_PRELOAD" ]; then
    EXTRA_ARGS="$EXTRA_ARGS --reload"
fi
GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}

gunicorn demo:create_app\(\)                            \
    --log-level $GUNICORN_LOG_LEVEL                     \
    --bind 0.0.0.0:$PORT                                \
    --workers $WEB_CONCURRENCY                          \
    --threads $GUNICORN_WORKER_THREADS                  \
    --timeout $GUNICORN_TIMEOUT                         \
    --worker-class $GUNICORN_WORKER_CLASS               \
    --worker-connections $GUNICORN_WORKER_CONNECTIONS   \
    --max-requests $GUNICORN_MAX_REQUESTS               \
    --max-requests-jitter $GUNICORN_MAX_REQUESTS_JITTER \
    $EXTRA_ARGS
