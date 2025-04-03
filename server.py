from opcua import Server
from opcua import ua
import time

# Initialize the OPC UA server
server = Server()

# Set server endpoint (you can customize the URL here)
server.set_endpoint("opc.tcp://127.0.0.1:4840/freeopcua/server/")

# Setup server namespace (URI for the namespace)
uri = "http://example.org"
idx = server.register_namespace(uri)

# Create the root node in the address space
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

# Example dictionary with tag names
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


# Helper function to add variables
def add_variables(parent_obj, tag_list):
    tag_var_dict = {}  # Store references to the variables
    for tag in tag_list:
        # Add a variable for each tag
        var = parent_obj.add_variable(idx, tag,
                                      False)  # Assuming default value as False for booleans, change accordingly.
        tag_var_dict[tag] = var
    return tag_var_dict


# Create sub-objects and variables under GlobalVars based on the provided dictionary structure
tag_group_objs = {}  # Store tag group objects for later access
tag_group_var_dicts = {}  # Store dictionaries of variables for each tag group

for tag_group, tags in tag_hierarchy.items():
    # Create an object for each tag group
    tag_group_obj = global_vars.add_object(idx, tag_group)
    tag_group_objs[tag_group] = tag_group_obj  # Store the created object

    # Add variables under the tag group and store them
    tag_group_var_dict = add_variables(tag_group_obj, tags)
    tag_group_var_dicts[tag_group] = tag_group_var_dict

# Set variables to be writable by the client
for tag_group, tag_vars in tag_group_var_dicts.items():
    for tag, var in tag_vars.items():
        var.set_writable()

# Start the server
server.start()

print(f"Server is running at {server.endpoint}")

try:
    # Server running indefinitely, periodically updating values
    while True:
        time.sleep(1)
        for tag_group, tag_vars in tag_group_var_dicts.items():
            for tag, var in tag_vars.items():
                # Check if the data type is Boolean using get_data_type()
                if var.get_data_type() == ua.VariantType.Boolean:
                    var.set_value(True)  # Update boolean tags to True
                else:
                    var.set_value(100.0)  # For numeric tags, set to 100.0
except KeyboardInterrupt:
    print("Server stopped.")
finally:
    server.stop()

