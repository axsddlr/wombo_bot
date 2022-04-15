from json import dumps

import requests


async def gen_image(prompt: str, style):
    with requests.Session() as session:
        r = session.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw",
            json={"returnSecureToken": True})
        data = r.json()
        token = data["idToken"]
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
        state = data["state"]

        if state == "completed":
            break
        if state == "failed":
            print(data)
            raise RuntimeError(data)

    finishedImage_url = data["photo_url_list"][-1]
    return finishedImage_url
