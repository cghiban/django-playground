# project

Changelog:
* added tool for fetching nucleodide data from NCBI (`manage.py fetchnuc`)
* setup Django with two views to handle basic search
* converted regexp.py into a lib in ./search/lib
* still debating on using a DB or not
* not sure if I should fetch the file in XML format first and then confirt it to FASTA (not seeing any benefits)

#### TODO:

    [x] - create tool to fetch data from NCBI
    [] - create tool to perform regexp searches
    [] - compress storred data (gzip) and handle searches from gzipped FASTA files
    [] - make use of celery w/ redis
    [] - save search results
    [] - paginate results on large results


