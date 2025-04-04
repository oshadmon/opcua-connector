import argparse
from opcua import Server
from opcua import ua
from opcua.server.user_manager import UserManager
import ssl


TAG_HIERARCHY = {
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


def __add_variables(idx, parent_obj, tag_list, path_prefix="", is_string:bool=False):
    """
    Function to add variables with string NodeIds
    """
    tag_var_dict = {}
    for tag in tag_list:
        if is_string is True:
            full_path = f"{path_prefix}.{tag}" if path_prefix else tag
            var = parent_obj.add_variable(ua.NodeId(full_path, idx), tag, False)
            tag_var_dict[tag] = var
        else:
            var = parent_obj.add_variable(idx, tag, False)  # Assuming default value as False for booleans, change accordingly.
            tag_var_dict[tag] = var

    return tag_var_dict


def connect_opcua(conn:str='127.0.0.1:4840'):
    server = Server()
    server.set_endpoint(f"opc.tcp://{conn}/freeopcua/server/")
    idx  = server.register_namespace('http://example.org')
    return server, idx

def create_objs()

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('opcua_conn', type=str, default='127.0.0.1:4840', help='OPC-UA connection IP and Port')
    parse.add_argument('--str', type=bool, nargs='?', const=True, default=False, help='use string based OPC-UA values')
    args = parse.parse_args()

    server, idx = connect_opcua()
