#!/usr/bin/env python

import config

import subprocess

from typing import Union, Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class PushEvent(BaseModel):
    after: str
    base_ref: str | None
    before: str
    commits: list

@app.post("/webhook")
async def webhook_receive(push_event: PushEvent, x_github_event: Annotated[str | None, Header()] = None):
    if x_github_event == 'push':
        print(push_event)
        result = subprocess.run(config.PUSH_EVENT_CMD, cwd=config.PUSH_EVENT_CMD_CWD, text=True, check=False)
        print(f"Command '{config.PUSH_EVENT_CMD}' exited with code {result.returncode}")
        if result.stdout:
            print(f"Command stdout: {result.stdout}")
        if result.stderr:
            print(f"Command stderr: {result.stderr}")

if __name__ == '__main__':
    print("Started webhook receiver")
