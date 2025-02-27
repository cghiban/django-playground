from celery.result import AsyncResult
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .lib.data import DataStore
from search.tasks import run_search
import os

ds = DataStore(os.path.join(settings.BASE_DIR, "data"))

def index(request):
    data_files = ds.get_data_files()
    selected = None
    if request.GET.dict().get("f") is not None:
        f = request.GET.dict()["f"]
        if f in data_files:
            selected = f

    context = {
        "data_files": data_files,
        "selected": selected,
    }
    return render(request, "index.html", context)

def search(request):
    get_data = request.GET.dict()
    query  = get_data.get("q")
    data_file  = get_data.get("f")

    # extra check to prevent path traversal
    if data_file.find("..") != -1:
        return HttpResponse("invalid request. file not found")

    if query is None or data_file is None:
        return HttpResponse("invalid request. query and/or file are missing")
    query = query.strip()
    data_file = data_file.strip()
    if query.strip() == "" or data_file == "":
        return HttpResponse("invalid request. query and/or file are missing")

    if not ds.exists(data_file):
        return HttpResponse("file not found")

    task = run_search.delay(data_file, query)

    return redirect(f"./check-task?t={task.id}&q={query}&f={data_file}")

def check_task(request):
    get_data = request.GET.dict()
    query  = get_data.get("q")
    data_file  = get_data.get("f")
    task_id = get_data.get("t").strip()
    if task_id == "":
        return HttpResponse("invalid request. missing task id", status_code=400)

    task_result = AsyncResult(task_id)

    context = {
        "q": query,
        "f": data_file,
        "task_id": task_id,
        "task_status": task_result.status,
    }
    return render(request, "check-task.html", context)


def search_results(request):
    get_data = request.GET.dict()
    query  = get_data.get("q")
    data_file  = get_data.get("f")
    task_id = get_data.get("t").strip()
    if task_id == "":
        return HttpResponse("invalid request. missing task id", status_code=400)

    task_result = AsyncResult(task_id)

    if task_result.ready():
        result = task_result.result
        context = {
            "q": query,
            "f": data_file,
            "task_id": task_id,
            "task_status": task_result.status,
            "matches": result.get("matches"),
            "name": result.get("name"),
        }
        return render(request, "search-results.html", context)

