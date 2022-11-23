#!/bin/env python3

import os, sys
from ownca import CertificateAuthority
basedir ="/tmp/csc"

def lambda_handler(event, context):
    fqdn = event["fqdn"]
    ca = CertificateAuthority(ca_storage='/tmp/CA', common_name='dog CA')

    server = ca.issue_certificate(fqdn, dns_names=[fqdn, 'localhost'])

    return {"server_key": server.key_bytes, 
            "server_crt": server.cert_bytes, 
            "ca_crt": ca.cert_bytes}

def main(argv, stdout, environ):
    fqdn=argv[1]
    event = {"fqdn": fqdn}
    response_map = lambda_handler(event,[])
    print(f"server_key: {response_map['server_key']}")
    print(f"server_key: {response_map['server_key']}")
    print(f"server_crt: {response_map['server_crt']}")

if __name__ == "__main__":
    main(sys.argv, sys.stdout,os.environ)
