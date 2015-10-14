#!/usr/bin/env python

import os

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#

bind = '0.0.0.0:%i' % int(os.getenv('PORT', 5000))
backlog = int(os.getenv('GUNICORN_BACKLOG', 2048))

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       async class should handle most 'normal' types of work
#       loads. You'll want to read http://gunicorn/deployment.hml
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       An string referring to a 'gunicorn.workers' entry point
#       or a python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       are:
#
#           egg:gunicorn#sync
#           egg:gunicorn#eventlet   - Requires eventlet >= 0.9.7
#           egg:gunicorn#gevent     - Requires gevent >= 0.12.2 (?)
#           egg:gunicorn#tornado    - Requires tornado >= 0.2
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   max_requests - The maximum number of requests a worker will process
#       before restarting.
#
#       Any value greater than zero will limit the number of requests
#       a work will process before automatically restarting. This is
#       a simple method to help limit the damage of memory leaks.
#
#       If this is set to zero (the default) then the automatic
#       worker restarts are disabled.
#
#   max_requests_jitter - The maximum jitter to add to the max-requests
#       setting.
#
#       The jitter causes the restart per worker to be randomized
#       by randint(0, max_requests_jitter). This is intended to
#       stagger worker restarts to avoid all workers restarting
#       at the same time.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#   graceful_timeout - Timeout for graceful workers restart.
#
#       Generally set to thirty seconds. How max time worker can handle
#       request after got restart signal. If the time is up worker will
#       be force killed.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#
#   threads - The number of worker threads for handling requests.
#
#       Run each worker with the specified number of threads.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES) range.
#       You'll want to vary this a bit to find the best for your
#       particular application's work load.

workers = int(os.getenv('WEB_CONCURRENCY', 3))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', 2000))
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 0))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 0))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))
graceful_timeout = int(os.getenv('GUNICORN_GRACEFUL_TIMEOUT', 0))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 2))
threads = int(os.getenv('GUNICORN_THREADS', 1))

#
# Debugging
#
#   reload - Restart workers when code changes.
#
#       This setting is intended for development. It will cause workers to be
#       restarted whenever application code changes.
#
#       The reloader is incompatible with application preloading. When using a
#       paste configuration be sure that the server block does not import any
#       application code or the reload will not work as designed.
#
#   spew - Install a trace function that spews every line of Python
#       that is executed when running the server. This is the
#       nuclear option.
#
#       True or False
#

reload = bool(os.getenv('GUNICORN_RELOAD', False))
spew = False

#
# Server mechanics
#
#   daemon - Detach the main Gunicorn process from the controlling
#       terminal with a standard fork/fork sequence.
#
#       True or False
#
#   pidfile - The path to a pid file to write
#
#       A path string or None to not write a pid file.
#
#   user - Switch worker processes to run as this user.
#
#       A valid user id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getpwnam(value) or None
#       to not change the worker process user.
#
#   group - Switch worker process to run as this group.
#
#       A valid group id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getgrnam(value) or None
#       to change the worker processes group.
#
#   umask - A mask for file permissions written by Gunicorn. Note that
#       this affects unix socket permissions.
#
#       A valid value for the os.umask(mode) call or a string
#       compatible with int(value, 0) (0 means Python guesses
#       the base, so values like "0", "0xFF", "0022" are valid
#       for decimal, hex, and octal representations)
#
#   tmp_upload_dir - A directory to store temporary request data when
#       requests are read. This will most likely be disappearing soon.
#
#       A path to a directory where the process owner can write. Or
#       None to signal that Python should choose one on its own.
#

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

errorlog = '-'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
accesslog = '-'

#
# Process naming
#
#   proc_name - A base to use with setproctitle to change the way
#       that Gunicorn processes are reported in the system process
#       table. This affects things like 'ps' and 'top'. If you're
#       going to be running more than one instance of Gunicorn you'll
#       probably want to set a name to tell them apart. This requires
#       that you install the setproctitle module.
#
#       A string or None to choose a default of something like 'gunicorn'.
#

proc_name = None
