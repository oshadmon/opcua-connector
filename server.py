import argparse
import random
import string
import time

from opcua import Server, ua
from opcua.server.user_manager import UserManager
from opcua.tools import parse_args

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
   "D1001DriveSpeedReferenceAO_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 4, 'min': 0.0, 'max': 1491.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1002ChargePumpDriveSpeedReferenceAO_ENG": {'alter_datatype': ua.VariantType.Double, 'idx': 5, 'min': 0.0, 'max': 1.8, 'base_value': round(random.uniform(10, 100), 2)},
   "D2001PELubePumpDriveSpeedReferenceAO_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 6, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1002ChargePumpVFDRunCommandDO": {'alter_datatype': ua.VariantType.Float, 'idx': 7, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2001PELubePumpVFDRunCommandDO": {'alter_datatype': ua.VariantType.Int32, 'idx': 8, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "CV1001PositionFeedbackAI_ENG": {'alter_datatype': ua.VariantType.Float, 'idx': 9, 'min': 0.0, 'max': 100.0, 'base_value': round(random.uniform(10, 100), 2)},
   "CV1002PositionFeedbackAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 10, 'min': 0.0, 'max': 100.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1001MotorSpeedAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 11, 'min': 0.0, 'max': 1499.541259765625, 'base_value': round(random.uniform(10, 100), 2)},
   "D1001MotorTorqueAI_ENG": {'alter_datatype': ua.VariantType.Double, 'idx': 12, 'min': 0.0, 'max': 2614.678955078125, 'base_value': round(random.uniform(10, 100), 2)},
   "D1002ChargePumpSpeedAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 13, 'min': 0.0, 'max': 1918.417236328125, 'base_value': round(random.uniform(10, 100), 2)},
   "D1002ChargePumpTorqueAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 14, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2001PELubePumpDriveSpeedAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 15, 'min': 0.0, 'max': 14414.728515625, 'base_value': round(random.uniform(10, 100), 2)},
   "FT1001MainLoopFlowrateAI_ENG": {'alter_datatype': ua.VariantType.Double, 'idx': 16, 'min': 0.0, 'max': 1546.874755859375, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2001PELubeSupplyFlowAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 17, 'min': 0.0, 'max': 87.02466583251953, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2001PELubeSupplyFlowSetpoint_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 18, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LT1001MainWaterTankLevelAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 19, 'min': 0.0, 'max': 93.24625396728516, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1001MaingPumpChargePressAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 20, 'min': 0.0, 'max': 114.5335159301758, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1002MainPumpDischargePressAI_ENG": {'alter_datatype': ua.VariantType.Double, 'idx': 21, 'min': 0.0, 'max': 3.920371398925781, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1003MainPumpDischargePressAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 22, 'min': 0.0, 'max': 1.79097607421875, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1004ChokeCV1002PressAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 23, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2001PELubeSupplyPressAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 24, 'min': 0.0, 'max': 246.5438385009766, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2001PELubeSupplyPressSetpoint_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 25, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2002PELubeSupplyPressAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 26, 'min': 0.0, 'max': 105.1539306640625, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2002PELubeSupplyPressSetpoint_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 27, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1001PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 28, 'min': -16.59999847412109, 'max': 210.1999969482422, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1002PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Float, 'idx': 29, 'min': 0.0, 'max': 104.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1003PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 30, 'min': 0.0, 'max': 127.3999938964844, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1004PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Float, 'idx': 31, 'min': 0.0, 'max': 107.5999984741211, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1005PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 32, 'min': 0.0, 'max': 109.4000015258789, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1006PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 33, 'min': 0.0, 'max': 102.1999969482422, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1007PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 34, 'min': 0.0, 'max': 111.1999969482422, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1008PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 35, 'min': 0.0, 'max': 105.7999954223633, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1009PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Double, 'idx': 36, 'min': 0.0, 'max': 105.7999954223633, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1010PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 37, 'min': 0.0, 'max': 5928.7998046875, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1011PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 38, 'min': 0.0, 'max': 215.5999908447266, 'base_value': round(random.uniform(10, 100), 2)},
   "TC1012PumpTempSensorAI_ENG": {'alter_datatype': ua.VariantType.Double, 'idx': 39, 'min': 0.0, 'max': 111.1999969482422, 'base_value': round(random.uniform(10, 100), 2)},
   "TT1001MainWaterTemperatureAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 40, 'min': 0.0, 'max': 86.41093444824219, 'base_value': round(random.uniform(10, 100), 2)},
   "TT2001PELubeTankTempAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 41, 'min': 0.0, 'max': 121.0767364501953, 'base_value': round(random.uniform(10, 100), 2)},
   "TT2002PELubeSupplyTempAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 42, 'min': 0.0, 'max': 121.2526016235352, 'base_value': round(random.uniform(10, 100), 2)},
   "CV1002ChokeValvePositionSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 43, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "CV1002ChokeValveStop": {'alter_datatype': ua.VariantType.Int32, 'idx': 44, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "CV1001ChokeValveStop": {'alter_datatype': ua.VariantType.Float, 'idx': 45, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "CV1001ChokeValvePositionSetpoint": {'alter_datatype': ua.VariantType.Double, 'idx': 46, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1002ChargePumpMotorStop": {'alter_datatype': ua.VariantType.Int32, 'idx': 47, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2001LL_AlarmSetpoint": {'alter_datatype': ua.VariantType.String, 'idx': 48, 'min': 0.0, 'max': 65.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1001H_AlarmSetpoint": {'alter_datatype': ua.VariantType.Boolean, 'idx': 49, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1002H_AlarmSetpoint": {'alter_datatype': ua.VariantType.Boolean, 'idx': 50, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1003H_AlarmSetpoint": {'alter_datatype': ua.VariantType.Float, 'idx': 51, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1004HH_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 52, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS2001L_AlarmSetpoint": {'alter_datatype': ua.VariantType.String, 'idx': 53, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LT1001L_AlarmSetpoint": {'alter_datatype': ua.VariantType.Boolean, 'idx': 54, 'min': 0.0, 'max': 100.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LT1001LL_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 55, 'min': 0.0, 'max': 60.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1001L_AlarmSetpoint": {'alter_datatype': ua.VariantType.Float, 'idx': 56, 'min': 0.0, 'max': 80.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1001LL_AlarmSetpoint": {'alter_datatype': ua.VariantType.Double, 'idx': 57, 'min': 0.0, 'max': 50.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1002HH_AlarmSetpoint": {'alter_datatype': ua.VariantType.Float, 'idx': 58, 'min': 0.0, 'max': 5000.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1003HH_AlarmSetpoint": {'alter_datatype': ua.VariantType.String, 'idx': 59, 'min': 0.0, 'max': 5000.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2001HH_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 60, 'min': 0.0, 'max': 250.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2002L_AlarmSetpoint": {'alter_datatype': ua.VariantType.Boolean, 'idx': 61, 'min': 0.0, 'max': 50.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2002LL_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 62, 'min': 0.0, 'max': 55.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT1001H_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 63, 'min': 0.0, 'max': 105.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT1001HH_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 64, 'min': 0.0, 'max': 110.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT2001H_AlarmSetpoint": {'alter_datatype': ua.VariantType.String, 'idx': 65, 'min': 0.0, 'max': 145.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT2001HH_AlarmSetpoint": {'alter_datatype': ua.VariantType.Int32, 'idx': 66, 'min': 0.0, 'max': 165.0, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2001LL_Alarm": {'alter_datatype': ua.VariantType.Int32, 'idx': 67, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1001H_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 68, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1002H_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 69, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1003H_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 70, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS1004HH_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 71, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LS2001L_Alarm": {'alter_datatype': ua.VariantType.String, 'idx': 72, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LT1001L_Alarm": {'alter_datatype': ua.VariantType.Float, 'idx': 73, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "LT1001LL_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 74, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1001L_Alarm": {'alter_datatype': ua.VariantType.Double, 'idx': 75, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1001LL_Alarm": {'alter_datatype': ua.VariantType.Int32, 'idx': 76, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1002HH_Alarm": {'alter_datatype': ua.VariantType.String, 'idx': 77, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT1003HH_Alarm": {'alter_datatype': ua.VariantType.String, 'idx': 78, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2001HH_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 79, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2002L_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 80, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2), 'base_value': round(random.uniform(10, 100), 2)},
   "PT2002LL_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 81, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT1001H_Alarm": {'alter_datatype': ua.VariantType.String, 'idx': 82, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT1001HH_Alarm": {'alter_datatype': ua.VariantType.String, 'idx': 83, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT2001H_Alarm": {'alter_datatype': ua.VariantType.Boolean, 'idx': 84, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "TT2001HH_Alarm": {'alter_datatype': ua.VariantType.String, 'idx': 85, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2002PELubePumpVFDRunCommandDO": {'alter_datatype': ua.VariantType.String, 'idx': 86, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2002PELubePumpDriveSpeedAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 87, 'min': 0.0, 'max': 1235.37060546875, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2006PELubeSupplyPressSetpointAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 88, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2006PELubeSupplyPressAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 89, 'min': 0.0, 'max': 209.7582855224609, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2005PELubeSupplyPressAI_ENG": {'alter_datatype': ua.VariantType.Int32, 'idx': 90, 'min': 0.0, 'max': 84.48954010009766, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2005PELubeSupplyPressSetpointAI_ENG": {'alter_datatype': ua.VariantType.Float, 'idx': 91, 'min': 0.0, 'max': 0.0, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2004PELubeSupplyPressAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 92, 'min': 0.0, 'max': 293.5883178710938, 'base_value': round(random.uniform(10, 100), 2)},
   "PT2003PELubeSupplyPressAI_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 93, 'min': 0.0, 'max': 300.1100463867188, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2002PELubeSupplyFlowAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 94, 'min': 0.0, 'max': 26.51929473876953, 'base_value': round(random.uniform(10, 100), 2)},
   "D2003PELubeCoolerManualSpeedValue": {'alter_datatype': ua.VariantType.Int32, 'idx': 95, 'min': 0.0, 'max': 1.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2002PELubePumpMtr2ManualSpeedValue": {'alter_datatype': ua.VariantType.Int32, 'idx': 96, 'min': 0.0, 'max': 8.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D1001MotorEff": {'alter_datatype': ua.VariantType.Float, 'idx': 97, 'min': 0.0, 'max': 100.0, 'base_value': round(random.uniform(10, 100), 2)},
   "D2001PELubePumpDriveEff": {'alter_datatype': ua.VariantType.String, 'idx': 98, 'min': 0.0, 'max': 111867.6015625, 'base_value': round(random.uniform(10, 100), 2)},
   "D2002PELubePumpDriveEff": {'alter_datatype': ua.VariantType.Boolean, 'idx': 99, 'min': 0.0, 'max': 3931.418212890625, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2001PELubeDriveCalculatedFlowrate_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 100, 'min': 0.0, 'max': 6.774921875, 'base_value': round(random.uniform(10, 100), 2)},
   "FT1001MainLoopCalculatedFlowrateAI_ENG": {'alter_datatype': ua.VariantType.String, 'idx': 101, 'min': 0.0, 'max': 4.9226568603515, 'base_value': round(random.uniform(10, 100), 2)},
   "FT2002PELubeDriveCalculatedFlowrate_ENG": {'alter_datatype': ua.VariantType.Boolean, 'idx': 102, 'min': 0.0, 'max': 3.187256240844, 'base_value': round(random.uniform(10, 100), 2)}
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
                'D1001VFDStop': ua.VariantType.Double, 'D1001VFDStopSpeedSetpoint': ua.VariantType.Double
            },
            "PE_Lube_Tags": {
                'D2001PELubePumpMtr1Stop': ua.VariantType.Double, 'D2003PELubeCoolerManualSpeedValue': ua.VariantType.Double,
                'D2002PELubePumpMtr2ManualSpeedValue': ua.VariantType.Double
            },
            "Outputs": {
                'D1001DriveRunCommandDO': ua.VariantType.Double, 'D1001DriveSpeedReferenceAO_ENG': ua.VariantType.Double,
                'D1002ChargePumpDriveSpeedReferenceAO_ENG': ua.VariantType.Double, 'D2001PELubePumpDriveSpeedReferenceAO_ENG': ua.VariantType.Double,
                'D1002ChargePumpVFDRunCommandDO': ua.VariantType.Double, 'D2001PELubePumpVFDRunCommandDO': ua.VariantType.Double,
                'D2002PELubePumpVFDRunCommandDO': ua.VariantType.Double
            },
            "Inputs": {
                'CV1001PositionFeedbackAI_ENG': ua.VariantType.Double, 'CV1002PositionFeedbackAI_ENG': ua.VariantType.Double,
                'D1001MotorSpeedAI_ENG': ua.VariantType.Float, 'D1001MotorTorqueAI_ENG': ua.VariantType.Float,
                'D1002ChargePumpSpeedAI_ENG': ua.VariantType.Float, 'D1002ChargePumpTorqueAI_ENG': ua.VariantType.Double,
                'D2001PELubePumpDriveSpeedAI_ENG': ua.VariantType.Float, 'FT1001MainLoopFlowrateAI_ENG': ua.VariantType.Float,
                'FT2001PELubeSupplyFlowAI_ENG': ua.VariantType.Float, 'FT2001PELubeSupplyFlowSetpoint_ENG': ua.VariantType.Double,
                'LT1001MainWaterTankLevelAI_ENG': ua.VariantType.Float, 'PT1001MaingPumpChargePressAI_ENG': ua.VariantType.Float,
                'PT1002MainPumpDischargePressAI_ENG': ua.VariantType.Float, 'PT1003MainPumpDischargePressAI_ENG': ua.VariantType.Float,
                'PT1004ChokeCV1002PressAI_ENG': ua.VariantType.Double, 'PT2001PELubeSupplyPressAI_ENG': ua.VariantType.Float,
                'PT2001PELubeSupplyPressSetpoint_ENG': ua.VariantType.Double, 'PT2002PELubeSupplyPressAI_ENG': ua.VariantType.Float,
                'PT2002PELubeSupplyPressSetpoint_ENG': ua.VariantType.Double, 'TC1001PumpTempSensorAI_ENG': ua.VariantType.Float,
                'TC1002PumpTempSensorAI_ENG': ua.VariantType.Double, 'TC1003PumpTempSensorAI_ENG': ua.VariantType.Float,
                'TC1004PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1005PumpTempSensorAI_ENG': ua.VariantType.Float,
                'TC1006PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1007PumpTempSensorAI_ENG': ua.VariantType.Float,
                'TC1008PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1009PumpTempSensorAI_ENG': ua.VariantType.Float,
                'TC1010PumpTempSensorAI_ENG': ua.VariantType.Float, 'TC1011PumpTempSensorAI_ENG': ua.VariantType.Float,
                'TC1012PumpTempSensorAI_ENG': ua.VariantType.Float, 'TT1001MainWaterTemperatureAI_ENG': ua.VariantType.Float,
                'TT2001PELubeTankTempAI_ENG': ua.VariantType.Float, 'TT2002PELubeSupplyTempAI_ENG': ua.VariantType.Float,
                'D2002PELubePumpDriveSpeedAI_ENG': ua.VariantType.Float, 'PT2006PELubeSupplyPressSetpointAI_ENG': ua.VariantType.Double,
                'PT2006PELubeSupplyPressAI_ENG': ua.VariantType.Float, 'PT2005PELubeSupplyPressAI_ENG': ua.VariantType.Float,
                'PT2005PELubeSupplyPressSetpointAI_ENG': ua.VariantType.Double, 'PT2004PELubeSupplyPressAI_ENG': ua.VariantType.Float,
                'PT2003PELubeSupplyPressAI_ENG': ua.VariantType.Float, 'FT2002PELubeSupplyFlowAI_ENG': ua.VariantType.Float,
                'D1001MotorEff': ua.VariantType.Double, 'D2001PELubePumpDriveEff': ua.VariantType.Float, 'D2002PELubePumpDriveEff': ua.VariantType.Float,
                'FT2001PELubeDriveCalculatedFlowrate_ENG': ua.VariantType.Float, 'FT1001MainLoopCalculatedFlowrateAI_ENG': ua.VariantType.Float,
                'FT2002PELubeDriveCalculatedFlowrate_ENG': ua.VariantType.Float
            },
            "CHOKE_TAGS": {
                'CV1002ChokeValvePositionSetpoint': ua.VariantType.Double, 'CV1002ChokeValveStop': ua.VariantType.Double,
                'CV1001ChokeValveStop': ua.VariantType.Double, 'CV1001ChokeValvePositionSetpoint': ua.VariantType.Double
            },
            "CHARGE_PUMP_TAGS": {
                'D1002ChargePumpMotorStop': ua.VariantType.Double
            },
            "ALARM_TAGS": {
                'FT2001LL_AlarmSetpoint': ua.VariantType.Double, 'LS1001H_AlarmSetpoint': ua.VariantType.Double,
                'LS1002H_AlarmSetpoint': ua.VariantType.Double, 'LS1003H_AlarmSetpoint': ua.VariantType.Double,
                'LS1004HH_AlarmSetpoint': ua.VariantType.Double, 'LS2001L_AlarmSetpoint': ua.VariantType.Double,
                'LT1001L_AlarmSetpoint': ua.VariantType.Double, 'LT1001LL_AlarmSetpoint': ua.VariantType.Double,
                'PT1001L_AlarmSetpoint': ua.VariantType.Double, 'PT1001LL_AlarmSetpoint': ua.VariantType.Double,
                'PT1002HH_AlarmSetpoint': ua.VariantType.Double, 'PT1003HH_AlarmSetpoint': ua.VariantType.Double,
                'PT2001HH_AlarmSetpoint': ua.VariantType.Double, 'PT2002L_AlarmSetpoint': ua.VariantType.Double,
                'PT2002LL_AlarmSetpoint': ua.VariantType.Double, 'TT1001H_AlarmSetpoint': ua.VariantType.Double,
                'TT1001HH_AlarmSetpoint': ua.VariantType.Double, 'TT2001H_AlarmSetpoint': ua.VariantType.Double,
                'TT2001HH_AlarmSetpoint': ua.VariantType.Double, 'FT2001LL_Alarm': ua.VariantType.Double,
                'LS1001H_Alarm': ua.VariantType.Double, 'LS1002H_Alarm': ua.VariantType.Double, 'LS1003H_Alarm': ua.VariantType.Double,
                'LS1004HH_Alarm': ua.VariantType.Double, 'LS2001L_Alarm': ua.VariantType.Double, 'LT1001L_Alarm': ua.VariantType.Double,
                'LT1001LL_Alarm': ua.VariantType.Double, 'PT1001L_Alarm': ua.VariantType.Double, 'PT1001LL_Alarm': ua.VariantType.Double,
                'PT1002HH_Alarm': ua.VariantType.Double, 'PT1003HH_Alarm': ua.VariantType.Double, 'PT2001HH_Alarm': ua.VariantType.Double,
                'PT2002L_Alarm': ua.VariantType.Double, 'PT2002LL_Alarm': ua.VariantType.Double, 'TT1001H_Alarm': ua.VariantType.Double,
                'TT1001HH_Alarm': ua.VariantType.Double, 'TT2001H_Alarm': ua.VariantType.Double, 'TT2001HH_Alarm': ua.VariantType.Double
            }
        }

        if is_advanced is True:
            for tag in self.tag_hierarchy:
                for index in self.tag_hierarchy[tag]:
                    if index in IDX_VARIABLES:
                        self.tag_hierarchy[tag][index] = IDX_VARIABLES[index]['alter_datatype']

    def setup_server(self, enable_auth:bool=False, string_mode:str=ua.VariantType.Int32):
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

    def build_nodeid(self, name, parent_path="", string_mode:str=ua.VariantType.Int32):
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

    def add_variables(self, parent_obj, tag_dict, parent_path="", string_mode: str = ua.VariantType.Int32):
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


    def create_tag_group_objects(self, global_vars, string_mode:str=ua.VariantType.Int32):
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

    def get_random_value(self, vtype, min_val, max_val, base_value=None):
        return {
            ua.VariantType.Int32: int(random.uniform(min_val, max_val)),
            ua.VariantType.Double: round(random.uniform(min_val, max_val), 2),
            ua.VariantType.Float: random.uniform(min_val, max_val),
            ua.VariantType.Boolean: random.choice([True, False]),
            ua.VariantType.String: random.choice(string.ascii_uppercase)
        }.get(vtype, None)

    def update_variable_values(self, tag_group_var_dicts, change_rate:float=1, value_change:float=None, update_base:bool=False):
        try:
            while True:
                time.sleep(change_rate)
                for tag_vars in tag_group_var_dicts.values():
                    for var, vtype in tag_vars.values():
                        min_val = IDX_VARIABLES[list(tag_vars.keys())[0]]['min']
                        max_val = IDX_VARIABLES[list(tag_vars.keys())[0]]['max']
                        if value_change is not None and (isinstance(value_change, int) or isinstance(value_change, float)):
                            min_val = IDX_VARIABLES[list(tag_vars.keys())[0]]['base_value'] * (1-value_change)
                            max_val = IDX_VARIABLES[list(tag_vars.keys())[0]]['base_value'] * (1+value_change)
                        new_val = self.get_random_value(vtype, min_val, max_val)
                        if value_change is not None and (isinstance(value_change, int) or isinstance(value_change, float)) and update_base is True:
                            IDX_VARIABLES[list(tag_vars.keys())[0]]['base_value'] = new_val
                        # if list(tag_vars.keys())[0] == 'D1001VFDStop':
                        #     print(IDX_VARIABLES[list(tag_vars.keys())[0]]['base_value'] , new_val)
                        var.set_value(new_val)
        except KeyboardInterrupt:
            print("Server stopped by user.")
        finally:
            self.server.stop()

    def run(self, enable_auth=False, string_mode:str='short', change_rate:float=1, value_change:float=None, update_base:bool=False):
        global_vars = self.setup_server(enable_auth=enable_auth, string_mode=string_mode)
        tag_group_var_dicts = self.create_tag_group_objects(global_vars, string_mode=string_mode)
        self.set_variables_writable(tag_group_var_dicts)
        self.start_server()
        self.update_variable_values(tag_group_var_dicts, change_rate=change_rate, value_change=value_change, update_base=update_base)

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
    parser.add_argument('--string-mode', choices=['int', 'short', 'long'], default='short', help='String NodeId mode')
    parser.add_argument('--change-rate', type=float, default=1, help='Frequency of how often to change the value (seconds)')
    parser.add_argument('--value-change', type=float, default=None, help='numeric value(s) change rate ({value} * 1-{value_rate}) <= {value} <=  {value} * 1+{value_rate}')
    parser.add_argument('--update-base', type=bool, nargs='?', const=True, default=False, help='when using `--value-change`, update base value')
    parser.add_argument('--enable-auth', type=bool, nargs='?', const=True, default=False, help='Enable authentication')
    parser.add_argument('--advanced-opcua', type=bool, nargs='?', const=True, default=False, help='Multiple data types, as opposed to only float values')
    args = parser.parse_args()

    args.change_rate =  abs(args.change_rate)
    if args.value_change is not None:
        args.value_change = abs(args.value_change/100) if args.value_change > 1 else abs(args.value_change)

    opcua_server = OPCUAServer(endpoint=args.opcua_conn, is_advanced=args.advanced_opcua)
    opcua_server.run(enable_auth=args.enable_auth, string_mode=args.string_mode, change_rate=abs(args.change_rate), value_change=args.value_change, update_base=args.update_base)
