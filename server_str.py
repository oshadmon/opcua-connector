import random
from opcua import Server, ua
import time

# Initialize the OPC UA server
server = Server()

# Set server endpoint
server.set_endpoint("opc.tcp://127.0.0.1:4840/freeopcua/server/")

# Setup server namespace
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create the root node
objects = server.get_objects_node()

# Create the DeviceSet object
device_set = objects.add_object(idx, "DeviceSet")

# Create the WAGO device object under DeviceSet
wago_device = device_set.add_object(idx, "WAGO 750-8210 PFC200 G2 4ETH XTR")

# Create the Resources object under WAGO device
resources = wago_device.add_object(idx, "Resources")

# Create the Application object under Resources
application = resources.add_object(idx, "Application")

# Create GlobalVars object under Application
global_vars = application.add_object(idx, "GlobalVars")

# Tag hierarchy dictionary
tag_hierarchy = {
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

# Function to add variables with string NodeIds
def add_variables(parent_obj, tag_list, path_prefix=""):
    tag_var_dict = {}
    for tag in tag_list:
        full_path = f"{path_prefix}.{tag}" if path_prefix else tag
        var = parent_obj.add_variable(ua.NodeId(full_path, idx), tag, False)
        tag_var_dict[tag] = var
    return tag_var_dict

# Create objects and variables under GlobalVars
tag_group_objs = {}
tag_group_var_dicts = {}

for tag_group, tags in tag_hierarchy.items():
    tag_group_obj = global_vars.add_object(idx, tag_group)
    tag_group_objs[tag_group] = tag_group_obj

    # Construct the full string-based path for NodeId
    path_prefix = f"DeviceSet.{wago_device.get_browse_name().Name}.Resources.Application.GlobalVars.{tag_group}"
    tag_group_var_dict = add_variables(tag_group_obj, tags, path_prefix)
    tag_group_var_dicts[tag_group] = tag_group_var_dict

# Set variables as writable
for tag_vars in tag_group_var_dicts.values():
    for var in tag_vars.values():
        var.set_writable()

# Start the server
server.start()
print(f"Server is running at {server.endpoint}")

# Periodically update variable values
try:
    while True:
        time.sleep(1)
        for tag_vars in tag_group_var_dicts.values():
            for var in tag_vars.values():
                var.set_value(random.random())
except KeyboardInterrupt:
    print("Server stopped.")
finally:
    server.stop()
