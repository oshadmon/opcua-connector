* full attributes
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and output = stdout and attributes = *
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and output = stdout and node="ns=2"

get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and output = stdout and node="ns=2;i=7" and class = variable and format = get_value

get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and output = stdout and node="ns=2;s=D1001VFDStop " and class = variable and format = get_value

get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/server and node="ns=2;s=DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars.Inputs.CV1001PositionFeedbackAI_ENG"
<get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/server and nodes=[
    "ns=2;i=1", "ns=2;i=2", "ns=2;i=3", "ns=2;i=4", "ns=2;i=5", 
    "ns=2;i=6", "ns=2;i=7", "ns=2;i=8", "ns=2;i=9", "ns=2;i=10"
] and include = all>

get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/server and node="ns=2;i=10" and include = all
get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/server and node="ns=2;s=d2001pelubepumpmtr1stop" and include = all