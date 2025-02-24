# E-utils

# einfo

curl https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?format=json|jq

```
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?format=json&db=nuccore"|jq
{
  "header": {
    "type": "einfo",
    "version": "0.3"
  },
  "einforesult": {
    "dbinfo": [
      {
        "dbname": "nuccore",
        "menuname": "Nucleotide",
        "description": "Core Nucleotide db",
        "dbbuild": "Build250222-1235m.1",
        "count": "649062146",
        "lastupdate": "2025/02/23 19:58",
        "fieldlist": [

```

```
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?format=json&db=nucleotide"|jq
{
  "header": {
    "type": "einfo",
    "version": "0.3"
  },
  "einforesult": {
    "dbinfo": [
      {
        "dbname": "nuccore",
        "menuname": "Nucleotide",
        "description": "Core Nucleotide db",
        "dbbuild": "Build250222-1235m.1",
        "count": "649062146",
        "lastupdate": "2025/02/23 19:58",
        "fieldlist": [
          {
```

# esummary

```
curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nuccore&id=30271926,224589800&format=json"

{
  "header": {"type": "esummary","version": "0.3"},
  "result": {
    "uids": ["30271926","224589800"],
    "30271926": {
      "uid": "30271926",
      "term": "30271926",
      "caption": "NC_004718",
      "title": "SARS coronavirus Tor2, complete genome",
      "extra": "gi|30271926|ref|NC_004718.3|",
      "gi": 30271926,
      "createdate": "2003/04/14",
      "updatedate": "2020/11/20",
      "flags": 512,
      "taxid": 227984,
      "slen": 29751,
      "biomol": "genomic",
      "moltype": "rna",
      "topology": "linear",
      "sourcedb": "refseq",
      "projectid": "485481",
      "genome": "genomic",
      "subtype": "isolate|host|country",
      "subname": "Tor2|Homo sapiens; patient #2 with severe acute respiratory syndrome (SARS)|Canada: Toronto",
      "assemblygi": 30248028,
      "assemblyacc": "AY274119",
      "completeness": "complete",
      "geneticcode": "1",
      "strand": "",
      "organism": "SARS coronavirus Tor2",
      "oslt": {
        "indexed": true,
        "value": "NC_004718.3"
      },
      "accessionversion": "NC_004718.3"
    },
    "224589800": {
      "uid": "224589800",
      "term": "224589800",
      "caption": "NC_000001",
      "accessionversion": "NC_000001.10",
      "sourcedb": "refseq",
      "title": "Homo sapiens chromosome 1, GRCh37.p13 Primary Assembly",
      "extra": "gi|224589800|gnl|ASM:GCF_000001305|1|ref|NC_000001.10||gpp|GPC_000000025.1||gnl|NCBI_GENOMES|1",
      "gi": 224589800,
      "createdate": "2002/08/29",
      "updatedate": "2013/08/13",
      "genome": "chromosome",
      "organism": "Homo sapiens",
      "taxid": 9606,
      "geneticcode": "1",
      "subtype": "chromosome",
      "subname": "1",
      "slen": 249250621,
      "moltype": "dna",
      "topology": "linear",
      "biomol": "genomic",
      "assemblygi": 224384768,
      "assemblyacc": "CM000663.1",
      "projectid": "PRJNA168",
      "biosample": "",
      "statistics": "",
      "comment": "This sequence has been updated.",
      "status": "replaced",
      "replacedby": "NC_000001.11",
      "flags": 512,
      "idgiclass": {}
    }
  }
}
```


# efetch

```bash
curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=30271926&seq_start=1&seq_stop=1000&rettype=fasta&retmode=text"

curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=30271926&rettype=fasta&retmode=text" -o data/30271926.fasta
```