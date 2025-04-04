import argparse
import random
from opcua import Server, ua
import time


class OPCUAServer:
    def __init__(self, endpoint="127.0.0.1:4840"):
        self.server = Server()
        self.endpoint = f"opc.tcp://{endpoint}/freeopcua/server/"
        self.idx = None
        self.tag_hierarchy = {
            "VFD_CNTRL_TAGS": ['D1001VFDStop', 'D1001VFDStopSpeedSetpoint'],
            "PE_Lube_Tags": ['D2001PELubePumpMtr1Stop', 'D2003PELubeCoolerManualSpeedValue',
                             'D2002PELubePumpMtr2ManualSpeedValue'],
            "Outputs": ['D1001DriveRunCommandDO', 'D1001DriveSpeedReferenceAO_ENG', 'D1002ChargePumpDriveSpeedReferenceAO_ENG',
                        'D2001PELubePumpDriveSpeedReferenceAO_ENG'],
            "Inputs": ['CV1001PositionFeedbackAI_ENG', 'CV1002PositionFeedbackAI_ENG', 'D1001MotorSpeedAI_ENG',
                       'D1001MotorTorqueAI_ENG'],
            "CHOKE_TAGS": ['CV1002ChokeValvePositionSetpoint', 'CV1002ChokeValveStop'],
            "CHARGE_PUMP_TAGS": ['D1002ChargePumpMotorStop'],
            "ALARM_TAGS": ['FT2001LL_AlarmSetpoint', 'LS1001H_AlarmSetpoint', 'LS1002H_AlarmSetpoint']
        }

    def setup_server(self):
        """Setup server and create necessary OPC UA nodes."""
        self.server.set_endpoint(self.endpoint)
        self.idx = self.server.register_namespace("http://example.org")

        objects = self.server.get_objects_node()
        device_set = objects.add_object(self.idx, "DeviceSet")
        wago_device = device_set.add_object(self.idx, "WAGO 750-8210 PFC200 G2 4ETH XTR")
        resources = wago_device.add_object(self.idx, "Resources")
        application = resources.add_object(self.idx, "Application")
        global_vars = application.add_object(self.idx, "GlobalVars")
        return global_vars, wago_device

    def add_variables(self, parent_obj, tag_list, path_prefix="", is_string:bool=False):
        """Helper function to add variables under a parent object."""
        tag_var_dict = {}
        for tag in tag_list:
            if is_string is True:
                full_path = f"{path_prefix}.{tag}" if path_prefix else tag
                var = parent_obj.add_variable(ua.NodeId(full_path, self.idx), tag, False)
                tag_var_dict[tag] = var
            else:
                # Add a variable for each tag
                var = parent_obj.add_variable(self.idx, tag, False)  # Assuming default value as False for booleans, change accordingly.
                tag_var_dict[tag] = var
        return tag_var_dict

    def create_tag_group_objects(self, global_vars, wago_device, is_string:bool=False):
        """Create tag group objects and variables under GlobalVars."""
        tag_group_objs = {}
        tag_group_var_dicts = {}

        for tag_group, tags in self.tag_hierarchy.items():
            tag_group_obj = global_vars.add_object(self.idx, tag_group)
            tag_group_objs[tag_group] = tag_group_obj

            # Construct the full string-based path for NodeId
            path_prefix = f"DeviceSet.{wago_device.get_browse_name().Name}.Resources.Application.GlobalVars.{tag_group}"
            tag_group_var_dict = self.add_variables(parent_obj=tag_group_obj, tag_list=tags, path_prefix=path_prefix, is_string=is_string)
            tag_group_var_dicts[tag_group] = tag_group_var_dict

        return tag_group_var_dicts

    def set_variables_writable(self, tag_group_var_dicts):
        """Set all variables as writable."""
        for tag_vars in tag_group_var_dicts.values():
            for var in tag_vars.values():
                var.set_writable()

    def start_server(self):
        """Start the OPC UA server."""
        self.server.start()
        print(f"Server is running at {self.server.endpoint}")

    def update_variable_values(self, tag_group_var_dicts):
        """Periodically update variable values."""
        try:
            while True:
                time.sleep(1)
                for tag_vars in tag_group_var_dicts.values():
                    for var in tag_vars.values():
                        var.set_value(random.random())
        except KeyboardInterrupt:
            print("Server stopped.")
        finally:
            self.server.stop()

    def run(self, is_string:bool=False):
        """Run the OPC UA server and handle operations."""
        global_vars, wago_device = self.setup_server()
        tag_group_var_dicts = self.create_tag_group_objects(global_vars, wago_device, is_string=is_string)
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()
        self.update_variable_values(tag_group_var_dicts)




if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--opcua-conn', type=str, default='127.0.0.1:4840', help="OPC-UA connection IP + Port")
    parse.add_argument('--string', type=bool, nargs='?', const=True, default=False, help='Use string var as opposed to int')
    args = parse.parse_args()
    # Create and run the OPC UA server
    opcua_server = OPCUAServer(endpoint=args.opcua_conn)
    opcua_server.run(is_string=args.string)
