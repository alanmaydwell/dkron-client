import threading
import time
import requests


class DKronClient:
    def __init__(self, url):
        self.url = url + "/v1"

    def get_dkron_status(self):
        response = requests.get(self.url)
        return response

    def make_job_url(self, job):
        # upper-case job names fail
        return self.url + "/jobs/" + job.lower()

    def get_job_status(self, job):
        return requests.get(self.make_job_url(job))

    def run_job(self, job):
        """Warning - may block if the chosen job runs indefinitely"""
        response = requests.post(self.make_job_url(job))
        return response

    def run_job_in_thread(self, job):
        """
        Don't get response from API when starting a daemon, maybe because the daemon
        itself runs indefinitely and API is waiting for it to finish. Running in
        in thread to stop this from blocking things"""
        # daemon=True is for Python, not the API. Stops script waiting for threads to complete.
        run_job_thread = threading.Thread(target=self.run_job, args=(job,), daemon=True)
        run_job_thread.start()

    def is_job_running(self, job):
        result = False
        response = self.get_job_status(job)
        if response.status_code == 200:
            json = response.json()
            displayname = json.get("displayname")
            if "*RUNNING*" in displayname:
                result = True
        return result

    def restart_job(self, job):
        running = self.is_job_running(job)
        if not running:
            self.run_job_in_thread(job)
            # Delay is a bit of bodge to allow time for job to start
            time.sleep(0.5)
            running = self.is_job_running(job)
            print(f"Job {job} restarted. Running status now: {running}")
        else:
            print(f"Job {job} is already running")

    def restart_job_list(self, job_list):
        for job in job_list:
            self.restart_job((job))
