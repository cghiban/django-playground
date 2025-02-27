from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from search.lib.data import DataStore
import aiohttp
import asyncio
import os

ds = DataStore(os.path.join(settings.BASE_DIR, "data"))
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CHUNK_SIZE = 100_000

async def run(nucc:str):
    url = EUTILS + f"esummary.fcgi?db=nuccore&id={nucc}&format=json"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if not resp.ok:
                msg = f"ERR: code:{resp.status} - {resp.text()[:90]}"
                print(msg)
                return
            resp = await resp.json()
            #print(resp)
            #print(resp["result"])
            if "result" in resp and nucc not in resp["result"]["uids"]:
                if len(resp["result"]["uids"]) >0:
                    nucc = resp["result"]["uids"][0]
            print(f"nucc: [{ nucc}]")
            #print(resp["result"][nucc])
            print("-----")
            if "result" in resp and nucc in resp["result"]:
                info = resp["result"][nucc]
                desc = nucc
                if "title" in info:
                    desc = info["title"]
                print(f". found {nucc}: {desc}")
                return await _download(session, nucc)
            else:
                print(f"ERR: nucleotide {nucc} not found")
                return None

async def _download(session, nucc):
    filename = f"{nucc}.fa"

    if ds.exists(filename):
        print(f"ERR: file {filename} already exists")
        return None

    url = EUTILS + f"efetch.fcgi?db=nuccore&id={nucc}&rettype=fasta&retmode=text"
    print(f". downloading from {url}")
    full_path = ds.absolute_path(filename)
    print(f". storring file to {full_path}")
    
    bytes_written = 0
    async with session.get(url) as resp:
        if not resp.ok:
            msg = f"ERR: code:{resp.status} - {resp.text()[:90]}"
            print(msg)
            return None
        with open(full_path, 'wb') as fd:
            async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                bytes_written += fd.write(chunk)

    return filename, bytes_written

class Command(BaseCommand):
    help = "fetches nucleotide data by gid/refid and stores it locally in FASTA format"

    def add_arguments(self, parser):
        parser.add_argument("nucc", nargs=1, type=str)

    def handle(self, *args, **options):
        nucc = options["nucc"]
        if not nucc:
            self.stderr.write(
                self.style.ERROR("missing argument <nucc>")
            )
        if type(nucc) == list and len(nucc) > 0:
            nucc = nucc[0].strip()
        
        resp = asyncio.run(run(nucc))
        if resp is not None:
            filename, size = resp
            self.stderr.write(
                self.style.SUCCESS(f"wrote {size} bytes to {filename}")
            )
        else:
            raise CommandError("command failed. see above message(s)")