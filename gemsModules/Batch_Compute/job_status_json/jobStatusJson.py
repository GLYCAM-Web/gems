import sys, json
JobStatusEntry = {
    "label": "NotSet\n",
    "date": "NotSet\n",
    "time": "NotSet\n",
    "type": "NotSet\n", 
    "jobId": "NotSet\n",
    "messages": "NotSet\n",
    "errors": "NotSet\n",
    "queue": "NotSet\n",
    "status": "NotSet\n",
    "ahead_r": "NotSet\n",
    "ahead_w": "NotSet\n",
    "ahead_o": "NotSet\n",
    "elapsed": "NotSet\n",
    "remaining": "NotSet\n",
    "stdout": "NotSet\n",
    "stderr": "NotSet\n",
    "testresult": "NotSet\n",
    "reason": "NotSet\n",
}

BatchJobSetInfo = {
    "webId": "NotSet\n",
    "directory": "NotSet\n",
    "messages": "NotSet\n",
    "errors" : "NotSet\n",
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
