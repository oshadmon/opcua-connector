{
    "VFD_CNTRL_TAGS": {
        'D1001VFDStop': "int",
        'D1001VFDStopSpeedSetpoint': "float"
    },
    "PE_Lube_Tags": {
        'D2001PELubePumpMtr1Stop': "char",
        'D2003PELubeCoolerManualSpeedValue':"bool",
         'D2002PELubePumpMtr2ManualSpeedValue': "int"
    },
    "Outputs": {
        'D1001DriveRunCommandDO': "float",
        'D1001DriveSpeedReferenceAO_ENG': "char",
        'D1002ChargePumpDriveSpeedReferenceAO_ENG': "bool",
        'D2001PELubePumpDriveSpeedReferenceAO_ENG': "int"
    },
    "Inputs": {
        'CV1001PositionFeedbackAI_ENG': "float",
        'CV1002PositionFeedbackAI_ENG': "char",
        'D1001MotorSpeedAI_ENG': "bool",
        'D1001MotorTorqueAI_ENG': "int"
    },
    "CHOKE_TAGS": {
        'CV1002ChokeValvePositionSetpoint': "float",
        'CV1002ChokeValveStop': "char"
    },
    "CHARGE_PUMP_TAGS": {
        'D1002ChargePumpMotorStop': "bool"
`   },
    "ALARM_TAGS": {
        'FT2001LL_AlarmSetpoint': "int",
        'LS1001H_AlarmSetpoint': "float",
        'LS1002H_AlarmSetpoint': "bool"
    }
}