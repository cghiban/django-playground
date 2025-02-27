# Django playground

Create a virtualenv and activate it:
```shell
$ python3.12 -m venv venv
$ source venv/bin/activate 
```

Install the requirements:
```shell
$ pip install --upgrade pip 
$ pip install -r requirements.txt
```

Fetch some data:
```shell
$ mkdir -p data
$ python manage.py nucfetch 30271926
```

Run a search:
```shell
$ python manage.py nucsearch GATACA  30271926.fa
>search for GATACA in NC_004718.3. Found 4 matches
13787..13793	GATACA
18482..18488	GATACA
25759..25765	GATACA
29449..29455	GATACA
```

### Steps to run the server

Start redis server:
```shell
$ docker run -d --name redis-stack -p 6379:6379 redis/redis-stack-server:latest
```

Run the celery worker(s):
```shell
$ python -m celery -A nucsearch worker -l info
```

Run the server in a separate terminal:
```shell
$ python manage.py runserver
```

Open the browser to http://127.0.0.1:8000/search/

Changelog:
* added celery to perform the searches as background jobs
* added tool for regexp searching through the stored files (`manage.py nucsearch <pattern> <file>`)
* added tool for fetching nucleodide data from NCBI (`manage.py nucfetch <id>`)
* setup Django with two views to handle basic search
* converted regexp.py into a lib in ./search/lib
* still debating on using a DB or not
* not sure if I should fetch the file in XML format first and then convirt it to FASTA (not seeing any benefits)

#### TODO:

    [] - compress storred data (gzip) and handle searches from gzipped FASTA files
    [] - add a SearchForm and use this instead of what we do in search::views::search
    [] - refactor the search to make use of some Ajaxy calls
    [] - save search results, on disk, and link to them as text files
    [] - paginate results on large results
    [] - fix the html templates
    [] - modify the tools to make use of the celery task
    [] - add new task for fetching the data (we can then download data from the browser)
    [] - dockerize app
    [] - make use of docker compose to run the server and workers


