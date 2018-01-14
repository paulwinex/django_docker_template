from django.views.generic import TemplateView, View
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from .models import Dummy
import os


class MainView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(MainView, self).get_context_data(**kwargs)
        try:
            ctx['files'] = os.listdir(settings.MEDIA_ROOT)
        except Exception as e:
            ctx['errors'] = ctx.get('errors', []) + [str(e)]
        ctx['media'] = settings.MEDIA_ROOT
        try:
            values = Dummy.objects.all()
            ctx['values'] = values
        except Exception as e:
            ctx['errors'] = ctx.get('errors', []) + [str(e)]
        return ctx

    def post(self, request, **kwargs):
        errors = []
        if request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            try:
                fs.save(file.name, file)
            except Exception as e:
                errors.append(str(e))
        else:
            errors.append('No FILES in POST')
        ctx = self.get_context_data(**kwargs)
        ctx['errors'] = errors
        return self.render_to_response(ctx)


class RedisTest(View):
    def get(self, request):
        return JsonResponse(self.get_result())

    def get_result(self):
        from .tests import worker_test
        import time
        job = worker_test.delay()
        time.sleep(3)
        if job.is_finished:
            return {'result': job.result}
        else:
            return {'result': 'ERROR'}

from redis import Redis
from rq_scheduler import Scheduler
from rq.job import Job
from datetime import timedelta
from .tests import scheduler_test


class SchedulerTest(View):
    redis_job_name = 'scheduler_test_job_id'

    def get(self, request):
        if 'result' in request.GET:
            return JsonResponse({'result': self.get_result()})
        else:
            self.create_job()
            return JsonResponse({'result': 'OK'})

    @classmethod
    def create_job(cls):
        r = Redis(host=settings.REDIS_HOST, port=6379)
        scheduler = Scheduler(connection=r)
        job = scheduler.enqueue_in(timedelta(seconds=30), scheduler_test)
        r.set(cls.redis_job_name + str(len(list(r.scan_iter(cls.redis_job_name+'*')))), str(job.id))

    @classmethod
    def get_result(cls):
        r = Redis(host=settings.REDIS_HOST, port=6379)
        results = []
        for id in r.scan_iter(cls.redis_job_name + '*'):
            job = Job(r.get(id).decode("utf-8"), Redis(host=settings.REDIS_HOST, port=6379))
            results.append([id.decode("utf-8"), job.result or 'Waiting...'])
            if job.result:
                r.delete(id)
        return results
