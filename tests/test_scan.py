import unittest
import requests

class TestScanEndpoint(unittest.TestCase):

    def test_scan_endpoint(self):
        base_url = "https://llmsearch.dandiarchive.org/scan/"
        
        query = "Are there any dandisets that contain EEG data?"

        payload = {"query": query}
        response = requests.post(base_url, json=payload)

        self.assertEqual(response.status_code, 200)

        response = response.json()
        ids = response.get("ids", [])
        names = response.get("names", [])

        self.assertTrue(ids)
        self.assertTrue(names)
        self.assertEqual(len(ids), 6)
        self.assertEqual(len(names), 6)

        for id in ids:
            url = f"https://dandiarchive.org/dandiset/{id}"
            url_response = requests.get(url)
            self.assertEqual(url_response.status_code, 200, f"URL {url} is not reachable.")


if __name__ == "__main__":
    unittest.main()