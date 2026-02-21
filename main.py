import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
#comment1
load_dotenv()

app = FastAPI()

GITHUB_SECRET = "ASjhjaskGIrewuPheOTg"


def verify_signature(payload_body: bytes, signature_header: str):
    if not signature_header:
        raise HTTPException(status_code=403, detail="Missing signature")

    sha_name, signature = signature_header.split("=")
    if sha_name != "sha256":
        raise HTTPException(status_code=403, detail="Invalid signature format")

    mac = hmac.new(
        GITHUB_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256,
    )

    if not hmac.compare_digest(mac.hexdigest(), signature):
        raise HTTPException(status_code=403, detail="Invalid signature")


@app.post("/")
async def github_webhook(request: Request):
    body = await request.body()

    signature = request.headers.get("x-hub-signature-256")
    verify_signature(body, signature)

    payload = await request.json()

    branch = payload.get("ref")
    commits = payload.get("commits", [])
    head_commit = payload.get("head_commit", {})

    print("Branch:", branch)
    print("Latest Commit:", head_commit.get("id"))
    print("Message:", head_commit.get("message"))

    for commit in commits:
        print("Commit:", commit["id"], "-", commit["message"])

    return {"status": "success"}