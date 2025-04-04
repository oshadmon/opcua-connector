import argparse
import random
import string
import time
from opcua import Server, ua
from opcua.server.user_manager import UserManager


def user_authentication(isession, username, password):
    return username == "user1" and password == "pass123"


class OPCUAServer:
    def __init__(self, endpoint="127.0.0.1:4840"):
        self.server = Server()
        self.endpoint = f"opc.tcp://{endpoint}/freeopcua/server/"
        self.idx = None

        # Updated tag hierarchy with types
        self.tag_hierarchy = {
            "VFD_CNTRL_TAGS": {
                'D1001VFDStop': "int",
                'D1001VFDStopSpeedSetpoint': "float"
            },
            "PE_Lube_Tags": {
                'D2001PELubePumpMtr1Stop': "char",
                'D2003PELubeCoolerManualSpeedValue': "bool",
                'D2002PELubePumpMtr2ManualSpeedValue': "int"
            },
            "Outputs": {
                'D1001DriveRunCommandDO': "float",
                'D1001DriveSpeedReferenceAO_ENG': "char",
                'D1002ChargePumpDriveSpeedReferenceAO_ENG': "bool",
                'D2001PELubePumpDriveSpeedReferenceAO_ENG': "int"
            },
            "Inputs": {
                'CV1001PositionFeedbackAI_ENG': "float",
                'CV1002PositionFeedbackAI_ENG': "char",
                'D1001MotorSpeedAI_ENG': "bool",
                'D1001MotorTorqueAI_ENG': "int"
            },
            "CHOKE_TAGS": {
                'CV1002ChokeValvePositionSetpoint': "float",
                'CV1002ChokeValveStop': "char"
            },
            "CHARGE_PUMP_TAGS": {
                'D1002ChargePumpMotorStop': "bool"
            },
            "ALARM_TAGS": {
                'FT2001LL_AlarmSetpoint': "int",
                'LS1001H_AlarmSetpoint': "float",
                'LS1002H_AlarmSetpoint': "bool"
            }
        }

    def setup_server(self, enable_auth: bool = False):
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name("OPC-UA Server")
        self.idx = self.server.register_namespace("http://example.org")

        if enable_auth:
            self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
            self.server.user_manager = UserManager(user_authentication)

        objects = self.server.get_objects_node()
        device_set = objects.add_object(ua.NodeId("DeviceSet", self.idx), "DeviceSet")
        wago_device = device_set.add_object(
            ua.NodeId("WAGO 750-8210 PFC200 G2 4ETH XTR", self.idx),
            "WAGO 750-8210 PFC200 G2 4ETH XTR"
        )
        resources = wago_device.add_object(ua.NodeId("Resources", self.idx), "Resources")
        application = resources.add_object(ua.NodeId("Application", self.idx), "Application")
        global_vars = application.add_object(ua.NodeId("GlobalVars", self.idx), "GlobalVars")

        return global_vars, wago_device

    def add_variables(self, parent_obj, tag_dict):
        tag_var_dict = {}
        for tag, vtype in tag_dict.items():
            default_value = self.get_default_value(vtype)
            var = parent_obj.add_variable(self.idx, tag, default_value)
            tag_var_dict[tag] = (var, vtype)
        return tag_var_dict

    def create_tag_group_objects(self, global_vars, wago_device):
        tag_group_var_dicts = {}

        for tag_group, tags_with_types in self.tag_hierarchy.items():
            tag_group_obj = global_vars.add_object(self.idx, tag_group)
            tag_group_var_dicts[tag_group] = self.add_variables(tag_group_obj, tags_with_types)

        return tag_group_var_dicts

    def set_variables_writable(self, tag_group_var_dicts):
        for tag_vars in tag_group_var_dicts.values():
            for var, _ in tag_vars.values():
                var.set_writable()

    def start_server(self):
        self.server.start()
        print(f"Server is running at {self.server.endpoint}")

    def get_default_value(self, vtype):
        if vtype == "int":
            return 0
        elif vtype == "float":
            return 0.0
        elif vtype == "bool":
            return False
        elif vtype == "char":
            return ""
        return None

    def get_random_value(self, vtype):
        if vtype == "int":
            return random.randint(0, 1000)
        elif vtype == "float":
            return round(random.uniform(0, 100.0), 2)
        elif vtype == "bool":
            return random.choice([True, False])
        elif vtype == "char":
            return random.choice(string.ascii_uppercase)
        return None

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

    def run(self, enable_auth: bool = False, is_string: bool = False):
        global_vars, wago_device = self.setup_server(enable_auth=enable_auth)
        tag_group_var_dicts = self.create_tag_group_objects(global_vars, wago_device)
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()
        self.update_variable_values(tag_group_var_dicts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--opcua-conn', type=str, default='127.0.0.1:4840', help="OPC-UA connection IP + Port")
    parser.add_argument('--string', type=bool, nargs='?', const=True, default=False, help='Use string var names')
    parser.add_argument('--enable-auth', type=bool, nargs='?', const=True, default=False, help='Enable authentication')
    args = parser.parse_args()

    opcua_server = OPCUAServer(endpoint=args.opcua_conn)
    opcua_server.run(enable_auth=args.enable_auth, is_string=args.string)
import argparse
import random
import string
import time
from opcua import Server, ua
from opcua.server.user_manager import UserManager


def user_authentication(isession, username, password):
    return username == "user1" and password == "pass123"


class OPCUAServer:
    def __init__(self, endpoint="127.0.0.1:4840"):
        self.server = Server()
        self.endpoint = f"opc.tcp://{endpoint}/freeopcua/server/"
        self.idx = None

        # Updated tag hierarchy with types
        self.tag_hierarchy = {
            "VFD_CNTRL_TAGS": {
                'D1001VFDStop': "int",
                'D1001VFDStopSpeedSetpoint': "float"
            },
            "PE_Lube_Tags": {
                'D2001PELubePumpMtr1Stop': "char",
                'D2003PELubeCoolerManualSpeedValue': "bool",
                'D2002PELubePumpMtr2ManualSpeedValue': "int"
            },
            "Outputs": {
                'D1001DriveRunCommandDO': "float",
                'D1001DriveSpeedReferenceAO_ENG': "char",
                'D1002ChargePumpDriveSpeedReferenceAO_ENG': "bool",
                'D2001PELubePumpDriveSpeedReferenceAO_ENG': "int"
            },
            "Inputs": {
                'CV1001PositionFeedbackAI_ENG': "float",
                'CV1002PositionFeedbackAI_ENG': "char",
                'D1001MotorSpeedAI_ENG': "bool",
                'D1001MotorTorqueAI_ENG': "int"
            },
            "CHOKE_TAGS": {
                'CV1002ChokeValvePositionSetpoint': "float",
                'CV1002ChokeValveStop': "char"
            },
            "CHARGE_PUMP_TAGS": {
                'D1002ChargePumpMotorStop': "bool"
            },
            "ALARM_TAGS": {
                'FT2001LL_AlarmSetpoint': "int",
                'LS1001H_AlarmSetpoint': "float",
                'LS1002H_AlarmSetpoint': "bool"
            }
        }

    def setup_server(self, enable_auth: bool = False):
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name("OPC-UA Server")
        self.idx = self.server.register_namespace("http://example.org")

        if enable_auth:
            self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
            self.server.user_manager = UserManager(user_authentication)

        objects = self.server.get_objects_node()
        device_set = objects.add_object(ua.NodeId("DeviceSet", self.idx), "DeviceSet")
        wago_device = device_set.add_object(
            ua.NodeId("WAGO 750-8210 PFC200 G2 4ETH XTR", self.idx),
            "WAGO 750-8210 PFC200 G2 4ETH XTR"
        )
        resources = wago_device.add_object(ua.NodeId("Resources", self.idx), "Resources")
        application = resources.add_object(ua.NodeId("Application", self.idx), "Application")
        global_vars = application.add_object(ua.NodeId("GlobalVars", self.idx), "GlobalVars")

        return global_vars, wago_device

    def add_variables(self, parent_obj, tag_dict):
        tag_var_dict = {}
        for tag, vtype in tag_dict.items():
            default_value = self.get_default_value(vtype)
            var = parent_obj.add_variable(self.idx, tag, default_value)
            tag_var_dict[tag] = (var, vtype)
        return tag_var_dict

    def create_tag_group_objects(self, global_vars, wago_device):
        tag_group_var_dicts = {}

        for tag_group, tags_with_types in self.tag_hierarchy.items():
            tag_group_obj = global_vars.add_object(self.idx, tag_group)
            tag_group_var_dicts[tag_group] = self.add_variables(tag_group_obj, tags_with_types)

        return tag_group_var_dicts

    def set_variables_writable(self, tag_group_var_dicts):
        for tag_vars in tag_group_var_dicts.values():
            for var, _ in tag_vars.values():
                var.set_writable()

    def start_server(self):
        self.server.start()
        print(f"Server is running at {self.server.endpoint}")

    def get_default_value(self, vtype):
        if vtype == "int":
            return 0
        elif vtype == "float":
            return 0.0
        elif vtype == "bool":
            return False
        elif vtype == "char":
            return ""
        return None

    def get_random_value(self, vtype):
        if vtype == "int":
            return random.randint(0, 1000)
        elif vtype == "float":
            return round(random.uniform(0, 100.0), 2)
        elif vtype == "bool":
            return random.choice([True, False])
        elif vtype == "char":
            return random.choice(string.ascii_uppercase)
        return None

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

    def run(self, enable_auth: bool = False, is_string: bool = False):
        global_vars, wago_device = self.setup_server(enable_auth=enable_auth)
        tag_group_var_dicts = self.create_tag_group_objects(global_vars, wago_device)
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()
        self.update_variable_values(tag_group_var_dicts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--opcua-conn', type=str, default='127.0.0.1:4840', help="OPC-UA connection IP + Port")
    parser.add_argument('--string', type=bool, nargs='?', const=True, default=False, help='Use string var names')
    parser.add_argument('--enable-auth', type=bool, nargs='?', const=True, default=False, help='Enable authentication')
    args = parser.parse_args()

    opcua_server = OPCUAServer(endpoint=args.opcua_conn)
    opcua_server.run(enable_auth=args.enable_auth, is_string=args.string)
