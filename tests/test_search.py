import unittest
from search import load_homes, parse_query, search_homes

class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.homes = load_homes()

    def test_csv_loaded(self):
        self.assertEqual(len(self.homes), 2500)
        self.assertEqual(self.homes[0]['price'], 380935)
        self.assertEqual(self.homes[0]['baths'], 2.5)

    def test_text_query(self):
        parsed = parse_query('3 bedrooms 2 baths under $450k near tennis courts and coffee within 8 minutes')
        self.assertEqual(parsed['max_price'], 450000)
        self.assertEqual(parsed['beds'], 3)
        self.assertEqual(parsed['baths'], 2)
        self.assertEqual(parsed['minutes'], 8)
        self.assertEqual(parsed['lifestyles'], ['Tennis courts', 'Coffee shops'])

    def test_combined_filters_and_strict_proximity(self):
        results = search_homes(self.homes, lifestyles=['Tennis courts', 'Parks'], minutes=12,
                               strict=True, max_price=450000, beds=3, baths=2)
        self.assertTrue(results)
        for h in results:
            self.assertLessEqual(h['price'], 450000)
            self.assertGreaterEqual(h['beds'], 3)
            self.assertGreaterEqual(h['baths'], 2)
            self.assertTrue(all(h['times'][n] <= 12 for n in ['Tennis courts', 'Parks']))

    def test_sort_empty_and_score(self):
        self.assertEqual(search_homes(self.homes, max_price=1), [])
        result = search_homes(self.homes, sort='Price: low to high')
        self.assertEqual([h['price'] for h in result], sorted(h['price'] for h in self.homes))
        self.assertIsNone(result[0]['score'])
        ranked = search_homes(self.homes, lifestyles=['Tennis courts'])
        self.assertEqual([h['score'] for h in ranked], sorted([h['score'] for h in ranked], reverse=True))

if __name__ == '__main__':
    unittest.main()
