# OPC-UA Server

**Setup**: 
1. install python3 
2. Install requirements -- _opcua_ 
```shell
python3 -m venv venv 
souce ./venv/bin/activate 
python3 -m pip install --upgrade pip 
python3 -m pip install --upgrade opcua
```
**Run**: 
To run with integer based name
1. start OPC-UA server
```shell
opcua-connector/server.py --opcua-conn 127.0.0.1:4840
```

2. On AnyLog, execute command
```anylog
get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/server and nodes=["ns=2;i=10"] and include = all

<< COMMENT
OPCUA Nodes values
id        name                             source_timestamp           server_timestamp status_code           value              
---------|--------------------------------|--------------------------|----------------|---------------------|------------------|
ns=2;i=1 |deviceset                       |                          |                |BadAttributeIdInvalid|                  |
ns=2;i=2 |wago 750-8210 pfc200 g2 4eth xtr|                          |                |BadAttributeIdInvalid|                  |
ns=2;i=3 |resources                       |                          |                |BadAttributeIdInvalid|                  |
ns=2;i=4 |application                     |                          |                |BadAttributeIdInvalid|                  |
ns=2;i=5 |globalvars                      |                          |                |BadAttributeIdInvalid|                  |
ns=2;i=6 |vfd_cntrl_tags                  |                          |                |BadAttributeIdInvalid|                  |
ns=2;i=7 |d1001vfdstop                    |2025-04-04 00:55:09.453414|                |Good                 |0.8254508736164989|
ns=2;i=8 |d1001vfdstopspeedsetpoint       |2025-04-04 00:55:09.453485|                |Good                 |0.8981730312198819|
ns=2;i=9 |pe_lube_tags                    |                          |                |BadAttributeIdInvalid|                  |
ns=2;i=10|d2001pelubepumpmtr1stop         |2025-04-04 00:55:09.453522|                |Good                 |0.8304308176491271|
<< COMMENT
```

To run with string based name
1. start OPC-UA server
```shell
opcua-connector/server.py --opcua-conn 127.0.0.1:4840 --string
```

2. On AnyLog, execute command
```anylog
get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/server and node="ns=2;s=DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars.Inputs.CV1001PositionFeedbackAI_ENG" and include = all

<< COMMENT
OPCUA Nodes values
id                                                                                                   name                         source_timestamp           server_timestamp status_code value               
----------------------------------------------------------------------------------------------------|----------------------------|--------------------------|----------------|-----------|-------------------|
ns=2;s=DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars.Inputs.CV1001Posi|
tionFeedbackAI_ENG                                                                                  |cv1001positionfeedbackai_eng|2025-04-04 00:55:53.398573|                |Good       |0.17754649485308305|
<< COMMENT
```