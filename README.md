# project

Steps to run the server:

Run the celery worker(s)
```shell
python -m celery -A nucsearch worker -l info
```

Run the server
```shell
python manage.py runserver
```

Changelog:
* added celery to perform the searches as background jobs
* added tool for regexp searching through the stored files (`manage.py nucsearch <pattern> <file>`)
* added tool for fetching nucleodide data from NCBI (`manage.py nucfetch <id>`)
* setup Django with two views to handle basic search
* converted regexp.py into a lib in ./search/lib
* still debating on using a DB or not
* not sure if I should fetch the file in XML format first and then convirt it to FASTA (not seeing any benefits)

#### TODO:

    [x] - create tool to fetch data from NCBI
    [x] - create tool to perform regexp searches
    [] - compress storred data (gzip) and handle searches from gzipped FASTA files
    [x] - make use of celery w/ redis for search
    [] - add a SearchForm and use this instead of what we do in search::views::search
    [] - refactor the search to make use of some Ajaxy calls
    [] - save search results, on disk, and link to them as text files
    [] - paginate results on large results
    [] - fix the html templates
    [] - modify the tools to make use of the celery task
    [] - add new task for fetching the data (we can then download data from the browser)
    [] - dockerize app
    [] - make use of docker compose to run the server and workers


