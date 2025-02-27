from django.conf import settings
from .lib.data import DataStore
from .lib.search import RESearch
from celery import shared_task
import os

ds = DataStore(os.path.join(settings.BASE_DIR, "data"))


@shared_task()
def run_search(filename, pattern):
    # TODO -- args validation
    res = RESearch(filepath=ds.absolute_path(filename), include_match=True)
    return res.search(pattern)
