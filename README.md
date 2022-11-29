# csc

A simple, insecure service that creates a self-signed CA, and returns self signed certificates
and keys.  Each passkey is only useable once, and is only valid for 5 minutes.

Part of the simple docker deployment of dog (https://github.com/relaypro-open/dog).

```
#!/bin/bash
#Get passkey from hopefully secured,encrypted /register endpoint
passkey=$(curl -s http://csc:8000/csc/register | jq -r .passkey)
#Use passkey to request certs and hostkey
certs=$(curl -s -d '{"fqdn": "rabbitmq", "passkey": "'$passkey'"}' http://csc:8000/csc/cert)
echo $certs | jq -r .server_key > /etc/dog/private/server.key
echo $certs | jq -r .server_crt > /etc/dog/certs/server.crt
echo $certs | jq -r .ca_crt >     /etc/dog/certs/ca.crt
#Hostkey is part of dog's config.json
echo $certs | jq -r .hostkey > /etc/dog/config.json
```

Useful for testing TLS connections with mutual TLS authentication.

NOTE: INSECURE, NOT FOR USE IN PRODUCTION!
