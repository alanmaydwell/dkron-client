from dkron_client import DKronClient

daemons = ["CISMONERR", "MAN0B020D", "MAN0B060D",
           "MAN0B070DD", "MAN0B070DP", "MAN0C010D"]
dkron_url = "http://url_here:8080"

print(f"Accessing: {dkron_url}")
dkron = DKronClient(dkron_url)
dkron_status = dkron.get_dkron_status()
if dkron_status.status_code == 200:
    dkron.restart_job_list(daemons)
else:
    print(f"DKron error code: {dkron_status.status_code}")
