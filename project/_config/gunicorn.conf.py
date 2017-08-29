import multiprocessing, os

bind = '0.0.0.0:%s' % os.environ.get('APP_PORT', '8081')
user = "root"
group = "root"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = '/data/logs/gunicorn_acess.log'
loglevel = "warning"
workers = multiprocessing.cpu_count() * 2 + 1
# TEST: gunicorn -c /data/web/project/config/gunicorn.conf.py main.wsgi:application
