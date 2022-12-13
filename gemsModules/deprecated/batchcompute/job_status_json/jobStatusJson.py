import sys, json
JobStatusEntry = {
    "label": "NotSet",
    "date": "NotSet",
    "time": "NotSet",
    "type": "NotSet", 
    "jobId": "NotSet",
    "messages": "NotSet",
    "errors": "NotSet",
    "queue": "NotSet",
    "status": "NotSet",
    "ahead_r": "NotSet",
    "ahead_w": "NotSet",
    "ahead_o": "NotSet",
    "elapsed": "NotSet",
    "remaining": "NotSet",
    "stdout": "NotSet",
    "stderr": "NotSet",
    "testresult": "NotSet",
    "reason": "NotSet",
}

BatchJobSetInfo = {
    "webId": "NotSet",
    "directory": "NotSet",
    "messages": "NotSet",
    "errors" : "NotSet",
    "jobInfo":[],
}

def dump_job_set_json(batch_job_set, file_path):
    with open (file_path, "w") as json_file:
        json.dump(batch_job_set, json_file, indent = 4)

if (__name__ == '__main__'):
  batch_job_set=BatchJobSetInfo
  batch_job_set['jobInfo'].append(JobStatusEntry)
  dump_job_set_json(batch_job_set,"temp.json")
  print("""

Please inspect and then delete the file temp.json.

If that file was not generated, then something is wrong.

""")
