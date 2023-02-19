from celery import Celery

celery = Celery('web', broker='redis://redis:6379/0', backend='redis://redis:6379')
celery.autodiscover_tasks(['tasks.data_parser'])
