# DKron Client

Uses DKron scheduler API

## Daemon Restart Script
`start_jobs.py` was created to restart daemons. Uses a thread for each when restarting as we don't get a response from the API for these, presumably because they themselves run indefinitely.

### Setup
In `start_jobs.py` edit the job list in line 3 and the URL in line 5 to suit your environment.

## Requires
- Python
- requests module - `pip install requests`