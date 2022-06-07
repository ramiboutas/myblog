# gunicorn.conf.py
# Non logging stuff
bind = "unix:/run/gunicorn_myblog.sock"
workers = 3
# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn_myblog.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn_myblog.error.log"
# Whether to send Django output to the error log
capture_output = True
# How verbose the Gunicorn error logs should be
loglevel = "info"
