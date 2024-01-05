import json
def find_data(file_dir):
    file_dir = file_dir+"/.report.json"
    with open(file_dir) as fp:
        content = json.loads(fp.readlines()[0])
        duration = content["duration"]
        success = content["exitcode"]
        caseCount = content["summary"]["total"]
        try:
            caseSuccessCount = content["summary"]["passed"]
        except KeyError:
            caseSuccessCount = 0
        try:
            caseFailCount = content["summary"]["failed"]
        except KeyError:
            caseFailCount = 0
        caseSkipConut = int(caseCount) - int(caseSuccessCount) - int(caseFailCount)
        data = {"duration": duration, "success": success, "caseCount": caseCount, "caseSuccessCount": caseSuccessCount,
                "caseFailCount": caseFailCount, "caseSkipConut": caseSkipConut}
        data = json.dumps(data)[1:-1]
        return data
