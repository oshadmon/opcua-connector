import argparse
import random
import string
import time
from opcua import Server, ua
from opcua.server.user_manager import UserManager
from opcua.tools import parse_args
import multiprocessing

from server_working import OPCUAServer

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
int 27
float 13
double 10
char 26
bool 27
"""
IDX_VARIABLES = {
   "D1001VFDStop": {'alter_datatype': ua.VariantType.Float, 'idx': 0, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1001VFDStopSpeedSetpoint": {'alter_datatype': ua.VariantType.Double, 'idx': 1, 'min': 0.0, 'max': 50.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2001PELubePumpMtr1Stop": {'alter_datatype': ua.VariantType.Boolean, 'idx': 2, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1001DriveRunCommandDO": {'alter_datatype': ua.VariantType.Float, 'idx': 3, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
    ...,
   "FT2001PELubeDriveCalculatedFlowrate_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 100, 'min': 0.0, 'max': 6.774921875, 'base_value': round(random.uniform(10, 100), 2)},
   "FT1001MainLoopCalculatedFlowrateAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 101, 'min': 0.0, 'max': 4.9226568603515, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2002PELubeDriveCalculatedFlowrate_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 102, 'min': 0.0, 'max': 3.187256240844, 'base_value': round(random.uniform(10, 100), 2)}
}

def authenticate(username, password):
    return username == "user1" and password == "pass123"

def run_variable_updater(server:OPCUAServer, tag_groups, change_rate, value_change, update_base):
    server.update_variable_values(tag_groups, change_rate, value_change, update_base)


class OPCUAServer:
    def __init__(self, endpoint="127.0.0.1:4840", is_advanced: bool = False):
        self.server = Server()
        self.endpoint = f"opc.tcp://{endpoint}/freeopcua/server/"
        self.idx = None
        self.is_advanced = is_advanced

        self.tag_hierarchy = {
            "VFD_CNTRL_TAGS": {
                'D1001VFDStop': ua.VariantType.Double, 'D1001VFDStopSpeedSetpoint': ua.VariantType.Double
            },
            "PE_Lube_Tags": {
                'D2001PELubePumpMtr1Stop': ua.VariantType.Double, 'D2003PELubeCoolerManualSpeedValue': ua.VariantType.Double,
                'D2002PELubePumpMtr2ManualSpeedValue': ua.VariantType.Double
            },
           ...
        }

        if self.is_advanced:
            for tag_group in self.tag_hierarchy:
                for tag_name in self.tag_hierarchy[tag_group]:
                    if tag_name in IDX_VARIABLES:
                        self.tag_hierarchy[tag_group][tag_name] = IDX_VARIABLES[tag_name]['alter_datatype']

    def setup_server(self, enable_auth: bool = False, string_mode: str = 'short'):
        self.server.set_endpoint(self.endpoint)
        self.server.set_server_name("OPC-UA Server")
        self.idx = self.server.register_namespace("http://example.org")

        if enable_auth:
            self.server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
            self.setup_authentication()

        objects = self.server.get_objects_node()
        device_set = objects.add_object(
            self.build_nodeid("DeviceSet", string_mode=string_mode),
            "DeviceSet"
        )

        wago = device_set.add_object(
            self.build_nodeid("WAGO 750-8210 PFC200 G2 4ETH XTR", parent_path="DeviceSet", string_mode=string_mode),
            "WAGO 750-8210 PFC200 G2 4ETH XTR"
        )

        resources = wago.add_object(
            self.build_nodeid("Resources", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR", string_mode=string_mode),
            "Resources"
        )

        application = resources.add_object(
            self.build_nodeid("Application", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources", string_mode=string_mode),
            "Application"
        )

        global_vars = application.add_object(
            self.build_nodeid("GlobalVars", parent_path="DeviceSet.WAGO 750-8210 PFC200 G2 4ETH XTR.Resources.Application", string_mode=string_mode),
            "GlobalVars"
        )

        return global_vars

    def setup_authentication(self):
        self.valid_users = {
            "root": "demo"
        }
        self.server.user_manager.authenticate = self.authenticate_user

    def authenticate_user(self, username, password):
        if username in self.valid_users and self.valid_users[username] == password:
            print(f"User '{username}' authenticated successfully.")
            return True
        else:
            print(f"Authentication failed for user '{username}'.")
            return False

    def build_nodeid(self, name, parent_path="", string_mode='short'):
        # string_mode can be 'int', 'short', or 'long'
        if string_mode == 'int':
            if name in IDX_OBJECTS:
                node_id_value = IDX_OBJECTS.index(name) + 1000
            elif name in IDX_VARIABLES:
                node_id_value = IDX_VARIABLES[name]['idx'] + 2001
                if len(IDX_OBJECTS) >= 2000:
                    node_id_value += len(IDX_OBJECTS)
            else:
                raise ValueError(f"Missing {name} from both objects and variables list(s)")
            return ua.NodeId(node_id_value, self.idx)
        elif string_mode == 'short':
            # Use string name as is
            return ua.NodeId(name, self.idx)
        elif string_mode == 'long':
            full_name = f"{parent_path}.{name}" if parent_path else name
            return ua.NodeId(full_name, self.idx)
        else:
            raise ValueError(f"Unknown string_mode '{string_mode}'")

    def add_variables(self, parent_obj, tag_dict, parent_path="", string_mode='short'):
        tag_var_dict = {}
        for tag, vtype in tag_dict.items():
            default_value = {
                ua.VariantType.Int32: 0,
                ua.VariantType.Float: 0.0,
                ua.VariantType.Double: 0.0,
                ua.VariantType.Boolean: False,
                ua.VariantType.String: "",
            }.get(vtype, None)
            nodeid = self.build_nodeid(tag, parent_path=parent_path, string_mode=string_mode)
            var = parent_obj.add_variable(nodeid, tag, default_value, varianttype=vtype)
            tag_var_dict[tag] = (var, vtype)
        return tag_var_dict

    def create_tag_group_objects(self, global_vars, string_mode='short'):
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
        print(f"Server is running at {self.endpoint}")

    def get_random_value(self, vtype, min_val, max_val, base_value=None):
        return {
            ua.VariantType.Int32: int(random.uniform(min_val, max_val)),
            ua.VariantType.Double: round(random.uniform(min_val, max_val), 2),
            ua.VariantType.Float: random.uniform(min_val, max_val),
            ua.VariantType.Boolean: bool(random.getrandbits(1)),
            ua.VariantType.String: ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        }.get(vtype, base_value)

    def update_variable_values(self, tag_group_var_dicts, change_rate, value_change, update_base):
        last_update_time = time.time()
        while True:
            current_time = time.time()
            if current_time - last_update_time >= change_rate:
                last_update_time = current_time
                for tag_group, tag_vars in tag_group_var_dicts.items():
                    for tag, (var, vtype) in tag_vars.items():
                        base_value = IDX_VARIABLES.get(tag, {}).get('base_value', None)
                        min_val = IDX_VARIABLES.get(tag, {}).get('min', 0.0)
                        max_val = IDX_VARIABLES.get(tag, {}).get('max', 1.0)
                        if update_base and base_value is not None:
                            base_value += value_change
                            # Clamp value inside range
                            base_value = max(min_val, min(base_value, max_val))
                            IDX_VARIABLES[tag]['base_value'] = base_value
                            var.set_value(base_value)
                        else:
                            # Random fluctuation around base value
                            new_val = base_value + random.uniform(-value_change, value_change) if base_value else self.get_random_value(vtype, min_val, max_val)
                            # Clamp if numeric
                            if isinstance(new_val, (float, int)):
                                new_val = max(min_val, min(new_val, max_val))
                            var.set_value(new_val)
            time.sleep(0.01)


def run_variable_updater(server, tag_group_name, tag_vars, change_rate, value_change, update_base):
    last_update_time = time.time()
    while True:
        current_time = time.time()
        if current_time - last_update_time >= change_rate:
            last_update_time = current_time
            for tag, (var, vtype) in tag_vars.items():
                base_value = IDX_VARIABLES.get(tag, {}).get('base_value', None)
                min_val = IDX_VARIABLES.get(tag, {}).get('min', 0.0)
                max_val = IDX_VARIABLES.get(tag, {}).get('max', 1.0)
                if update_base and base_value is not None:
                    base_value += value_change
                    base_value = max(min_val, min(base_value, max_val))
                    IDX_VARIABLES[tag]['base_value'] = base_value
                    var.set_value(base_value)
                else:
                    new_val = base_value + random.uniform(-value_change, value_change) if base_value else server.get_random_value(vtype, min_val, max_val)
                    if isinstance(new_val, (float, int)):
                        new_val = max(min_val, min(new_val, max_val))
                    var.set_value(new_val)
        time.sleep(0.01)



def main():
    parser = argparse.ArgumentParser(description="OPC-UA Server")
    parser.add_argument("--endpoint", default="0.0.0.0:4840", help="Endpoint address")
    parser.add_argument("--enable-auth", action="store_true", help="Enable authentication")
    parser.add_argument("--string-mode", choices=['int', 'short', 'long'], default='short', help="NodeId string mode")
    parser.add_argument("--change-rate", type=float, default=1.0, help="Change rate in seconds")
    parser.add_argument("--value-change", type=float, default=0.1, help="Value change amount")
    parser.add_argument("--update-base", action="store_true", help="Update base values")
    parser.add_argument("--advanced", action="store_true", help="Use advanced tag types")
    args = parser.parse_args()

    server = OPCUAServer(endpoint=args.endpoint, is_advanced=args.advanced)
    global_vars = server.setup_server(enable_auth=args.enable_auth, string_mode=args.string_mode)
    tag_group_var_dicts = server.create_tag_group_objects(global_vars, string_mode=args.string_mode)
    server.set_variables_writable(tag_group_var_dicts)

    server.start_server()

    try:
        processes = []
        for tag_group_name, tag_vars in tag_group_var_dicts.items():
            p = multiprocessing.Process(
                target=run_variable_updater,
                args=(server, tag_group_name, tag_vars, args.change_rate, args.value_change, args.update_base)
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        for p in processes:
            p.terminate()
        server.server.stop()

if __name__ == "__main__":
    main()