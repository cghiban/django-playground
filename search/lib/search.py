from Bio import SeqIO
import re
from multiprocessing.pool import Pool


def search_batch(pat, start:int, seq:str, include_match:bool=False)->set:
    out = list()
    it = pat.finditer(seq)
    for m in it:
        a, b = m.span()
        # we'll need the coords of the original sequence
        if include_match:
            out.append((a+start, b+start, seq[a:b]))
        else:
            out.append((a+start, b+start))
    return set(out)

class RESearch:
    def __init__(self, filepath, batch_size=None, threads=None, include_match:bool=False):
        self.filepath=filepath
        self.batch_size = 50_000
        self.threads = 8
        self.include_match = include_match
        if batch_size is not None:
            self.batch_size=batch_size
        if threads is not None:
            self.threads=threads

    def search(self, pattern:str)->dict:
        """
        Performs the search. It asumes the fasta file has ony one sequence.
        It returns a list of locations that match the given pattern
        """
        pat = re.compile(pattern)
        sequence = SeqIO.parse(self.filepath, "fasta")
        s = next(sequence)
        total_len = len(s)

        overlap = 40
        num_batches = int(len(s) / self.batch_size) + 1

        batches = []

        for i in range(num_batches):
            start = i * self.batch_size
            end = start + self.batch_size
            if start > 0:
                start -= overlap
            if end > total_len:
                end = total_len
            
            batches.append((pat, start, str(s[start:end].seq), self.include_match))

        uniq_matches = set()
        pool = Pool(processes=self.threads)
        results = pool.starmap(search_batch, batches)

        for r in results:
            uniq_matches.update(r)
        
        return {
            "name": s.id,
            "matches": sorted(uniq_matches),
            "matches_count": len(uniq_matches),
        }
