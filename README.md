# OPC-UA Server

This repository provides an OPC-UA server simulator for testing and development purposes.

![OPCUA Architecture](opcua_architecture.png)

### Data Structure
The server exposes 103 data points, structured under the DeviceSet node, rotating between types such as int, float, boolean, and char.

```lua
|- ns=2;s=DeviceSet
|-- ns=2;s=WAGO 750-8210 PFC200 G2 4ETH XTR
|--- ns=2;s=Resources
|---- ns=2;s=Application
|----- ns=2;s=GlobalVars
|------ ns=2;s=ALARM_TAGS
|------- ns=2;s=FT2001LL_AlarmSetpoint
|------- ns=2;s=LS1001H_AlarmSetpoint
|------- ns=2;s=LS1002H_AlarmSetpoint
|------ ns=2;s=CHARGE_PUMP_TAGS
|------- ns=2;s=D1002ChargePumpMotorStop
```

---

## Run via Docker

The simulator can be run using Docker. Set the following environment variables to configure the server:

| Variable        | Description                                                               | Default        |
|----------------|---------------------------------------------------------------------------|----------------|
| `OPCUA_CONN`    | IP:Port for the OPC-UA server                                              | `0.0.0.0:4840` |
| `STRING_MODE`   | NodeId indexing format: `int`, `short`, or `long`                         | `short`        |
| `CHANGE_RATE`   | Frequency of value updates (in seconds)                                   | `1`            |
| `VALUE_CHANGE`  | Rate of numeric value change (as a float)                                 | `None`         |
| `UPDATE_BASE`   | If true, updates the base value during value change                       | `false`        |
| `ADVANCED_OPCUA`| Enable support for multiple data types                                    | `false`        |
| `GET_HELP`      | Show command-line help and exit                                           | `false`        |


When deploying an OPC-UA server with a `VALUE_CHANGE` parameter, the system begins by generating an initial random 
floating-point number between 10 and 1000. This number becomes the _base value_ for each variable.

For each update cycle, a new value is generated within a percentage range of this base value. The range is calculated as:
```
new_value ∈ [base_value × (1 - VALUE_CHANGE), base_value × (1 + VALUE_CHANGE)]
```

For example, if the current base value is 25.314 and VALUE_CHANGE is 0.05, the next value will be randomly selected 
between - **min**: `25.314 × 0.95 = 24.0483` and **max**: `25.314 × 1.05 = 26.5797`. 

The optional flag `UPDATE_BASE`, when set to **True**, updates the base value to the newly generated value after each 
change. This causes future values to evolve relative to the latest one, allowing the variable to "drift" over time rather 
than fluctuate around a fixed starting point.

### Docker Example

```bash
docker run -d -p 4840:4840 \
  -e OPCUA_CONN=0.0.0.0:4840 \
  -e STRING_MODE=short \
  -e CHANGE_RATE=1 \
  -e VALUE_CHANGE=0.05 \
  -e UPDATE_BASE=true \
  -e ENABLE_AUTH=true \
  -e ADVANCED_OPCUA=true \
  -e GET_HELP=false \
  --detach-keys=ctrl-d --name opcua-simulator --rm oshadmon/opcua-simulator
```

## Local Deployment
1. Install dependencies
```shell
python3 -m pip install --upgrade pip
python3 -m pip install opcua>=0.0
```

2. Start the OPC-UA server
```shell
python3 server.py \
  [--opcua-conn 127.0.0.1:4840] \
  [--string-mode {int, short, long}] \
  [--change-rate 1.0] \
  [--value-change 0.05] \
  [--update-base] \
  [--advanced-opcua]
```
When --advanced-opcua is used, tag values may be of type int, float, char, or string.  Without it, all values are floats / double.

--- 

## Accessing Data by Index Format

* Long format -- `python3 server.py --string-mode long`
```anylog
# Sample Query
<set opcua values where 
    url=opc.tcp://127.0.0.1:4840/freeopcua/server and
    node="ns=2;s=DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars.ALARM_TAGS.FT2001LL_AlarmSetpoint" and 
    include=all>
```

* Short form -- `python3 server.py --string-mode short`
```anylog
# Sample Query
<set opcua values where 
    url=opc.tcp://127.0.0.1:4840/freeopcua/server and
    node="ns=2;s=FT2001LL_AlarmSetpoint" and 
    include=all>
```

* Int form -- `python3 server.py --string-mode int`
```anylog
# Sample Query
<set opcua values where 
    url=opc.tcp://127.0.0.1:4840/freeopcua/server and
    node="ns=2;i=2017" and 
    include=all>
```
 

