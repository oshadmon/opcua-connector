# OPC-UA Server 
The following provides a OPC-UA server for testing purposses. 

![OPCUA Architecture](opcua_architecture.png)

## Deployment
1. Install python3 with pip and OPCUA package
```shell
python3  -m pip install --upgrade pip 
python3  -m pip install --upgrade opcua>=0.0
```

2. Start OPC-UA service
When using authentication - user: user1 | password: pass123
```shell
python3 server.py [--conn 127.0.0.1:4840] [--string] [--enable-auth] 
```

