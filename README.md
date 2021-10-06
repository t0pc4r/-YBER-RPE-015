# RPE-015

## VM Info

While on the lab network, the VM can be reached by ssh'ing to IP 10.137.85.33 on port 10022:

```
ssh -p 10022 sysadmin@10.137.85.33
```

The password is on the Signal chat.

## Kibana

To view Kibana, open a browser to `10.137.85.33:5601`

## Elasticsearch

Elasticsearch is running in the VM but the port is being forwarded to `19200` on the `10.137.85.33` host.
