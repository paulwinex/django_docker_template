from django.core.management.base import BaseCommand, CommandError
from app.models import Dummy


class Command(BaseCommand):
    help = 'Init database'

    def handle(self, *args, **options):
        try:
            if not Dummy.objects.count():
                for i in range(5):
                    Dummy.objects.create(value='Value %s' % i)
                self.stdout.write(self.style.SUCCESS('Successfully init'))
            else:
                self.stdout.write(self.style.SUCCESS('Database is filled'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
