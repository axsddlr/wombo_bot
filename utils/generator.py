from json import dumps

import requests


async def gen_image(prompt: str, style):
    with requests.Session() as session:

        data = "grant_type=refresh_token&refresh_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjFhZjYwYzE3ZTJkNmY4YWQ1MzRjNDAwYzVhMTZkNjc2ZmFkNzc3ZTYiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiNml4MHMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcGFpbnQtcHJvZCIsImF1ZCI6InBhaW50LXByb2QiLCJhdXRoX3RpbWUiOjE2NTAwMDY4ODcsInVzZXJfaWQiOiJwRVY0ZFBZS2haWGo0VzFBMGRmcGtJM055eGYxIiwic3ViIjoicEVWNGRQWUtoWlhqNFcxQTBkZnBrSTNOeXhmMSIsImlhdCI6MTY1OTA2NzY2MiwiZXhwIjoxNjU5MDcxMjYyLCJlbWFpbCI6ImF4c2RsckBpY2xvdWQuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiYXBwbGUuY29tIjpbIjAwMTcwMC5hMTI2OWMwOTRlNzA0ZmY1OTRlOTUxZmQzMWU4NDRmNS4wNzAwIl0sImVtYWlsIjpbImF4c2RsckBpY2xvdWQuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiYXBwbGUuY29tIn19.H8rKg9P4yAsoHvQWolhM4oHcj5L7SUak7PDzDsVctKO2FDXk57ohYguST_SaN8lg-9BmHBDE2bzkmWyBvvAew0YsDIfMUjDsKM4nWACDxnOZltzPRyJGi3Xapc8h0eWKnJtNCYYgrrcT8R0Vv8NKkzaLSRhiNQzCX_DBqvBuL9Ai3n8UHZ14-qFPljufFiBzb-GVMLIO3BFhUENNRM3EtslUJoxpCmhIdHTkW2OLpQoqQsafqXJYbdqUjkNYOEBTjEHrxh9T1_jiCAKX2OjNjYriu9EIgoROX7Teuncc3rUA29WJVmEqgwv_9lPYIAnFPLddux0IwdCli92ZCcTz9A"

        r = session.post(
            "https://securetoken.googleapis.com/v1/token?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw", data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        data = r.json()
        token = data["id_token"]
        auth_headers = {"Authorization": "bearer " + token}

        # retrieve task id
        r = session.post("https://paint.api.wombo.ai/api/tasks", headers=auth_headers, json=dumps({"premium": False}))
        data = r.json()

        task_id = data["id"]

        # Start the task
        query = {"input_spec": {
            "display_freq": 10,
            "prompt": prompt,
            "style": style.value
        }}
        r = session.put("https://app.wombo.art/api/tasks/" + task_id, json=dumps(query), headers=auth_headers)
        data = r.json()

    while True:
        r = session.get("https://app.wombo.art/api/tasks/" + task_id, headers=auth_headers)
        data = r.json()
        if "state" in data:
            state = data["state"]

            if state == "completed":
                break
            if state == "failed":
                print(data)

                raise RuntimeError(data)

        if not ("state" in data):
            return

    finishedImage_url = data["photo_url_list"][-1]
    return finishedImage_url
