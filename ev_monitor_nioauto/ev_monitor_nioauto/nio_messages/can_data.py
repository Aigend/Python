CAN_DATA = {
    '628': {
        'msg_id': 628,
        "value": b'\x00\x00\x00\x00\xc0\x0f\x00\x10',
        "pasted_value": '{"CSC_Com_Index":0,"Hazard2_Performance_Index":0,' \
                        '"CTD_MainP_Index":0,"CVT_Performance_Index":0,"BCV_Current_Performance_Index":0,' \
                        '"CBL_Circutry_Index":0,"CTD_MainN_Index":0,"PDCAN_Timeout_Index":0,"Hazard3_Performance_Index":0,' \
                        '"BCV_Voltage_Performance_Index":0,"SOH_Performance_Index":0,"ISO_Performance_Index":0,' \
                        '"Crash_Performance_Index":0,"OBC_Com_Index":3,"OBC_Performance_Index":3,"Hazard4_Performance_Index":0,' \
                        '"Hazard6_Performance_Index":0,"CSC_Circuitry_Index":0,"Hazard1_Performance_Index":0,"HVIL_Circuitry_Index":0,' \
                        '"BCV_Current_Com_Index":0,"SOF_Performance_Index":0,"SOC_Performance_Index":0,"CTM_Performance_Index":0,' \
                        '"FCC_Performance_Index":3,"PTCAN_Timeout_Index":0,"THM_Performance":0,"CTD_Pre_Index":0,' \
                        '"Hazard5_Performance_Index":0,"Reserved_8":1,"Reserved_7":0}'

    },
    '578': {
        'msg_id': 578,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': '{"VCUHVDCDCMdReq":0,"VCUReqOutputVoltg":0.0,"VCUReqOutputCrrnt":0.0}'
    },
    '624': {
        'msg_id': 624,
        'value': b'\x00\x00\x00\x00\x00\x00\x0F\xA0',
        'pasted_value': '{"BMSBatteryRatedVoltage":0.0,"BMSDCChargingCurrentMeasurement":0.0,"BMSReadyDCCharging":0,"BMSDCChargingVoltageMeasurement":0.0}'
    },
    '850': {
        'msg_id': 850,
        'value': b'\x68\x00\x50\x00\x00',
        'pasted_value': '{"LVBattSOCSts":0,"VCULvBattWarn":0,"LVBattUSts":1,"LVBattSOC":80,"LVBattChgSts":0,"LVBattU":13.000005,"LoadShed":0,"VCUHVBattCutOffWarn":0}'
    },
    '851': {
        'msg_id': 851,
        'value': b'\x00\x00\x00\x28\x00\x00\x40\x00',
        'pasted_value': '{"HVBattPreEstimdTi":0,"LVBattChrgWakeUp":0, "HVBattRejectReason":0,"LVBattI":0,"LVBattISts":0,"LVBattT":0,"LVBattSOHSts":0,"LVBattDchaWakeUpSts":0,"LVBattSOCWakeUpSts":1,"LVBattSOH":0,"LVBattTSts":0,"LVBattChrgWakeUpSts":0,"LVBattSOCWakeUp":0,"LVBattIRng":0,"LVBattDchaWakeUp":0,"HVBattPreSts":0}'
    },
    '852': {
        'msg_id': 852,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': '{"LVBattSOHLAMSts":0,"LVBattCustomerID":0,"LVBattSOHSUL":0,"LVBattSOHSULSts":0,"LVBattSOHLAM":0.0,"LVBattSOHCORSts":0,"LVBattSOHCOR":0.0,"VCURemainingRng2":0.0,"VehElecCns1":0.0,"VehElecCns2":0.0}'
    },
    '173': {
        'msg_id': 173,
        'value': b'\x32\x85\x50\x20\x2A\x20\x00\x00',
        'pasted_value': '{"BMSAlarmClockStatus":0,"BMSDCChrgDerateCrrntSts":0,"BMSIsolationLvl":1,"BMSBalanceSts":0,"BMSChrgState":0,"BMSDischgCrrntLimit":1293.3,"BMSFaultCat":0,"BMSVoltgLimitMax":412.8,"BMSInterlockStatus":1,"BMSVoltgLimitMin":259.2}'
    },
    '883': {
        'msg_id': 883,
        'value': b'\x82\x80\x80\x82\x00\xA0\x00\x02',
        'pasted_value': '{"BMSESSInletTempValidity":0,"BMSESSInletTemp":24.0,"BMSESSOutletTempValidity":0,"BMSESSOutletTempMask":1,"BMSESSOutletTemp":24.0,"BMSTempAverage":24.0,"BMSTempMin":24.0,"BMSTempAverageValidity":0,"BMSHVShutdownReq":0,"BMSTempMax":25.0,"BMSTempMaxValidity":0,"BMSESSInletTempMask":1,"BMSTempMinValidity":0,"BMSCellTarTempVld":0,"Msg373Rsvd1":0,"BMSCellTarTemp":-9.0,"Msg373Rsvd2":0,"ReflashReq":0}'
    },
    '616': {
        'msg_id': 616,
        'value': b'\x16\x2D\x06\x2B\x16\x2D\x94\x99',
        'pasted_value': '{"BMSDischrgPowerLimitST":567.7,"BMSDischrgPowerLimitLT":157.9,"BMSDischrgPowerLimitDynamic":567.7,"BMSInsulationResistanceValue":38041}'
    },
    '617': {
        'msg_id': 617,
        'value': b'\x0F\x40\x0F\x32\x05\xA1\x0F\x3B',
        'pasted_value': '{"BMSEstimateChrgTime":1441,"BMSCellVoltgAverageValidity":0,"BMSCellVoltgMaxValidity":0,"BMSCellVoltgMin":3.89,"BMSCellVoltgMax":3.904,"BMSCellVoltgAverage":3.899,"BMSCellVoltgMinValidity":0}'
    },
    '618': {
        'msg_id': 618,
        'value': b'\x07\xBB\x02\xBA\x07\xBB\x00\x00',
        'pasted_value': '{"BMSChrgPowerLimitLT":69.8,"BMSChrgPowerLimitST":197.9,"BMSChrgPowerLimitDynamic":197.9,"BMSEstimatePercChrgTime":0}'
    },
    '623': {
        'msg_id': 623,
        'value': b'\x00\x02\x14\x06\x23\x10\x11\x02',
        'pasted_value': '{"BMSBatteryPackCap":0,"BMSBatteryRatedCapacity":435.4,"BMSBatteryType":6, "BMSMaxPermitDCChargeVoltage":897.6,"BMSProtocalVersion":532}'
    }
}


CAN_DATA_V74 = {
    '851': {
        'msg_id': 851,
        'value': b'\x00\x00\x00\x28\x00\x00\x40\x00',
        'pasted_value': '{"HVBattPreEstimdTi":0,"LVBattChrgWakeUp":0,"LVBattI":0,"LVBattISts":0,"LVBattT":0,"LVBattSOHSts":0,"LVBattDchaWakeUpSts":0,"LVBattSOCWakeUpSts":1,"LVBattSOH":0,"LVBattTSts":0,"LVBattChrgWakeUpSts":0,"LVBattSOCWakeUp":0,"LVBattIRng":0,"LVBattDchaWakeUp":0,"HVBattPreSts":0}'
    },
    '852': {
        'msg_id': 852,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': '{"LVBattSOHLAMSts":0,"LVBattCustomerID":0,"LVBattSOHSUL":0,"LVBattSOHSULSts":0,"LVBattSOHLAM":0.0,"LVBattSOHCORSts":0,"LVBattSOHCOR":0.0}'
    },
    '173': {
        'msg_id': 173,
        'value': b'\x32\x85\x50\x20\x2A\x20\x00\x00',
        'pasted_value': '{"BMSAlarmClockStatus":0,"BMSIsolationLvl":1,"BMSBalanceSts":0,"BMSChrgState":0,"BMSDischgCrrntLimit":1293.3,"BMSFaultCat":0,"BMSVoltgLimitMax":412.8,"BMSInterlockStatus":1,"BMSVoltgLimitMin":259.2}'
    },
    '883': {
        'msg_id': 883,
        'value': b'\x82\x80\x80\x82\x00\xA0\x00\x02',
        'pasted_value': '{"BMSESSInletTempMask":1,"BMSTempMinValidity":0,"BMSESSInletTempValidity":0,"BMSESSInletTemp":24.0,"BMSESSOutletTempValidity":0,"BMSESSOutletTempMask":1,"BMSESSOutletTemp":24.0,"BMSTempAverage":24.0,"BMSTempMin":24.0,"BMSTempAverageValidity":0,"BMSHVShutdownReq":0,"BMSTempMax":25.0,"BMSTempMaxValidity":0,"BMSCellTempStandardDeviation":0.2}'
    },
    '618': {
        'msg_id': 618,
        'value': b'\x07\xBB\x02\xBA\x07\xBB\x00\x00',
        'pasted_value': '{"BMSChrgPowerLimitLT":69.8,"BMSChrgPowerLimitST":197.9,"BMSChrgPowerLimitDynamic":197.9}'
    },
}


CAN_DATA_ES8_754 = {
    '628': {
        'msg_id': 628,
        "value": b'\x00\x00\x00\x00\xc0\x0f\x00\x10',
        "pasted_value": '{"CSC_Com_Index":0,"Hazard2_Performance_Index":0,' \
                        '"CTD_MainP_Index":0,"CVT_Performance_Index":0,"BCV_Current_Performance_Index":0,' \
                        '"CBL_Circutry_Index":0,"CTD_MainN_Index":0,"PDCAN_Timeout_Index":0,"Hazard3_Performance_Index":0,' \
                        '"BCV_Voltage_Performance_Index":0,"SOH_Performance_Index":0,"ISO_Performance_Index":0,' \
                        '"Crash_Performance_Index":0,"OBC_Com_Index":3,"OBC_Performance_Index":3,"Hazard4_Performance_Index":0,' \
                        '"Hazard6_Performance_Index":0,"CSC_Circuitry_Index":0,"Hazard1_Performance_Index":0,"HVIL_Circuitry_Index":0,' \
                        '"BCV_Current_Com_Index":0,"SOF_Performance_Index":0,"SOC_Performance_Index":0,"CTM_Performance_Index":0,' \
                        '"FCC_Performance_Index":3,"PTCAN_Timeout_Index":0,"THM_Performance":0,"BMSUploadSts":0,"CTD_Pre_Index":0,' \
                        '"Reserved_8":1,"Reserved_7":0}'
    },
    '883': {
        'msg_id': 883,
        'value': b'\x82\x80\x80\x82\x00\xA0\x00\x02',
        'pasted_value': '{"BMSESSInletTempMask":1,"BMSTempMinValidity":0,"BMSESSInletTempValidity":0,"BMSESSInletTemp":24.0,"BMSESSOutletTempValidity":0,"BMSESSOutletTempMask":1,"BMSESSOutletTemp":24.0,"BMSTempAverage":24.0,"BMSTempMin":24.0,"BMSTempAverageValidity":0,"BMSHVShutdownReq":0,"BMSTempMax":25.0,"BMSTempMaxValidity":0,"BMSCellTempStandardDeviation":0.2}'
    }
}

CAN_DATA_ES8_757 = {
    '628': {
        'msg_id': 628,
        "value": b'\x00\x00\x00\x00\xc0\x0f\x00\x10',
        "pasted_value": '{"CSC_Com_Index":0,"Hazard2_Performance_Index":0,' \
                        '"CTD_MainP_Index":0,"CVT_Performance_Index":0,"BCV_Current_Performance_Index":0,' \
                        '"CBL_Circutry_Index":0,"CTD_MainN_Index":0,"PDCAN_Timeout_Index":0,"Hazard3_Performance_Index":0,' \
                        '"BCV_Voltage_Performance_Index":0,"SOH_Performance_Index":0,"ISO_Performance_Index":0,' \
                        '"Crash_Performance_Index":0,"OBC_Com_Index":3,"OBC_Performance_Index":3,"Hazard4_Performance_Index":0,' \
                        '"Hazard6_Performance_Index":0,"CSC_Circuitry_Index":0,"Hazard1_Performance_Index":0,"HVIL_Circuitry_Index":0,' \
                        '"BCV_Current_Com_Index":0,"SOF_Performance_Index":0,"SOC_Performance_Index":0,"CTM_Performance_Index":0,' \
                        '"FCC_Performance_Index":3,"PTCAN_Timeout_Index":0,"THM_Performance":0,"BMSUploadSts":0,"CTD_Pre_Index":0,' \
                        '"Reserved_8":1,"Reserved_7":0}'
    },
    '883': {
        'msg_id': 883,
        'value': b'\x82\x80\x80\x82\x00\xA0\x00\x02',
        'pasted_value': '{"BMSESSInletTempMask":1,"BMSTempMinValidity":0,"BMSESSInletTempValidity":0,"BMSESSInletTemp":24.0,'
                        '"BMSESSOutletTempValidity":0,"BMSESSOutletTempMask":1,"BMSESSOutletTemp":24.0,"BMSTempAverage":24.0,'
                        '"BMSTempMin":24.0,"BMSTempAverageValidity":0,"BMSHVShutdownReq":0,"BMSTempMax":25.0,"BMSTempMaxValidity":0,'
                        '"BMSCellTarTemp":-9.0,"BMSCellTarTempVld":0,"BMS_OverDcgChrgProtect":0,"Msg373Rsvd2":0,"ReflashReq":0}'
    }
}

CAN_DATA_ES8_759 = {
    '739': {
        'msg_id': 739,
        "value": b'\x00\x0f\x00\x00',
        "pasted_value": '{"MATE_NOMI_ProId":0,"MATE_NOMI_Sts":0,'
                        '"MATE_NOMI_CarWshngSts":0,"MATE_NOMI_BackLiSts":15,"MATE_NOMI_WarningRsp":0,'
                        '"MateCalSts":0}'
    },
    '543': {
        'msg_id': 543,
        'value': b'\x00\x00\x00\x80',
        'pasted_value': '{"TripEng":0.0,"RealEngCsp":-100.0,"TqRatio":80}'
    }
}

CAN_DATA_ES6_307 = {
    '628': {
        'msg_id': 628,
        "value": b'\x00\x00\x00\x00\xc0\x0f\x00\x10',
        "pasted_value": '{"CSC_Com_Index":0,"Hazard2_Performance_Index":0,'
                        '"CTD_MainP_Index":0,"CVT_Performance_Index":0,"BCV_Current_Performance_Index":0,'
                        '"CBL_Circutry_Index":0,"CTD_MainN_Index":0,"PDCAN_Timeout_Index":0,"Hazard3_Performance_Index":0,'
                        '"BCV_Voltage_Performance_Index":0,"SOH_Performance_Index":0,"ISO_Performance_Index":0,'
                        '"Crash_Performance_Index":0,"OBC_Com_Index":3,"OBC_Performance_Index":3,"Hazard4_Performance_Index":0,'
                        '"Hazard6_Performance_Index":0,"CSC_Circuitry_Index":0,"Hazard1_Performance_Index":0,"HVIL_Circuitry_Index":0,'
                        '"BCV_Current_Com_Index":0,"SOF_Performance_Index":0,"SOC_Performance_Index":0,"CTM_Performance_Index":0,'
                        '"FCC_Performance_Index":3,"PTCAN_Timeout_Index":0,"THM_Performance":0,"Hazard5_Performance_Index":0,'
                        '"Reserved_7":0,"Reserved_8":1,"CTD_Pre_Index":0}'
    },
    '883': {
        'msg_id': 883,
        'value': b'\x82\x80\x80\x82\x00\xA0\x00\x02',
        'pasted_value': '{"BMSESSInletTempMask":1,"BMSTempMinValidity":0,"BMSESSInletTempValidity":0,"BMSESSInletTemp":24.0,'
                        '"BMSESSOutletTempValidity":0,"BMSESSOutletTempMask":1,"BMSESSOutletTemp":24.0,"BMSTempAverage":24.0,"BMSTempMin":24.0,'
                        '"BMSTempAverageValidity":0,"BMSHVShutdownReq":0,"BMSTempMax":25.0,"BMSTempMaxValidity":0,"BMS_OverDcgChrgProtect":0,'
                        '"Msg373Rsvd2":0,"ReflashReq":0,"BMSCellTarTemp":-9.0,"BMSCellTarTempVld":0}'
    }
}

CAN_DATA_ES6_309 = {
    '1959': {
        'msg_id': 1959,
        "value": b'\x07\x06\x05\x04\x03\x02\x01\x00',
        'pasted_value': '{"XcpRespData0_EPB2":7,"XcpRespData1_EPB2":6,"XcpRespData2_EPB2":5,"XcpRespData3_EPB2":4,'
                        '"XcpRespData4_EPB2":3,"XcpRespData5_EPB2":2,"XcpRespData6_EPB2":1,"XcpRespData7_EPB2":0}'
    },
    '1941': {
        'msg_id': 1941,
        'value': b'\x00\x01\x02\x03\x04\x05\x06\x07',
        'pasted_value': '{"XcpRespData0_EPB1":0,"XcpRespData1_EPB1":1,"XcpRespData2_EPB1":2,"XcpRespData3_EPB1":3,'
                        '"XcpRespData4_EPB1":4,"XcpRespData5_EPB1":5,"XcpRespData6_EPB1":6,"XcpRespData7_EPB1":7}'
    }
}

CAN_DATA_VMS = {
    '60': {
        'msg_id': 60,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '61': {
        'msg_id': 61,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '62': {
        'msg_id': 62,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '68': {
    #     'msg_id': 68,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': '{"BMSBatteryPackCap":0}'
    # },
    '69': {
        'msg_id': 69,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '70': {
        'msg_id': 70,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '71': {
        'msg_id': 71,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '72': {
        'msg_id': 72,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '80': {
        'msg_id': 80,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '88': {
        'msg_id': 88,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '89': {
        'msg_id': 89,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '91': {
        'msg_id': 91,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '92': {
    #     'msg_id': 92,
    #     'value': b'\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '94': {
        'msg_id': 94,
        'value': b'\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '95': {
    #     'msg_id': 95,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '116': {
        'msg_id': 116,
        'value': b'\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '117': {
    #     'msg_id': 117,
    #     'value': b'\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '132': {
        'msg_id': 132,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '133': {
        'msg_id': 133,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '140': {
        'msg_id': 140,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '141': {
        'msg_id': 141,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '148': {
        'msg_id': 148,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '149': {
        'msg_id': 149,
        'value': b'\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '172': {
        'msg_id': 172,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '173': {
        'msg_id': 173,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '174': {
        'msg_id': 174,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '175': {
    #     'msg_id': 175,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '204': {
        'msg_id': 204,
        'value': b'\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '431': {
        'msg_id': 431,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '535': {
        'msg_id': 535,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '537': {
        'msg_id': 537,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '538': {
        'msg_id': 538,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '539': {
        'msg_id': 539,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '542': {
    #     'msg_id': 542,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    # '575': {
    #     'msg_id': 575,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '576': {
        'msg_id': 576,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '578': {
        'msg_id': 578,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '583': {
    #     'msg_id': 583,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '584': {
        'msg_id': 584,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '591': {
        'msg_id': 591,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '615': {
        'msg_id': 615,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '616': {
        'msg_id': 616,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '617': {
        'msg_id': 617,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '618': {
        'msg_id': 618,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '619': {
        'msg_id': 619,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '620': {
        'msg_id': 620,
        'value': b'\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '623': {
        'msg_id': 623,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '624': {
        'msg_id': 624,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '625': {
        'msg_id': 625,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '626': {
        'msg_id': 626,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '627': {
        'msg_id': 627,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '628': {
        'msg_id': 628,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '638': {
        'msg_id': 638,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '654': {
        'msg_id': 654,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '655': {
        'msg_id': 655,
        'value': b'\x00\x00',
        'pasted_value': ''
    },
    '686': {
        'msg_id': 686,
        'value': b'\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '720': {
        'msg_id': 720,
        'value': b'\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '770': {
        'msg_id': 770,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '784': {
        'msg_id': 784,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '785': {
        'msg_id': 785,
        'value': b'\x00\x00\x00',
        'pasted_value': ''
    },
    '786': {
        'msg_id': 786,
        'value': b'\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '788': {
        'msg_id': 788,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '850': {
        'msg_id': 850,
        'value': b'\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '851': {
        'msg_id': 851,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '852': {
        'msg_id': 852,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': '{"LVBattSOHLAMSts":0,"LVBattCustomerID":0,"LVBattSOHSUL":0,"LVBattSOHSULSts":0,"LVBattSOHLAM":0.0,"LVBattSOHCORSts":0,"LVBattSOHCOR":0.0}'
    },
    # '856': {
    #     'msg_id': 856,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '883': {
        'msg_id': 883,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '882': {
        'msg_id': 882,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '898': {
        'msg_id': 898,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '905': {
        'msg_id': 905,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '921': {
        'msg_id': 921,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '938': {
        'msg_id': 938,
        'value': b'\x00\x00\x00',
        'pasted_value': ''
    },
    '946': {
        'msg_id': 946,
        'value': b'\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '959': {
        'msg_id': 959,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    # '1033': {
    #     'msg_id': 1033,
    #     'value': b'\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    # '1034': {
    #     'msg_id': 1034,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    # '1035': {
    #     'msg_id': 1035,
    #     'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    #     'pasted_value': ''
    # },
    '1216': {
        'msg_id': 1216,
        'value': b'\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },
    '1582': {
        'msg_id': 1582,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
        'pasted_value': ''
    },

}




CAN_DATA_NO_PASTE = {
    '628': {
        'msg_id': 628,
        "value": b'\x00\x00\x00\x00\xc0\x0f\x00\x10',

    },
    '578': {
        'msg_id': 578,
        'value': b'\x00\x00\x00\x00',
    },
    '624': {
        'msg_id': 624,
        'value': b'\x00\x00\x00\x00\x00\x00\x0F\xA0',
    },
    '850': {
        'msg_id': 850,
        'value': b'\x68\x00\x50\x00\x00',
    },
    '851': {
        'msg_id': 851,
        'value': b'\x00\x00\x00\x28\x00\x00\x40\x00',
    },
    '852': {
        'msg_id': 852,
        'value': b'\x00\x00\x00\x00\x00\x00\x00\x00',
    },
    '173': {
        'msg_id': 173,
        'value': b'\x32\x85\x50\x20\x2A\x20\x00\x00',
    },
    '883': {
        'msg_id': 883,
        'value': b'\x82\x80\x80\x82\x00\xA0\x00\x02',
    },
    '616': {
        'msg_id': 616,
        'value': b'\x16\x2D\x06\x2B\x16\x2D\x94\x99',
    },
    '617': {
        'msg_id': 617,
        'value': b'\x0F\x40\x0F\x32\x05\xA1\x0F\x3B',
    },
    '618': {
        'msg_id': 618,
        'value': b'\x07\xBB\x02\xBA\x07\xBB\x00\x00',
    },
    '615': {
        'msg_id': 615,
        'value': '0000000000000000',
    },
    '619': {
        'msg_id': 619,
        'value': '0000000000000000',
    },
    '620': {
        'msg_id': 620,
        'value': '00000000000000',
    },
    '884': {
        'msg_id': 884,
        'value': '00000000000000',
    },
    '591': {
        'msg_id': 591,
        'value': '00000000',
    },
    '91': {
        'msg_id': 91,
        'value': '0000000000000000',
    },
    '720': {
        'msg_id': 720,
        'value': '00000000',
    },
    '432': {
        'msg_id': 432,
        'value': '0000000000000000',
    },
    '701': {
        'msg_id': 701,
        'value': '0000000000000000',
    },
    '148': {
        'msg_id': 148,
        'value': '000000000000',
    },
    '62': {
        'msg_id': 62,
        'value': '00000000',
    },
    '61': {
        'msg_id': 61,
        'value': '000000000000',
    },
    '60': {
        'msg_id': 60,
        'value': '00000000',
    },
    '539': {
        'msg_id': 539,
        'value': '00000000',
    },
    '538': {
        'msg_id': 538,
        'value': '0000000000000000',
    },
    '537': {
        'msg_id': 537,
        'value': '0000000000000000',
    },
    '72': {
        'msg_id': 72,
        'value': '0000000000000000',
    },
    '535': {
        'msg_id': 535,
        'value': '000000000000',
    },
    '1582': {
        'msg_id': 1582,
        'value': '0000000000000000',
    },
    '671': {
        'msg_id': 671,
        'value': '00000000000000',
    },
    '212': {
        'msg_id': 212,
        'value': '000000000000',
    },
    '141': {
        'msg_id': 141,
        'value': '0000000000000000',
    },
    '584': {
        'msg_id': 584,
        'value': '0000000000000000',
    },
    '133': {
        'msg_id': 133,
        'value': '0000000000000000',
    },
    '576': {
        'msg_id': 576,
        'value': '0000000000000000',
    },
    '2024': {
        'msg_id': 2024,
        'value': '0000000000000000',
    },
    '2016': {
        'msg_id': 2016,
        'value': '0000000000000000',
    },
    '2015': {
        'msg_id': 2015,
        'value': '0000000000000000',
    },
    '898': {
        'msg_id': 898,
        'value': '0000000000000000',
    },
    '638': {
        'msg_id': 638,
        'value': '0000000000000000',
    },
    '1288': {
        'msg_id': 1288,
        'value': '0000000000000000',
    },
    '1285': {
        'msg_id': 1285,
        'value': '0000000000000000',
    },
    '1292': {
        'msg_id': 1292,
        'value': '0000000000000000',
    },
    '44': {
        'msg_id': 44,
        'value': '0000000000000000',
    },
    '42': {
        'msg_id': 42,
        'value': '0000000000000000',
    },
    '43': {
        'msg_id': 43,
        'value': '0000000000000000',
    },
    '41': {
        'msg_id': 41,
        'value': '0000000000000000',
    },
    '1672': {
        'msg_id': 1672,
        'value': '0000000000000000',
    },
    '1679': {
        'msg_id': 1679,
        'value': '0000000000000000',
    },
    '623': {
        'msg_id': 623,
        'value': '0000000000000000',
    },
    '625': {
        'msg_id': 625,
        'value': '0000000000000000',
    },
    '626': {
        'msg_id': 626,
        'value': '0000000000000000',
    },
    '627': {
        'msg_id': 627,
        'value': '0000000000000000',
    },
    '654': {
        'msg_id': 654,
        'value': '0000000000000000'
    },
    '655': {
        'msg_id': 655,
        'value': '0000',
    },
    '686': {
        'msg_id': 686,
        'value': '00000000000000',
    },
    '770': {
        'msg_id': 770,
        'value': '0000000000000000',
    },
    '784': {
        'msg_id': 784,
        'value': '0000000000000000',
    },
    '785': {
        'msg_id': 785,
        'value': '000000',
    },
    '786': {
        'msg_id': 786,
        'value': '0000000000',
    },
    '788': {
        'msg_id': 788,
        'value': '0000000000000000',
    },
    '69': {
        'msg_id': 69,
        'value': '0000000000000000',
    },
    '70': {
        'msg_id': 70,
        'value': '0000000000000000',
    },
    '71': {
        'msg_id': 71,
        'value': '0000000000000000',
    },
    '80': {
        'msg_id': 80,
        'value': '00000000',
    },
    '88': {
        'msg_id': 88,
        'value': '000000000000',
    },
    '89': {
        'msg_id': 89,
        'value': '000000000000',
    },
    '132': {
        'msg_id': 132,
        'value': '0000000000000000',
    },
    '140': {
        'msg_id': 140,
        'value': '0000000000000000',
    },
    '149': {
        'msg_id': 149,
        'value': '0000000000',
    },
    '172': {
        'msg_id': 172,
        'value': '0000000000000000',
    },
    '174': {
        'msg_id': 174,
        'value': '0000000000000000',
    },
    '204': {
        'msg_id': 204,
        'value': '0000000000',
    },
    '431': {
        'msg_id': 431,
        'value': '000000000000',
    },
    '882': {
        'msg_id': 882,
        'value': '0000000000000000',
    },
    '905': {
        'msg_id': 905,
        'value': '0000000000000000',
    },
    '921': {
        'msg_id': 921,
        'value': '0000000000000000',
    },
    '938': {
        'msg_id': 938,
        'value': '000000',
    },
    '946': {
        'msg_id': 946,
        'value': '000000000000',
    },
    '959': {
        'msg_id': 959,
        'value': '0000000000000000',
    },
}
