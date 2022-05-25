from json import dumps

import requests


async def gen_image(prompt: str, style):
    with requests.Session() as session:

        data = "grant_type=refresh_token&refresh_token=AIwUaOmMdukSqJZSdchKpoLStrStqB7a1Uj9KfIDy8Z-mYnZPqXJlXRhZWy7SaOJPA2fKWX69oa04YqMLzVtXMnEvU_BYdxzij40PJke1wA8hGoo6OkWXgMpC-v5kT9M-q-B6Zwm4u61kzsubCyophH-nhOmKoeI6iUa1OnjOMrNouaVKVnfBOM"

        r = session.post(
            "https://securetoken.googleapis.com/v1/token?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        data = r.json()
        token = data["id_token"]
        auth_headers = {"Authorization": "bearer " + token}

        # retrieve task id
        r = session.post("https://app.wombo.art/api/tasks", headers=auth_headers, json=dumps({"premium": False}))
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
