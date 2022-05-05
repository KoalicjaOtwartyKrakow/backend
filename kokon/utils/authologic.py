import requests
from requests.auth import HTTPBasicAuth
from kokon.settings import AUTHOLOGIC_URL, AUTHOLOGIC_USER, AUTHOLOGIC_PASS


def start_conversation(user_id: str, host_url: str):
    response = requests.post(
        AUTHOLOGIC_URL,
        json={
            "userKey": user_id,
            "returnUrl": f"{host_url}/registration?conversation={'conversationId'}",
            "strategy": "salamlab:general",
            "query": {
                "identity": {
                    "fields": {
                        "mandatory": [
                            "PERSON_NAME_FIRSTNAME",
                            "PERSON_NAME_LASTNAME",
                            "PERSON_CONTACT_PHONE",
                            "PERSON_CONTACT_EMAIL",
                        ]
                    }
                }
            },
        },
        headers={
            "Accept": "application/vnd.authologic.v1.1+json",
            "Content-Type": "application/vnd.authologic.v1.1+json",
        },
        auth=HTTPBasicAuth(AUTHOLOGIC_USER, AUTHOLOGIC_PASS),
    )

    # TODO: handle other response codes
    if response.status_code == 200:
        return {"id": response.json()["id"], "url": response.json()["url"]}
