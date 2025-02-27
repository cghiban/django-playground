from django.test import TestCase # type: ignore
from search.lib.search import RESearch
import tempfile
import os

class SearchTestCase(TestCase):
    def setUp(self):
        pass

    def test_search_happy_path(self):
        """Ensure search is correct"""

        fs = tempfile.NamedTemporaryFile(delete=False)
        fs.write(b">s1\nXGATACAACAAC")
        fs.close()

        res = RESearch(filepath=fs.name, include_match=True)
        out = res.search("(GATA|ACA)")

        self.assertTrue("matches" in out)
        self.assertEqual(len(out["matches"]), 2, "we have matches")
        self.assertIn("GATA", [m[2] for m in out["matches"]])
        self.assertIn("ACA", [m[2] for m in out["matches"]])

        os.unlink(fs.name)
        self.assertFalse(os.path.exists(fs.name), "Test file removed")

    def test_search_404(self):
        """Test when we have no matches"""

        fs = tempfile.NamedTemporaryFile(delete=False)
        fs.write(b">s2\nXGATACAACAAC")
        fs.close()

        res = RESearch(filepath=fs.name, include_match=True)
        out = res.search("DJANGO")
        
        self.assertTrue("matches_count" in out)
        self.assertEqual(out["matches_count"], 0)
        
        self.assertTrue("name" in out)
        self.assertTrue("s2" in out["name"], "seq id matches")
        
        self.assertTrue("matches" in out)
        self.assertEqual(len(out["matches"]), 0, "we have no matches")
        
        os.unlink(fs.name)
        self.assertFalse(os.path.exists(fs.name), "Test file removed")
