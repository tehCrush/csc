#!/bin/env python3

import os, sys
from ownca import CertificateAuthority
import string
import random
import uuid
import sqlite3
import datetime
import easy_db
import arrow
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse

db = easy_db.DataBase("/tmp/csc.db")

import uvicorn
from fastapi import FastAPI

app = FastAPI()

basedir ="/tmp/csc"

def store_passkey(passkey):
    timestamp = datetime.datetime.utcnow()
    db.append("request", {"passkey": passkey, "timestamp": timestamp})

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

@app.get("/csc/register")
def csc(request: Request):
    passkey = get_random_string(20)
    store_passkey(passkey)
    return {"passkey": passkey}

@app.post("/csc/cert")
async def cert(info : Request):
    content = await info.json()
    passkey = content["passkey"]
    fqdn = content["fqdn"]
    response = db.pull_where('request', f'passkey = "{ passkey }"')
    print(response)
    if len(response) == 1:
        timestamp = response[0]['timestamp']
        now = arrow.utcnow()
        print(now.shift(minutes=-5))
        print(arrow.get(timestamp))
        if now.shift(minutes=-5) < arrow.get(timestamp):
            certs = create_cert(fqdn,passkey) 
            print(certs)
            with db as cursor:
                sql = 'DELETE FROM REQUEST WHERE PASSKEY=?'
                cursor.execute(sql, (passkey,))
            return certs
        else:
            return {"error": "passkey expired"}
    else:
        return {"error": "passkey does not exist"}

def create_cert(fqdn,passkey):
    ca = CertificateAuthority(ca_storage='/tmp/CA', common_name='dog CA')

    server = ca.issue_certificate(fqdn, dns_names=[fqdn, 'localhost'])
    hostkey = str(uuid.uuid1())

    return {"server_key": server.key_bytes.decode("utf-8"),
            "server_crt": server.cert_bytes.decode("utf-8"), 
            "ca_crt": ca.cert_bytes.decode("utf-8"),
            "hostkey": hostkey}

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def lambda_handler(event, context):
    fqdn = event["fqdn"]
    certs = create_cert(fqdn)
    return certs

def main(argv, stdout, environ):
    fqdn=argv[1]
    event = {"fqdn": fqdn}
    response_map = lambda_handler(event,[])
    print(f"server_key: {response_map['server_key']}")
    print(f"server_key: {response_map['server_key']}")
    print(f"server_crt: {response_map['server_crt']}")

if __name__ == "__main__":
    uvicorn.run("csc:app",reload=True)
