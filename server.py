import argparse
import random
import string
import time

from opcua import Server, ua
from opcua.server.user_manager import UserManager

# Static NodeIds for Objects (folders/nodes)
IDX_OBJECTS = [
    "DeviceSet",
    "WAGO 750-8210 PFC200 G2 4ETH XTR",
    "Resources",
    "Application",
    "GlobalVars",
    "VFD_CNTRL_TAGS",
    "PE_Lube_Tags",
    "Outputs",
    "Inputs",
    "CHOKE_TAGS",
    "CHARGE_PUMP_TAGS",
    "ALARM_TAGS"
]

# Static NodeIds for Variables (leaf tags)
""" 
int: 18
float: 19
char: 14
bool: 15
"""
IDX_VARIABLES = {
  "D1001VFDStop": "int",
  "D1001VFDStopSpeedSetpoint": "char",
  "D2001PELubePumpMtr1Stop": "int",
  "D2003PELubeCoolerManualSpeedValue": "float",
  "D2002PELubePumpMtr2ManualSpeedValue": "float",
  "D1001DriveRunCommandDO": "bool",
  "D1001DriveSpeedReferenceAO_ENG": "bool",
  "D1002ChargePumpDriveSpeedReferenceAO_ENG": "float",
  "D2001PELubePumpDriveSpeedReferenceAO_ENG": "bool",
  "D1002ChargePumpVFDRunCommandDO": "char",
  "D2001PELubePumpVFDRunCommandDO": "char",
  "CV1001PositionFeedbackAI_ENG": "int",
  "CV1002PositionFeedbackAI_ENG": "float",
  "D1001MotorSpeedAI_ENG": "char",
  "D1001MotorTorqueAI_ENG": "char",
  "D1002ChargePumpSpeedAI_ENG": "float",
  "D1002ChargePumpTorqueAI_ENG": "float",
  "D2001PELubePumpDriveSpeedAI_ENG": "int",
  "FT1001MainLoopFlowrateAI_ENG": "int",
  "FT2001PELubeSupplyFlowAI_ENG": "bool",
  "FT2001PELubeSupplyFlowSetpoint_ENG": "bool",
  "LT1001MainWaterTankLevelAI_ENG": "float",
  "PT1001MaingPumpChargePressAI_ENG": "char",
  "PT1002MainPumpDischargePressAI_ENG": "char",
  "PT1003MainPumpDischargePressAI_ENG": "float",
  "PT1004ChokeCV1002PressAI_ENG": "float",
  "PT2001PELubeSupplyPressAI_ENG": "int",
  "PT2001PELubeSupplyPressSetpoint_ENG": "int",
  "PT2002PELubeSupplyPressAI_ENG": "bool",
  "PT2002PELubeSupplyPressSetpoint_ENG": "int",
  "TC1001PumpTempSensorAI_ENG": "bool",
  "TC1002PumpTempSensorAI_ENG": "float",
  "TC1003PumpTempSensorAI_ENG": "int",
  "TC1004PumpTempSensorAI_ENG": "bool",
  "TC1005PumpTempSensorAI_ENG": "char",
  "TC1006PumpTempSensorAI_ENG": "float",
  "TC1007PumpTempSensorAI_ENG": "bool",
  "TC1008PumpTempSensorAI_ENG": "float",
  "TC1009PumpTempSensorAI_ENG": "float",
  "TC1010PumpTempSensorAI_ENG": "int",
  "TC1011PumpTempSensorAI_ENG": "int",
  "TC1012PumpTempSensorAI_ENG": "bool",
  "TT1001MainWaterTemperatureAI_ENG": "int",
  "TT2001PELubeTankTempAI_ENG": "bool",
  "TT2002PELubeSupplyTempAI_ENG": "char",
  "CV1002ChokeValvePositionSetpoint": "int",
  "CV1002ChokeValveStop": "float",
  "CV1001ChokeValveStop": "char",
  "CV1001ChokeValvePositionSetpoint": "char",
  "D1002ChargePumpMotorStop": "bool",
  "FT2001LL_AlarmSetpoint": "char",
  "LS1001H_AlarmSetpoint": "bool",
  "LS1002H_AlarmSetpoint": "char",
  "LS1003H_AlarmSetpoint": "int",
  "LS1004HH_AlarmSetpoint": "int",
  "LS2001L_AlarmSetpoint": "char",
  "LT1001L_AlarmSetpoint": "int",
  "LT1001LL_AlarmSetpoint": "float",
  "PT1001L_AlarmSetpoint": "int",
  "PT1001LL_AlarmSetpoint": "float",
  "PT1002HH_AlarmSetpoint": "float",
  "PT1003HH_AlarmSetpoint": "int",
  "PT2001HH_AlarmSetpoint": "float",
  "PT2002L_AlarmSetpoint": "bool",
  "PT2002LL_AlarmSetpoint": "bool",
  "TT1001H_AlarmSetpoint": "float"
}



def authenticate(username, password):
    return username == "user1" and password == "pass123"


class OPCUAServer:
    def __init__(self, endpoint="127.0.0.1:4840", is_advanced:bool=False):
        self.server = Server()
        self.endpoint = f"opc.tcp://{endpoint}/freeopcua/server/"
        self.idx = None

        self.tag_hierarchy = {
            "VFD_CNTRL_TAGS": {
                'D1001VFDStop': "float",
                'D1001VFDStopSpeedSetpoint': "float"
            },
            "PE_Lube_Tags": {
                'D2001PELubePumpMtr1Stop': "float",
                'D2003PELubeCoolerManualSpeedValue': "float",
                'D2002PELubePumpMtr2ManualSpeedValue': "float"
            },
            "Outputs": {
                'D1001DriveRunCommandDO': "float",
                'D1001DriveSpeedReferenceAO_ENG': "float",
                'D1002ChargePumpDriveSpeedReferenceAO_ENG': "float",
                'D2001PELubePumpDriveSpeedReferenceAO_ENG': "float",
                'D1002ChargePumpVFDRunCommandDO': "float",
                'D2001PELubePumpVFDRunCommandDO': "float"
            },
            "Inputs": {
                'CV1001PositionFeedbackAI_ENG': "float",
                'CV1002PositionFeedbackAI_ENG': "float",
                'D1001MotorSpeedAI_ENG': "float",
                'D1001MotorTorqueAI_ENG': "float",
                'D1002ChargePumpSpeedAI_ENG': "float",
                'D1002ChargePumpTorqueAI_ENG': "float",
                'D2001PELubePumpDriveSpeedAI_ENG': "float",
                'FT1001MainLoopFlowrateAI_ENG': "float",
                'FT2001PELubeSupplyFlowAI_ENG': "float",
                'FT2001PELubeSupplyFlowSetpoint_ENG': "float",
                'LT1001MainWaterTankLevelAI_ENG': "float",
                'PT1001MaingPumpChargePressAI_ENG': "float",
                'PT1002MainPumpDischargePressAI_ENG': "float",
                'PT1003MainPumpDischargePressAI_ENG': "float",
                'PT1004ChokeCV1002PressAI_ENG': "float",
                'PT2001PELubeSupplyPressAI_ENG': "float",
                'PT2001PELubeSupplyPressSetpoint_ENG': "float",
                'PT2002PELubeSupplyPressAI_ENG': "float",
                'PT2002PELubeSupplyPressSetpoint_ENG': "float",
                'TC1001PumpTempSensorAI_ENG': "float",
                'TC1002PumpTempSensorAI_ENG': "float",
                'TC1003PumpTempSensorAI_ENG': "float",
                'TC1004PumpTempSensorAI_ENG': "float",
                'TC1005PumpTempSensorAI_ENG': "float",
                'TC1006PumpTempSensorAI_ENG': "float",
                'TC1007PumpTempSensorAI_ENG': "float",
                'TC1008PumpTempSensorAI_ENG': "float",
                'TC1009PumpTempSensorAI_ENG': "float",
                'TC1010PumpTempSensorAI_ENG': "float",
                'TC1011PumpTempSensorAI_ENG': "float",
                'TC1012PumpTempSensorAI_ENG': "float",
                'TT1001MainWaterTemperatureAI_ENG': "float",
                'TT2001PELubeTankTempAI_ENG': "float",
                'TT2002PELubeSupplyTempAI_ENG': "float"
            },
            "CHOKE_TAGS": {
                'CV1002ChokeValvePositionSetpoint': "float",
                'CV1002ChokeValveStop': "float",
                'CV1001ChokeValveStop': "float",
                'CV1001ChokeValvePositionSetpoint': "float"
            },
            "CHARGE_PUMP_TAGS": {
                'D1002ChargePumpMotorStop': "float"
            },
            "ALARM_TAGS": {
                'FT2001LL_AlarmSetpoint': "float",
                'LS1001H_AlarmSetpoint': "float",
                'LS1002H_AlarmSetpoint': "float",
                'LS1003H_AlarmSetpoint': "float",
                'LS1004HH_AlarmSetpoint': "float",
                'LS2001L_AlarmSetpoint': "float",
                'LT1001L_AlarmSetpoint': "float",
                'LT1001LL_AlarmSetpoint': "float",
                'PT1001L_AlarmSetpoint': "float",
                'PT1001LL_AlarmSetpoint': "float",
                'PT1002HH_AlarmSetpoint': "float",
                'PT1003HH_AlarmSetpoint': "float",
                'PT2001HH_AlarmSetpoint': "float",
                'PT2002L_AlarmSetpoint': "float",
                'PT2002LL_AlarmSetpoint': "float",
                'TT1001H_AlarmSetpoint': "float"
            }
        }

        if is_advanced is True:
            for tag in self.tag_hierarchy:
                for index in self.tag_hierarchy[tag]:
                    if index in IDX_VARIABLES:
                        self.tag_hierarchy[tag][index] = IDX_VARIABLES[index]

    def setup_server(self, enable_auth:bool=False, string_mode:str='int'):
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name("OPC-UA Server")
        self.idx = self.server.register_namespace("http://example.org")

        if enable_auth:
            self.server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
            self.setup_authentication()
        # else:
        #     self.server.set_security_policy(ua.SecurityPolicyType.NoSecurity)

        objects = self.server.get_objects_node()
        device_set = objects.add_object(
            self.build_nodeid("DeviceSet", string_mode=string_mode),
            "DeviceSet")

        wago = device_set.add_object(
            self.build_nodeid("WAGO 750-8210 PFC200 G2 4ETH XTR", parent_path="DeviceSet", string_mode=string_mode),
            "WAGO 750-8210 PFC200 G2 4ETH XTR")

        resources = wago.add_object(
            self.build_nodeid("Resources", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR", string_mode=string_mode),
            "Resources")

        application = resources.add_object(
            self.build_nodeid("Application", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources", string_mode=string_mode),
            "Application")

        global_vars = application.add_object(
            self.build_nodeid("GlobalVars", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application", string_mode=string_mode),
            "GlobalVars")

        return global_vars

    def setup_authentication(self):
        """Configure user authentication."""
        # Usernames and passwords can be stored securely or loaded from a database.
        self.valid_users = {
            "root": "demo"
        }

        # Here we define the authentication callback function
        self.server.user_manager.authenticate = self.authenticate_user

    def authenticate_user(self, username, password):
        """Authenticate user based on username and password."""
        if username in self.valid_users and self.valid_users[username] == password:
            print(f"User '{username}' authenticated successfully.")
            return True
        else:
            print(f"Authentication failed for user '{username}'.")
            return False

    def build_nodeid(self, name, parent_path="", string_mode:str='int'):
        full_name = name

        if string_mode == 'int' and full_name in IDX_OBJECTS:
            full_name = IDX_OBJECTS.index(full_name) + 1000
        elif string_mode == 'int' and full_name in list(IDX_VARIABLES.keys()):
            full_name = list(IDX_VARIABLES.keys()).index(full_name) + 2001
            if len(IDX_OBJECTS) >= 2000:
                full_name = list(IDX_VARIABLES.keys()).index(full_name) + 2001 + len(IDX_OBJECTS)
        elif string_mode == 'int':
            raise ValueError(f'Missing {name} form both objects and variables list(s)')
        elif string_mode == 'long':
            full_name = f"{parent_path}.{name}" if parent_path else name

        return ua.NodeId(full_name, self.idx)


    def add_variables(self, parent_obj, tag_dict, parent_path="", string_mode:str='int'):
        tag_var_dict = {}
        for tag, vtype in tag_dict.items():
            default_value = self.get_default_value(vtype)
            nodeid = self.build_nodeid(tag, parent_path=parent_path, string_mode=string_mode)
            var = parent_obj.add_variable(nodeid, tag, default_value)
            tag_var_dict[tag] = (var, vtype)
        return tag_var_dict

    def create_tag_group_objects(self, global_vars, string_mode:str='int'):
        tag_group_var_dicts = {}
        base_path = "DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars"

        for tag_group, tags_with_types in self.tag_hierarchy.items():
            parent_path = f"{base_path}.{tag_group}" if string_mode == 'long' else base_path
            tag_group_nodeid = self.build_nodeid(tag_group, parent_path=base_path if string_mode == 'long' else "", string_mode=string_mode)
            tag_group_obj = global_vars.add_object(tag_group_nodeid, tag_group)
            tag_group_var_dicts[tag_group] = self.add_variables(tag_group_obj, tags_with_types, parent_path=parent_path, string_mode=string_mode)

        return tag_group_var_dicts

    def set_variables_writable(self, tag_group_var_dicts):
        for tag_vars in tag_group_var_dicts.values():
            for var, _ in tag_vars.values():
                var.set_writable()

    def start_server(self):
        self.server.start()
        print(f"Server is running at {self.server.endpoint}")

    def get_default_value(self, vtype):
        return {"int": 0, "float": 0.0, "bool": False, "char": ""}.get(vtype, None)

    def get_random_value(self, vtype):
        return {
            "int": random.randint(0, 1000),
            "float": round(random.uniform(0, 100.0), 2),
            "bool": random.choice([True, False]),
            "char": random.choice(string.ascii_uppercase)
        }.get(vtype, None)

    def update_variable_values(self, tag_group_var_dicts):
        try:
            while True:
                time.sleep(1)
                for tag_vars in tag_group_var_dicts.values():
                    for var, vtype in tag_vars.values():
                        new_val = self.get_random_value(vtype)
                        var.set_value(new_val)
        except KeyboardInterrupt:
            print("Server stopped by user.")
        finally:
            self.server.stop()

    def run(self, enable_auth=False, string_mode:str='int'):
        global_vars = self.setup_server(enable_auth=enable_auth, string_mode=string_mode)
        tag_group_var_dicts = self.create_tag_group_objects(global_vars, string_mode=string_mode)
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()
        self.update_variable_values(tag_group_var_dicts)

if __name__ == "__main__":
    """
    Sample server for OPC-UA
    :optonal arguments: 
        -h, --help          show this help message and exit
        --opcua-conn        OPC-UA connection IP + Port
        --string-mode       String NodeId mode
            * int   --          ns=2;s=FT2001LL_AlarmSetpoint
            * short --          ns=2;s=FT2001LL_AlarmSetpoint
            * long  --          ns=2;s=DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application.GlobalVars.ALARM_TAGS.FT2001LL_AlarmSetpoint
        --enable-auth       Enable authentication
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--opcua-conn', type=str, default='127.0.0.1:4840', help="OPC-UA connection IP + Port")
    parser.add_argument('--string-mode', choices=['int', 'short', 'long'], default='int', help='String NodeId mode')
    parser.add_argument('--enable-auth', type=bool, nargs='?', const=True, default=False, help='Enable authentication')
    parser.add_argument('--advanced-opcua', type=bool, nargs='?', const=True, default=False, help='Multiple data types, as opposed to only float values')
    args = parser.parse_args()


    opcua_server = OPCUAServer(endpoint=args.opcua_conn, is_advanced=True)
    opcua_server.run(enable_auth=args.enable_auth, string_mode=args.string_mode)
