from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .lib.data import DataStore
from .lib.search import RESearch
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

    if query is None or data_file is None:
        return HttpResponse("invalid request. query and/or file are missing")
    query = query.strip()
    data_file = data_file.strip()
    if query.strip() == "" or data_file == "":
        return HttpResponse("invalid request. query and/or file are missing")
    
    if not ds.exists(data_file):
        return HttpResponse("file not found")

    res = RESearch(filepath=ds.absolute_path(data_file))
    out = res.search(query)
    
    context = {
        "q": query,
        "f": data_file,
        "name": out.get("name"),
        "matches": out.get("matches"),
    }
    return render(request, "search-results.html", context)

