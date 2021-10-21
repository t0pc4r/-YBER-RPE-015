# RPE-015

## VM Info

While on the lab network, the VM can be reached by ssh'ing to IP 10.137.85.33 on port 10022:

```
ssh -p 10022 sysadmin@10.137.85.33
```

The password is on the Signal chat.

## Kibana

To view Kibana, open a browser to `10.137.85.33:5601`

Example of some data:

http://10.137.85.33:5601/app/discover#/?_g=(filters:!(),query:(language:kuery,query:''),refreshInterval:(pause:!f,value:10000),time:(from:'2020-09-01T22:44:36.830Z',to:now))&_a=(columns:!(),filters:!(),index:b62871c0-ea71-11eb-bb2c-539718c64181,interval:auto,query:(language:kuery,query:''),sort:!(!('@timestamp',desc)))

## Elasticsearch

Elasticsearch is running in the VM but the port is being forwarded to `19200` on the `10.137.85.33` host.

## OpenCTI

### Start the instance

```
./start_opencti.sh
```

### Log in

User: fake@fake.com
Password: openctiadminpassword

### Tear Down

```
./stop_opencti.sh
```
