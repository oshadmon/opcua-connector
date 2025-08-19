import os
from opcua import ua
import random

METADATAS = {
    "oil system": {
        "file": os.path.join('base_examples', 'hpu_mud_system_oil_data.v6.csv'),
        "oil_flowrate_lpm": 20,
        "oil_temp_supply_c": 45,
        "oil_pressure_kpa": 27,
        "oil_temp_cooled_c": 42
    },
    "main loop": {
        "file": os.path.join('base_examples', 'hpu_mud_system_main_loop_data.v6.csv'),
        "main_loop_flowrate_lpm": 19,
        "discharge_pressure_1_kpa": 24,
        "discharge_pressure_2_kpa": 25
    },
    "thermocouples": {
        "file": os.path.join('base_examples', 'hpu_mud_system_thermocouple_data.v6.csv'),
        'TC1001': 31, 'TC1002': 32, 'TC1003': 33, 'TC1004': 34,
        'TC1005': 35, 'TC1006': 36, 'TC1007': 37, 'TC1008': 38,
        'TC1009': 39, 'TC1010': 40, 'TC1011': 41, 'TC1012': 42
    }
}

tag_hierarchy = {
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
IDX_VARIABLES = {
    'LT1001MainWaterTankLevelAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 19, 'file': 'base_examples\\hpu_mud_system_main_loop_data.v6.csv', 'file_column': 'main_loop_flowrate_lpm'},
    'PT1001MaingPumpChargePressAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 20, 'file': 'base_examples\\hpu_mud_system_oil_data.v6.csv', 'file_column': 'oil_flowrate_lpm'},
    'PT2001PELubeSupplyPressAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 24, 'file': 'base_examples\\hpu_mud_system_main_loop_data.v6.csv', 'file_column': 'discharge_pressure_1_kpa'},
    'PT2001PELubeSupplyPressSetpoint_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 25, 'file': 'base_examples\\hpu_mud_system_main_loop_data.v6.csv', 'file_column': 'discharge_pressure_2_kpa'},
    'PT2002PELubeSupplyPressSetpoint_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 27, 'file': 'base_examples\\hpu_mud_system_oil_data.v6.csv', 'file_column': 'oil_pressure_kpa'},
    'TC1004PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 31, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1001'},
    'TC1005PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 32, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1002'},
    'TC1006PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 33, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1003'},
    'TC1007PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 34, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1004'},
    'TC1008PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 35, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1005'},
    'TC1009PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 36, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1006'},
    'TC1010PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 37, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1007'},
    'TC1011PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 38, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1008'},
    'TC1012PumpTempSensorAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 39, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1009'},
    'TT1001MainWaterTemperatureAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 40, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1010'},
    'TT2001PELubeTankTempAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 41, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1011'},
    'TT2002PELubeSupplyTempAI_ENG': {'alter_datatype':ua.VariantType.Float, 'idx': 42, 'file': 'base_examples\\hpu_mud_system_thermocouple_data.v6.csv', 'file_column': 'TC1012'},
    'CV1001ChokeValveStop': {'alter_datatype':ua.VariantType.Float, 'idx': 45, 'file': 'base_examples\\hpu_mud_system_oil_data.v6.csv', 'file_column': 'oil_temp_supply_c'}
}

NEW_IDX_VARS = {}


for root in tag_hierarchy:
    for key in tag_hierarchy[root]:
        if key in IDX_VARIABLES:
            if root not in NEW_IDX_VARS:
                NEW_IDX_VARS[root] = {}
            NEW_IDX_VARS[root][key] = tag_hierarchy[root][key]

print(NEW_IDX_VARS)