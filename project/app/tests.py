from django_rq import job


@job
def worker_test():
    print('*'*50)
    print('WORKER OK')
    print('*'*50)
    return 'OK'


@job
def scheduler_test():
    return 'OK'
