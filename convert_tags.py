from opcua import Server, ua
from opcua.server.user_manager import UserManager
from opcua.tools import parse_args
import json

import random

with open('tags.txt', 'r') as f:
    # Split lines
    lines = f.read().strip().split("\n")

# Extract header
header = lines[0].split("\t")

# Convert to list of dicts
list_of_dicts = []
for line in lines[1:]:
    values = line.split("\t")
    entry = {header[i]: values[i] for i in range(len(header))}
    # Optional: convert numbers to int
    entry["TagIndex"] = int(entry["TagIndex"])
    entry["TagType"] = int(entry["TagType"])
    entry["TagDataType"] = int(entry["TagDataType"])
    entry['TagName'] = entry['TagName'].rsplit("\\")[-1]
    list_of_dicts.append(entry)

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

updated_idx = {}

for key in IDX_VARIABLES:
    for row in list_of_dicts:
        if row['TagName'] == key:
            updated_idx[key] = IDX_VARIABLES[key]
            break

output = "{\n"
for key in updated_idx:
    output += f"\t\'{key}\': {updated_idx[key]},\n"
output = output.rsplit(",", 1)[0] + "\n}"
print(output)
