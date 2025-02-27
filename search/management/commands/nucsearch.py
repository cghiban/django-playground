from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from search.lib.data import DataStore
from search.lib.search import RESearch
import os

ds = DataStore(os.path.join(settings.BASE_DIR, "data"))

class Command(BaseCommand):
    help = "searches given pattern in the given file"

    def add_arguments(self, parser):
        parser.add_argument("pattern", nargs=1, type=str)
        parser.add_argument("file", nargs=1, type=str)

    def handle(self, *args, **options):
        pattern = options["pattern"]
        filename = options["file"]

        if not ds.exists(filename[0]):
            self.stderr.write(
                self.style.ERROR(f"file {filename} not found")
            )

        res = RESearch(filepath=ds.absolute_path(filename[0]), include_match=True)
        out = res.search(pattern[0])
        print(f">{out["name"]}. Found {len(out["matches"])} matches")
        for m in out["matches"]:
            print(f"{m[0]}..{m[1]}\t{m[2]}")
