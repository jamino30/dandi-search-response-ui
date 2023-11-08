from locust import HttpUser, task, between

class LocustTests(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_homepage(self):
        self.client.get("")

    @task
    def perform_scan(self):
        payload = {"query": "eeg data is awesome"}
        headers = {'content-type': 'application/json'}
        self.client.post("scan/", json=payload, headers=headers)
