import json
import random

VAR_LIST = {}
VAR_DICT = {} 

PARAMS = [
    "VFD_CNTRL_TAGS/D1001VFDStop", "VFD_CNTRL_TAGS/D1001VFDStopSpeedSetpoint", "PE_Lube_Tags/D2001PELubePumpMtr1Stop",
    "Outputs/D1001DriveRunCommandDO", "Outputs/D1001DriveSpeedReferenceAO_ENG", 
    "Outputs/D1002ChargePumpDriveSpeedReferenceAO_ENG", "Outputs/D2001PELubePumpDriveSpeedReferenceAO_ENG",
    "Outputs/D1002ChargePumpVFDRunCommandDO", "Outputs/D2001PELubePumpVFDRunCommandDO", 
    "Inputs/CV1001PositionFeedbackAI_ENG", "Inputs/CV1002PositionFeedbackAI_ENG", "Inputs/D1001MotorSpeedAI_ENG",
    "Inputs/D1001MotorTorqueAI_ENG", "Inputs/D1002ChargePumpSpeedAI_ENG","Inputs/D1002ChargePumpTorqueAI_ENG",
    "Inputs/D2001PELubePumpDriveSpeedAI_ENG","Inputs/FT1001MainLoopFlowrateAI_ENG",
    "Inputs/FT2001PELubeSupplyFlowAI_ENG","Inputs/FT2001PELubeSupplyFlowSetpoint_ENG",
    "Inputs/LT1001MainWaterTankLevelAI_ENG","Inputs/PT1001MaingPumpChargePressAI_ENG",
    "Inputs/PT1002MainPumpDischargePressAI_ENG","Inputs/PT1003MainPumpDischargePressAI_ENG",
    "Inputs/PT1004ChokeCV1002PressAI_ENG","Inputs/PT2001PELubeSupplyPressAI_ENG",
    "Inputs/PT2001PELubeSupplyPressSetpoint_ENG","Inputs/PT2002PELubeSupplyPressAI_ENG",
    "Inputs/PT2002PELubeSupplyPressSetpoint_ENG","Inputs/TC1001PumpTempSensorAI_ENG","Inputs/TC1002PumpTempSensorAI_ENG",
    "Inputs/TC1003PumpTempSensorAI_ENG","Inputs/TC1004PumpTempSensorAI_ENG","Inputs/TC1005PumpTempSensorAI_ENG",
    "Inputs/TC1006PumpTempSensorAI_ENG","Inputs/TC1007PumpTempSensorAI_ENG","Inputs/TC1008PumpTempSensorAI_ENG",
    "Inputs/TC1009PumpTempSensorAI_ENG","Inputs/TC1010PumpTempSensorAI_ENG","Inputs/TC1011PumpTempSensorAI_ENG",
    "Inputs/TC1012PumpTempSensorAI_ENG","Inputs/TT1001MainWaterTemperatureAI_ENG","Inputs/TT2001PELubeTankTempAI_ENG",
    "Inputs/TT2002PELubeSupplyTempAI_ENG","CHOKE_TAGS/CV1002ChokeValvePositionSetpoint",
    "CHOKE_TAGS/CV1002ChokeValveStop","CHOKE_TAGS/CV1001ChokeValveStop","CHOKE_TAGS/CV1001ChokeValvePositionSetpoint",
    "CHARGE_PUMP_TAGS/D1002ChargePumpMotorStop","ALARM_TAGS/FT2001LL_AlarmSetpoint","ALARM_TAGS/LS1001H_AlarmSetpoint",
    "ALARM_TAGS/LS1002H_AlarmSetpoint","ALARM_TAGS/LS1003H_AlarmSetpoint","ALARM_TAGS/LS1004HH_AlarmSetpoint",
    "ALARM_TAGS/LS2001L_AlarmSetpoint","ALARM_TAGS/LT1001L_AlarmSetpoint","ALARM_TAGS/LT1001LL_AlarmSetpoint",
    "ALARM_TAGS/PT1001L_AlarmSetpoint","ALARM_TAGS/PT1001LL_AlarmSetpoint","ALARM_TAGS/PT1002HH_AlarmSetpoint",
    "ALARM_TAGS/PT1003HH_AlarmSetpoint","ALARM_TAGS/PT2001HH_AlarmSetpoint","ALARM_TAGS/PT2002L_AlarmSetpoint",
    "ALARM_TAGS/PT2002LL_AlarmSetpoint","ALARM_TAGS/TT1001H_AlarmSetpoint","ALARM_TAGS/TT1001HH_AlarmSetpoint",
    "ALARM_TAGS/TT2001H_AlarmSetpoint","ALARM_TAGS/TT2001HH_AlarmSetpoint","ALARM_TAGS/FT2001LL_Alarm",
    "ALARM_TAGS/LS1001H_Alarm","ALARM_TAGS/LS1002H_Alarm","ALARM_TAGS/LS1003H_Alarm","ALARM_TAGS/LS1004HH_Alarm",
    "ALARM_TAGS/LS2001L_Alarm","ALARM_TAGS/LT1001L_Alarm","ALARM_TAGS/LT1001LL_Alarm","ALARM_TAGS/PT1001L_Alarm",
    "ALARM_TAGS/PT1001LL_Alarm","ALARM_TAGS/PT1002HH_Alarm","ALARM_TAGS/PT1003HH_Alarm","ALARM_TAGS/PT2001HH_Alarm",
    "ALARM_TAGS/PT2002L_Alarm","ALARM_TAGS/PT2002LL_Alarm","ALARM_TAGS/TT1001H_Alarm","ALARM_TAGS/TT1001HH_Alarm",
    "ALARM_TAGS/TT2001H_Alarm","ALARM_TAGS/TT2001HH_Alarm","Outputs/D2002PELubePumpVFDRunCommandDO",
    "Inputs/D2002PELubePumpDriveSpeedAI_ENG","Inputs/PT2006PELubeSupplyPressSetpointAI_ENG",
    "Inputs/PT2006PELubeSupplyPressAI_ENG","Inputs/PT2005PELubeSupplyPressAI_ENG",
    "Inputs/PT2005PELubeSupplyPressSetpointAI_ENG","Inputs/PT2004PELubeSupplyPressAI_ENG",
    "Inputs/PT2003PELubeSupplyPressAI_ENG","Inputs/FT2002PELubeSupplyFlowAI_ENG",
    "PE_Lube_Tags/D2003PELubeCoolerManualSpeedValue","PE_Lube_Tags/D2002PELubePumpMtr2ManualSpeedValue",
    "Inputs/D1001MotorEff","Inputs/D2001PELubePumpDriveEff","Inputs/D2002PELubePumpDriveEff",
    "Inputs/FT2001PELubeDriveCalculatedFlowrate_ENG","Inputs/FT1001MainLoopCalculatedFlowrateAI_ENG",
    "Inputs/FT2002PELubeDriveCalculatedFlowrate_ENG]"
]

for param in PARAMS: 
    key, value = param.split("/")
    if key not in VAR_DICT:
        VAR_DICT[key] = {}
    VAR_DICT[key][value] = 'float'

    if value not in VAR_LIST:
        VAR_LIST[value] = random.choice(['int', 'float', 'char', 'bool'])
    else:
        print(value)

print(json.dumps(VAR_DICT, indent=2))
print(json.dumps(VAR_LIST, indent=2))

for key in ['int', 'float', 'char', 'bool']:
    print(key, list(VAR_LIST.values()).count(key))
