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
int 27
float 13
double 10
char 26
bool 27
"""
IDX_VARIABLES = {
   "D1001VFDStop": {'alter_datatype': 'float', 'idx': 0, 'min': 0.0, 'max': 1.0},
   "D1001VFDStopSpeedSetpoint": {'alter_datatype': 'double', 'idx': 1, 'min': 0.0, 'max': 50.0},
   "D2001PELubePumpMtr1Stop": {'alter_datatype': 'bool', 'idx': 2, 'min': 0.0, 'max': 1.0},
   "D1001DriveRunCommandDO": {'alter_datatype': 'float', 'idx': 3, 'min': 0.0, 'max': 1.0},
   "D1001DriveSpeedReferenceAO_ENG": {'alter_datatype': 'int', 'idx': 4, 'min': 0.0, 'max': 1491.0},
   "D1002ChargePumpDriveSpeedReferenceAO_ENG": {'alter_datatype': 'double', 'idx': 5, 'min': 0.0, 'max': 1.8},
   "D2001PELubePumpDriveSpeedReferenceAO_ENG": {'alter_datatype': 'int', 'idx': 6, 'min': 0.0, 'max': 1.0},
   "D1002ChargePumpVFDRunCommandDO": {'alter_datatype': 'float', 'idx': 7, 'min': 0.0, 'max': 1.0},
   "D2001PELubePumpVFDRunCommandDO": {'alter_datatype': 'int', 'idx': 8, 'min': 0.0, 'max': 1.0},
   "CV1001PositionFeedbackAI_ENG": {'alter_datatype': 'float', 'idx': 9, 'min': 0.0, 'max': 100.0},
   "CV1002PositionFeedbackAI_ENG": {'alter_datatype': 'char', 'idx': 10, 'min': 0.0, 'max': 100.0},
   "D1001MotorSpeedAI_ENG": {'alter_datatype': 'char', 'idx': 11, 'min': 0.0, 'max': 1499.541259765625},
   "D1001MotorTorqueAI_ENG": {'alter_datatype': 'double', 'idx': 12, 'min': 0.0, 'max': 2614.678955078125},
   "D1002ChargePumpSpeedAI_ENG": {'alter_datatype': 'char', 'idx': 13, 'min': 0.0, 'max': 1918.417236328125},
   "D1002ChargePumpTorqueAI_ENG": {'alter_datatype': 'bool', 'idx': 14, 'min': 0.0, 'max': 0.0},
   "D2001PELubePumpDriveSpeedAI_ENG": {'alter_datatype': 'int', 'idx': 15, 'min': 0.0, 'max': 14414.728515625},
   "FT1001MainLoopFlowrateAI_ENG": {'alter_datatype': 'double', 'idx': 16, 'min': 0.0, 'max': 1546.874755859375},
   "FT2001PELubeSupplyFlowAI_ENG": {'alter_datatype': 'bool', 'idx': 17, 'min': 0.0, 'max': 87.02466583251953},
   "FT2001PELubeSupplyFlowSetpoint_ENG": {'alter_datatype': 'char', 'idx': 18, 'min': 0.0, 'max': 0.0},
   "LT1001MainWaterTankLevelAI_ENG": {'alter_datatype': 'bool', 'idx': 19, 'min': 0.0, 'max': 93.24625396728516},
   "PT1001MaingPumpChargePressAI_ENG": {'alter_datatype': 'char', 'idx': 20, 'min': 0.0, 'max': 114.5335159301758},
   "PT1002MainPumpDischargePressAI_ENG": {'alter_datatype': 'double', 'idx': 21, 'min': 0.0, 'max': 3.920371398925781},
   "PT1003MainPumpDischargePressAI_ENG": {'alter_datatype': 'int', 'idx': 22, 'min': 0.0, 'max': 1.79097607421875},
   "PT1004ChokeCV1002PressAI_ENG": {'alter_datatype': 'int', 'idx': 23, 'min': 0.0, 'max': 0.0},
   "PT2001PELubeSupplyPressAI_ENG": {'alter_datatype': 'char', 'idx': 24, 'min': 0.0, 'max': 246.5438385009766},
   "PT2001PELubeSupplyPressSetpoint_ENG": {'alter_datatype': 'int', 'idx': 25, 'min': 0.0, 'max': 0.0},
   "PT2002PELubeSupplyPressAI_ENG": {'alter_datatype': 'bool', 'idx': 26, 'min': 0.0, 'max': 105.1539306640625},
   "PT2002PELubeSupplyPressSetpoint_ENG": {'alter_datatype': 'char', 'idx': 27, 'min': 0.0, 'max': 0.0},
   "TC1001PumpTempSensorAI_ENG": {'alter_datatype': 'int', 'idx': 28, 'min': -16.59999847412109, 'max': 210.1999969482422},
   "TC1002PumpTempSensorAI_ENG": {'alter_datatype': 'float', 'idx': 29, 'min': 0.0, 'max': 104.0},
   "TC1003PumpTempSensorAI_ENG": {'alter_datatype': 'bool', 'idx': 30, 'min': 0.0, 'max': 127.3999938964844},
   "TC1004PumpTempSensorAI_ENG": {'alter_datatype': 'float', 'idx': 31, 'min': 0.0, 'max': 107.5999984741211},
   "TC1005PumpTempSensorAI_ENG": {'alter_datatype': 'int', 'idx': 32, 'min': 0.0, 'max': 109.4000015258789},
   "TC1006PumpTempSensorAI_ENG": {'alter_datatype': 'int', 'idx': 33, 'min': 0.0, 'max': 102.1999969482422},
   "TC1007PumpTempSensorAI_ENG": {'alter_datatype': 'bool', 'idx': 34, 'min': 0.0, 'max': 111.1999969482422},
   "TC1008PumpTempSensorAI_ENG": {'alter_datatype': 'bool', 'idx': 35, 'min': 0.0, 'max': 105.7999954223633},
   "TC1009PumpTempSensorAI_ENG": {'alter_datatype': 'double', 'idx': 36, 'min': 0.0, 'max': 105.7999954223633},
   "TC1010PumpTempSensorAI_ENG": {'alter_datatype': 'int', 'idx': 37, 'min': 0.0, 'max': 5928.7998046875},
   "TC1011PumpTempSensorAI_ENG": {'alter_datatype': 'char', 'idx': 38, 'min': 0.0, 'max': 215.5999908447266},
   "TC1012PumpTempSensorAI_ENG": {'alter_datatype': 'double', 'idx': 39, 'min': 0.0, 'max': 111.1999969482422},
   "TT1001MainWaterTemperatureAI_ENG": {'alter_datatype': 'bool', 'idx': 40, 'min': 0.0, 'max': 86.41093444824219},
   "TT2001PELubeTankTempAI_ENG": {'alter_datatype': 'char', 'idx': 41, 'min': 0.0, 'max': 121.0767364501953},
   "TT2002PELubeSupplyTempAI_ENG": {'alter_datatype': 'char', 'idx': 42, 'min': 0.0, 'max': 121.2526016235352},
   "CV1002ChokeValvePositionSetpoint": {'alter_datatype': 'int', 'idx': 43, 'min': 0.0, 'max': 1.0},
   "CV1002ChokeValveStop": {'alter_datatype': 'int', 'idx': 44, 'min': 0.0, 'max': 1.0},
   "CV1001ChokeValveStop": {'alter_datatype': 'float', 'idx': 45, 'min': 0.0, 'max': 1.0},
   "CV1001ChokeValvePositionSetpoint": {'alter_datatype': 'double', 'idx': 46, 'min': 0.0, 'max': 1.0},
   "D1002ChargePumpMotorStop": {'alter_datatype': 'int', 'idx': 47, 'min': 0.0, 'max': 1.0},
   "FT2001LL_AlarmSetpoint": {'alter_datatype': 'char', 'idx': 48, 'min': 0.0, 'max': 65.0},
   "LS1001H_AlarmSetpoint": {'alter_datatype': 'bool', 'idx': 49, 'min': 0.0, 'max': 0.0},
   "LS1002H_AlarmSetpoint": {'alter_datatype': 'bool', 'idx': 50, 'min': 0.0, 'max': 0.0},
   "LS1003H_AlarmSetpoint": {'alter_datatype': 'float', 'idx': 51, 'min': 0.0, 'max': 0.0},
   "LS1004HH_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 52, 'min': 0.0, 'max': 0.0},
   "LS2001L_AlarmSetpoint": {'alter_datatype': 'char', 'idx': 53, 'min': 0.0, 'max': 0.0},
   "LT1001L_AlarmSetpoint": {'alter_datatype': 'bool', 'idx': 54, 'min': 0.0, 'max': 100.0},
   "LT1001LL_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 55, 'min': 0.0, 'max': 60.0},
   "PT1001L_AlarmSetpoint": {'alter_datatype': 'float', 'idx': 56, 'min': 0.0, 'max': 80.0},
   "PT1001LL_AlarmSetpoint": {'alter_datatype': 'double', 'idx': 57, 'min': 0.0, 'max': 50.0},
   "PT1002HH_AlarmSetpoint": {'alter_datatype': 'float', 'idx': 58, 'min': 0.0, 'max': 5000.0},
   "PT1003HH_AlarmSetpoint": {'alter_datatype': 'char', 'idx': 59, 'min': 0.0, 'max': 5000.0},
   "PT2001HH_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 60, 'min': 0.0, 'max': 250.0},
   "PT2002L_AlarmSetpoint": {'alter_datatype': 'bool', 'idx': 61, 'min': 0.0, 'max': 50.0},
   "PT2002LL_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 62, 'min': 0.0, 'max': 55.0},
   "TT1001H_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 63, 'min': 0.0, 'max': 105.0},
   "TT1001HH_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 64, 'min': 0.0, 'max': 110.0},
   "TT2001H_AlarmSetpoint": {'alter_datatype': 'char', 'idx': 65, 'min': 0.0, 'max': 145.0},
   "TT2001HH_AlarmSetpoint": {'alter_datatype': 'int', 'idx': 66, 'min': 0.0, 'max': 165.0},
   "FT2001LL_Alarm": {'alter_datatype': 'int', 'idx': 67, 'min': 0.0, 'max': 1.0},
   "LS1001H_Alarm": {'alter_datatype': 'bool', 'idx': 68, 'min': 0.0, 'max': 1.0},
   "LS1002H_Alarm": {'alter_datatype': 'bool', 'idx': 69, 'min': 0.0, 'max': 0.0},
   "LS1003H_Alarm": {'alter_datatype': 'bool', 'idx': 70, 'min': 0.0, 'max': 0.0},
   "LS1004HH_Alarm": {'alter_datatype': 'bool', 'idx': 71, 'min': 0.0, 'max': 0.0},
   "LS2001L_Alarm": {'alter_datatype': 'char', 'idx': 72, 'min': 0.0, 'max': 1.0},
   "LT1001L_Alarm": {'alter_datatype': 'float', 'idx': 73, 'min': 0.0, 'max': 1.0},
   "LT1001LL_Alarm": {'alter_datatype': 'bool', 'idx': 74, 'min': 0.0, 'max': 1.0},
   "PT1001L_Alarm": {'alter_datatype': 'double', 'idx': 75, 'min': 0.0, 'max': 1.0},
   "PT1001LL_Alarm": {'alter_datatype': 'int', 'idx': 76, 'min': 0.0, 'max': 1.0},
   "PT1002HH_Alarm": {'alter_datatype': 'char', 'idx': 77, 'min': 0.0, 'max': 1.0},
   "PT1003HH_Alarm": {'alter_datatype': 'char', 'idx': 78, 'min': 0.0, 'max': 0.0},
   "PT2001HH_Alarm": {'alter_datatype': 'bool', 'idx': 79, 'min': 0.0, 'max': 1.0},
   "PT2002L_Alarm": {'alter_datatype': 'bool', 'idx': 80, 'min': 0.0, 'max': 0.0},
   "PT2002LL_Alarm": {'alter_datatype': 'bool', 'idx': 81, 'min': 0.0, 'max': 1.0},
   "TT1001H_Alarm": {'alter_datatype': 'char', 'idx': 82, 'min': 0.0, 'max': 1.0},
   "TT1001HH_Alarm": {'alter_datatype': 'char', 'idx': 83, 'min': 0.0, 'max': 1.0},
   "TT2001H_Alarm": {'alter_datatype': 'bool', 'idx': 84, 'min': 0.0, 'max': 0.0},
   "TT2001HH_Alarm": {'alter_datatype': 'char', 'idx': 85, 'min': 0.0, 'max': 1.0},
   "D2002PELubePumpVFDRunCommandDO": {'alter_datatype': 'char', 'idx': 86, 'min': 0.0, 'max': 1.0},
   "D2002PELubePumpDriveSpeedAI_ENG": {'alter_datatype': 'bool', 'idx': 87, 'min': 0.0, 'max': 1235.37060546875},
   "PT2006PELubeSupplyPressSetpointAI_ENG": {'alter_datatype': 'int', 'idx': 88, 'min': 0.0, 'max': 0.0},
   "PT2006PELubeSupplyPressAI_ENG": {'alter_datatype': 'char', 'idx': 89, 'min': 0.0, 'max': 209.7582855224609},
   "PT2005PELubeSupplyPressAI_ENG": {'alter_datatype': 'int', 'idx': 90, 'min': 0.0, 'max': 84.48954010009766},
   "PT2005PELubeSupplyPressSetpointAI_ENG": {'alter_datatype': 'float', 'idx': 91, 'min': 0.0, 'max': 0.0},
   "PT2004PELubeSupplyPressAI_ENG": {'alter_datatype': 'bool', 'idx': 92, 'min': 0.0, 'max': 293.5883178710938},
   "PT2003PELubeSupplyPressAI_ENG": {'alter_datatype': 'bool', 'idx': 93, 'min': 0.0, 'max': 300.1100463867188},
   "FT2002PELubeSupplyFlowAI_ENG": {'alter_datatype': 'char', 'idx': 94, 'min': 0.0, 'max': 26.51929473876953},
   "D2003PELubeCoolerManualSpeedValue": {'alter_datatype': 'int', 'idx': 95, 'min': 0.0, 'max': 1.0},
   "D2002PELubePumpMtr2ManualSpeedValue": {'alter_datatype': 'int', 'idx': 96, 'min': 0.0, 'max': 8.0},
   "D1001MotorEff": {'alter_datatype': 'float', 'idx': 97, 'min': 0.0, 'max': 100.0},
   "D2001PELubePumpDriveEff": {'alter_datatype': 'char', 'idx': 98, 'min': 0.0, 'max': 111867.6015625},
   "D2002PELubePumpDriveEff": {'alter_datatype': 'bool', 'idx': 99, 'min': 0.0, 'max': 3931.418212890625},
   "FT2001PELubeDriveCalculatedFlowrate_ENG": {'alter_datatype': 'char', 'idx': 100, 'min': 0.0, 'max': 6.774921875},
   "FT1001MainLoopCalculatedFlowrateAI_ENG": {'alter_datatype': 'char', 'idx': 101, 'min': 0.0, 'max': 4.9226568603515},
   "FT2002PELubeDriveCalculatedFlowrate_ENG": {'alter_datatype': 'bool', 'idx': 102, 'min': 0.0, 'max': 3.187256240844}
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
                'D1001VFDStop': 'double', 'D1001VFDStopSpeedSetpoint': 'double'
            },
            "PE_Lube_Tags": {
                'D2001PELubePumpMtr1Stop': 'double', 'D2003PELubeCoolerManualSpeedValue': 'double',
                'D2002PELubePumpMtr2ManualSpeedValue': 'double'
            },
            "Outputs": {
                'D1001DriveRunCommandDO': 'double', 'D1001DriveSpeedReferenceAO_ENG': 'double',
                'D1002ChargePumpDriveSpeedReferenceAO_ENG': 'double', 'D2001PELubePumpDriveSpeedReferenceAO_ENG': 'double',
                'D1002ChargePumpVFDRunCommandDO': 'double', 'D2001PELubePumpVFDRunCommandDO': 'double',
                'D2002PELubePumpVFDRunCommandDO': 'double'
            },
            "Inputs": {
                'CV1001PositionFeedbackAI_ENG': 'double', 'CV1002PositionFeedbackAI_ENG': 'double',
                'D1001MotorSpeedAI_ENG': 'float', 'D1001MotorTorqueAI_ENG': 'float',
                'D1002ChargePumpSpeedAI_ENG': 'float', 'D1002ChargePumpTorqueAI_ENG': 'double',
                'D2001PELubePumpDriveSpeedAI_ENG': 'float', 'FT1001MainLoopFlowrateAI_ENG': 'float',
                'FT2001PELubeSupplyFlowAI_ENG': 'float', 'FT2001PELubeSupplyFlowSetpoint_ENG': 'double',
                'LT1001MainWaterTankLevelAI_ENG': 'float', 'PT1001MaingPumpChargePressAI_ENG': 'float',
                'PT1002MainPumpDischargePressAI_ENG': 'float', 'PT1003MainPumpDischargePressAI_ENG': 'float',
                'PT1004ChokeCV1002PressAI_ENG': 'double', 'PT2001PELubeSupplyPressAI_ENG': 'float',
                'PT2001PELubeSupplyPressSetpoint_ENG': 'double', 'PT2002PELubeSupplyPressAI_ENG': 'float',
                'PT2002PELubeSupplyPressSetpoint_ENG': 'double', 'TC1001PumpTempSensorAI_ENG': 'float',
                'TC1002PumpTempSensorAI_ENG': 'double', 'TC1003PumpTempSensorAI_ENG': 'float',
                'TC1004PumpTempSensorAI_ENG': 'float', 'TC1005PumpTempSensorAI_ENG': 'float',
                'TC1006PumpTempSensorAI_ENG': 'float', 'TC1007PumpTempSensorAI_ENG': 'float',
                'TC1008PumpTempSensorAI_ENG': 'float', 'TC1009PumpTempSensorAI_ENG': 'float',
                'TC1010PumpTempSensorAI_ENG': 'float', 'TC1011PumpTempSensorAI_ENG': 'float',
                'TC1012PumpTempSensorAI_ENG': 'float', 'TT1001MainWaterTemperatureAI_ENG': 'float',
                'TT2001PELubeTankTempAI_ENG': 'float', 'TT2002PELubeSupplyTempAI_ENG': 'float',
                'D2002PELubePumpDriveSpeedAI_ENG': 'float', 'PT2006PELubeSupplyPressSetpointAI_ENG': 'double',
                'PT2006PELubeSupplyPressAI_ENG': 'float', 'PT2005PELubeSupplyPressAI_ENG': 'float',
                'PT2005PELubeSupplyPressSetpointAI_ENG': 'double', 'PT2004PELubeSupplyPressAI_ENG': 'float',
                'PT2003PELubeSupplyPressAI_ENG': 'float', 'FT2002PELubeSupplyFlowAI_ENG': 'float',
                'D1001MotorEff': 'double', 'D2001PELubePumpDriveEff': 'float', 'D2002PELubePumpDriveEff': 'float',
                'FT2001PELubeDriveCalculatedFlowrate_ENG': 'float', 'FT1001MainLoopCalculatedFlowrateAI_ENG': 'float',
                'FT2002PELubeDriveCalculatedFlowrate_ENG': 'float'
            },
            "CHOKE_TAGS": {
                'CV1002ChokeValvePositionSetpoint': 'double', 'CV1002ChokeValveStop': 'double',
                'CV1001ChokeValveStop': 'double', 'CV1001ChokeValvePositionSetpoint': 'double'
            },
            "CHARGE_PUMP_TAGS": {
                'D1002ChargePumpMotorStop': 'double'
            },
            "ALARM_TAGS": {
                'FT2001LL_AlarmSetpoint': 'double', 'LS1001H_AlarmSetpoint': 'double',
                'LS1002H_AlarmSetpoint': 'double', 'LS1003H_AlarmSetpoint': 'double',
                'LS1004HH_AlarmSetpoint': 'double', 'LS2001L_AlarmSetpoint': 'double',
                'LT1001L_AlarmSetpoint': 'double', 'LT1001LL_AlarmSetpoint': 'double',
                'PT1001L_AlarmSetpoint': 'double', 'PT1001LL_AlarmSetpoint': 'double',
                'PT1002HH_AlarmSetpoint': 'double', 'PT1003HH_AlarmSetpoint': 'double',
                'PT2001HH_AlarmSetpoint': 'double', 'PT2002L_AlarmSetpoint': 'double',
                'PT2002LL_AlarmSetpoint': 'double', 'TT1001H_AlarmSetpoint': 'double',
                'TT1001HH_AlarmSetpoint': 'double', 'TT2001H_AlarmSetpoint': 'double',
                'TT2001HH_AlarmSetpoint': 'double', 'FT2001LL_Alarm': 'double',
                'LS1001H_Alarm': 'double', 'LS1002H_Alarm': 'double', 'LS1003H_Alarm': 'double',
                'LS1004HH_Alarm': 'double', 'LS2001L_Alarm': 'double', 'LT1001L_Alarm': 'double',
                'LT1001LL_Alarm': 'double', 'PT1001L_Alarm': 'double', 'PT1001LL_Alarm': 'double',
                'PT1002HH_Alarm': 'double', 'PT1003HH_Alarm': 'double', 'PT2001HH_Alarm': 'double',
                'PT2002L_Alarm': 'double', 'PT2002LL_Alarm': 'double', 'TT1001H_Alarm': 'double',
                'TT1001HH_Alarm': 'double', 'TT2001H_Alarm': 'double', 'TT2001HH_Alarm': 'double'
            }
        }

        if is_advanced is True:
            for tag in self.tag_hierarchy:
                for index in self.tag_hierarchy[tag]:
                    if index in IDX_VARIABLES:
                        self.tag_hierarchy[tag][index] = IDX_VARIABLES[index]['alter_datatype']

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
            full_name = IDX_VARIABLES[full_name]['idx'] + 2001
            if len(IDX_OBJECTS) >= 2000:
                full_name = IDX_VARIABLES[full_name]['idx'] + 2001 + len(IDX_OBJECTS)
        elif string_mode == 'int':
            raise ValueError(f'Missing {name} form both objects and variables list(s)')
        elif string_mode == 'long':
            full_name = f"{parent_path}.{name}" if parent_path else name

        return ua.NodeId(full_name, self.idx)


    def add_variables(self, parent_obj, tag_dict, parent_path="", string_mode:str='int'):
        tag_var_dict = {}
        for tag, vtype in tag_dict.items():
            default_value = {"int": 0, "float": 0.0, "bool": False, "char": ""}.get(vtype, None)
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

    def get_random_value(self, vtype, min_val, max_val):
        return {
            "int": int(random.uniform(min_val, max_val)),
            "double": round(random.uniform(min_val, max_val), 2),
            "float": random.uniform(min_val, max_val),
            "bool": random.choice([True, False]),
            "char": random.choice(string.ascii_uppercase)
        }.get(vtype, None)

    def update_variable_values(self, tag_group_var_dicts):
        try:
            while True:
                time.sleep(1)
                for tag_vars in tag_group_var_dicts.values():
                    for var, vtype in tag_vars.values():
                        min_val = IDX_VARIABLES[list(tag_vars.keys())[0]]['min']
                        max_val = IDX_VARIABLES[list(tag_vars.keys())[0]]['max']
                        new_val = self.get_random_value(vtype, min_val, max_val)
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


    opcua_server = OPCUAServer(endpoint=args.opcua_conn, is_advanced=args.advanced_opcua)
    opcua_server.run(enable_auth=args.enable_auth, string_mode=args.string_mode)
