import unittest
import requests

from dandi.dandiapi import DandiAPIClient

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

        dandi_client = DandiAPIClient()
        for i, id in enumerate(ids):
            try:
                ds_id, ds_version = id.split("/")
                dandiset = dandi_client.get_dandiset(ds_id, ds_version)
                print(dandiset)
            except Exception:
                self.fail("Invalid dandiset ID.")
            self.assertEqual(dandiset.get_raw_metadata()["name"], names[i])



if __name__ == "__main__":
    unittest.main()