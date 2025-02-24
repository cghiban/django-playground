#!python

from Bio import SeqIO
import re
from multiprocessing.pool import Pool


def search_batch(pat, start:int, seq:str):
    out = list()
    it = pat.finditer(seq)
    for m in it:
        a, b = m.span()
        a += start # we'll need the coords of the original sequence
        b += start
        #print("\t", a, "->", b, "\t // \t", a, "->", b, "\t", m.group(), end="")
        #x = s[a: b + 2]
        #print("\t", str(x.seq))
        out.append((a, b))
    return set(out)

# for i in range(batches):
    
#     start = i * batch_size
#     end = start + batch_size
#     if start > 0:
#         start -= overlap
#     if end > total_len:
#         end = total_len
    
#     results = search_batch(i, pat, s[start:end])
#     uniq_matches.update(results)

if __name__ == "__main__":

    pat = re.compile(r'(AATCGA|GGCAT|GATACA*)')

    file = "data/224589800.fasta"
    #file = "data/30271926.fa"
    sequence = SeqIO.parse(file, "fasta")
    s = next(sequence)
    total_len = len(s)

    overlap = 100
    batch_size = 50_000
    num_batches = int(len(s) / batch_size) + 1

    batches = []
    uniq_matches = set()
    for i in range(num_batches):
        
        start = i * batch_size
        end = start + batch_size
        if start > 0:
            start -= overlap
        if end > total_len:
            end = total_len
        
        #results = search_batch(i, pat, s[start:end])
        #uniq_matches.update(results)
        batches.append((pat, start, str(s[start:end].seq)))  # Tuple for arguments

    pool = Pool(processes=8)
    results = pool.starmap(search_batch, batches)  # Apply search_batch to each chunk tuple

    print("results:", len(results))
    for r in results:
        uniq_matches.update(r)
    

    #print(len(uniq_matches), sorted(uniq_matches))
    print(len(uniq_matches), "matches")
    if len(uniq_matches) < 100:
        for m in sorted(uniq_matches):
            print(m, "\t", s[m[0]:m[1]].seq)
