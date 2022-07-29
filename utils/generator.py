import requests


async def gen_image(prompt: str, style):
    """
    It gets the token, gets the ID of the task, creates the task, and
    checks if the image is done.

    :param prompt: The text that will be written on the image
    :type prompt: str
    :param style: The style of the image
    :return: The URL of the image.
    """
    with requests.Session() as session:

        # Getting the token for the user.
        get_token = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw",
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                              "like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "content-type": "application/json",
                "x-client-version": "Firefox/JsCore/9.1.2/FirebaseCore-web",
                "Origin": "https://app.wombo.art",
                "DNT": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "TE": "trailers"
            }, json={
                "returnSecureToken": "true"
            }).json()
        id_token = get_token["idToken"]

        # It's getting the ID of the task.
        get_id = requests.post("https://paint.api.wombo.ai/api/tasks", headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://app.wombo.art/",
            "Authorization": f"bearer {id_token}",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://app.wombo.art",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }, json={
            "premium": False
        }).json()

        task_id = get_id["id"]

        # It's creating the task.
        initCreateTask = requests.put(f"https://paint.api.wombo.ai/api/tasks/{task_id}", headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://app.wombo.art/",
            "Authorization": f"bearer {id_token}",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://app.wombo.art",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": "_ga_BRH9PT4RKM=GS1.1.1644347760.1.0.1644347820.0; _ga=GA1.1.1610806426.1644347761",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }, json={
            "input_spec": {
                "prompt": prompt,
                "style": style.value,
                "display_freq": 10
            }
        })

    # It's checking if the image is done.
    while True:
        r = session.get(f"https://paint.api.wombo.ai/api/tasks/{task_id}", headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://app.wombo.art/",
            "Authorization": f"bearer {id_token}",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": "_ga_BRH9PT4RKM=GS1.1.1644347760.1.0.1644347820.0; _ga=GA1.1.1610806426.1644347761",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        })
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

    finishedImage_url = data["result"]["final"]
    return finishedImage_url
