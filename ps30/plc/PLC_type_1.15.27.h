/**************************************************************
 * Copyright (C) 2021, SHANGHAI NIO CO., LTD
 * All rights reserved.
 * Product No.  : PUS3.0
 * Component ID : BS
 * File Name    : PLC_type.h
 * Description  :
 * History :
 * Version         Date                User                Comments
 * V1.0            2022-07-01          shuquan.fan         update
 ***************************************************************/

#ifndef PLC_TYPE_H
#define PLC_TYPE_H
#include <stdint.h>


/**
 * @brief 指定结构体1字节对齐
 */

/**
 * @brief 宏定义
 */
#define PLC_AXIS_NUM_MAX (40)
#define PLC_SLOT_NUM_MAX (22)
#define PLC_MOTION_NUM_MAX (280)
#define PLC_ALARM_NUM_MAX (2000)

/**
 *@brief 主控下发请求报文头 数据结构定义
 */
typedef struct
{
	int8_t com_id;  /*命令ID*/
	bool   execute;	/*执行*/
 }PLC_REQ_HEADER_STRUCT;
 
/**
 *@brief PLC工作模式状态
 **/
typedef enum
{
	PLC_MODE_MIN        						= 0,
	PLC_MODE_AUTO       						= 1, // 自动
	PLC_MODE_MANUL      						= 2, // 手动    
	PLC_MODE_FAULT      						= 3, // 故障	   
	PLC_MODE_STOP       						= 4, // 停机	  
	PLC_MODE_PAUSE      						= 5, // 暂停	
	PLC_MODE_MAX
}PLC_MODE_ENUM;

/**
 *@brief 设备类型
 **/
typedef enum
{
	PLC_DEVICE_TYPE_MIN            				= -1,
	PLC_DEVICE_TYPE_SERVO           			= 1, // 伺服
	PLC_DEVICE_TYPE_CONVERTER       			= 2, // 变频器
	PLC_DEVICE_TYPE_EC              			= 3, // 电缸
	PLC_DEVICE_TYPE_ELECTROMAGNET  				= 4, // 电磁铁
	PLC_DEVICE_TYPE_SERVO_CONVERTER				= 5, // 伺服变频器组合
	PLC_DEVICE_TYPE_RELAY						= 6, // 继电器
	PLC_DEVICE_TYPE_OTHER						= 7, // 其他

	PLC_DEVICE_TYPE_MAX
}PLC_DEVICE_TYPE_ENUM;

/**
 *@brief 轴ID枚举定义
 **/
typedef enum
{
	PLC_AXIS_ID_MIN 							= 0,
	PLC_AXIS_ID_01								= 1, // 货叉
	PLC_AXIS_ID_02								= 2, // 堆垛机平移
	PLC_AXIS_ID_03								= 3, // 堆垛机升降
	PLC_AXIS_ID_04								= 4, // 加解锁1
	PLC_AXIS_ID_05								= 5, // 加解锁2
	PLC_AXIS_ID_06								= 6, // 加解锁3
	PLC_AXIS_ID_07								= 7, // 加解锁4
	PLC_AXIS_ID_08								= 8, // 加解锁5
	PLC_AXIS_ID_09								= 9, // 加解锁6
	PLC_AXIS_ID_10								= 10,// 加解锁7
	PLC_AXIS_ID_11 								= 11,// 加解锁8
	PLC_AXIS_ID_12 								= 12,// 加解锁9
	PLC_AXIS_ID_13 								= 13,// 加解锁10
	PLC_AXIS_ID_14 								= 14,// 加解锁11
	PLC_AXIS_ID_15 								= 15,// 加解锁12
	PLC_AXIS_ID_16 								= 16,// 左开合门
	PLC_AXIS_ID_17 								= 17,// 右开合门
	PLC_AXIS_ID_18 								= 18,// 1#枪头升降
	PLC_AXIS_ID_19 								= 19,// 2#枪头升降
	PLC_AXIS_ID_20 								= 20,// 9#枪头平移
	PLC_AXIS_ID_21 								= 21,// 9#枪头升降
	PLC_AXIS_ID_22 								= 22,// 10#枪头平移
	PLC_AXIS_ID_23 								= 23,// 10#枪头升降
	PLC_AXIS_ID_24 								= 24,// 1‘#枪头升降
	PLC_AXIS_ID_25 								= 25,// 2‘#枪头升降
	PLC_AXIS_ID_26 								= 26,// 左前车身定位销
	PLC_AXIS_ID_27 								= 27,// 左后车身定位销
	PLC_AXIS_ID_28 								= 28,// 右后车身定位销
	PLC_AXIS_ID_29 								= 29,// 左前推杆
	PLC_AXIS_ID_30 								= 30,// 右前推杆
	PLC_AXIS_ID_31 								= 31,// 前导向条
	PLC_AXIS_ID_32 								= 32,// V型槽
	PLC_AXIS_ID_33 								= 33,// 左后推杆
	PLC_AXIS_ID_34 								= 34,// 右后推杆
	PLC_AXIS_ID_35 								= 35,// 后导向条
	PLC_AXIS_ID_36 								= 36,// 加解锁平台平移
	PLC_AXIS_ID_37 								= 37,// 加解锁平台举升
	PLC_AXIS_ID_38 								= 38,// 预留
	PLC_AXIS_ID_39 								= 39,// 预留
	PLC_AXIS_ID_40 								= 40,// 升降仓

	PLC_AXIS_ID_50 								= 50,// 所有加解锁同步，虚拟轴
	PLC_AXIS_ID_52 								= 52,// 自动加锁屏蔽，虚拟轴
	PLC_AXIS_ID_53 								= 53,// 自动解锁屏蔽，虚拟轴
	PLC_AXIS_ID_54 								= 54,// 车辆举升一键回零点，虚拟轴
	PLC_AXIS_ID_55 								= 55,// 一键推车，虚拟轴

	PLC_AXIS_ID_MAX
}PLC_AXIS_ID_ENUM; 

/**
 *@brief 动作ID 枚举定义
 **/
typedef enum
{
	PLC_MOTION_ID_MIN 							= -1,

	PLC_MOTION_ID_PL_LF_CLAMP_HOME				= 1,// 左前推杆至原点位									
	PLC_MOTION_ID_PL_LF_CLAMP_WORK				= 2,// 左前推杆至工作位									
	PLC_MOTION_ID_PL_RF_CLAMP_HOME				= 3,// 右前推杆至原点位									
	PLC_MOTION_ID_PL_RF_CLAMP_WORK				= 4,// 右前推杆至工作位									
	PLC_MOTION_ID_PL_LR_CLAMP_HOME				= 5,// 左后推杆至原点位									
	PLC_MOTION_ID_PL_LR_CLAMP_WORK				= 6,// 左后推杆至工作位									
	PLC_MOTION_ID_PL_RR_CLAMP_HOME				= 7,// 右后推杆至原点位									
	PLC_MOTION_ID_PL_RR_CLAMP_WORK				= 8,// 右后推杆至工作位									
	PLC_MOTION_ID_PL_V_HOME						= 9,// V形槽至原点位							
	PLC_MOTION_ID_PL_V_WORK						= 10,// V形槽至工作位							
	PLC_MOTION_ID_GUN1_Z_HOME					= 11,// 1号枪头升降至原点位								
	PLC_MOTION_ID_GUN1_Z_WORK					= 12,// 1号枪头升降至工作位								
	PLC_MOTION_ID_GUN2_Z_HOME					= 13,// 2号枪头升降至原点位								
	PLC_MOTION_ID_GUN2_Z_WORK					= 14,// 2号枪头升降至工作位								
	PLC_MOTION_ID_GUN11_Z_HOME					= 15,// 1'号枪头升降至原点位								
	PLC_MOTION_ID_GUN11_Z_WORK					= 16,// 1'号枪头升降至工作位								
	PLC_MOTION_ID_GUN21_Z_HOME					= 17,// 2'号枪头升降至原点位								
	PLC_MOTION_ID_GUN21_Z_WORK					= 18,// 2'号枪头升降至工作位								
	PLC_MOTION_ID_GUN9_X_HOME					= 19,// 9号枪头横移至原点位								
	PLC_MOTION_ID_GUN9_X_WORK					= 20,// 9号枪头横移至工作位								
	PLC_MOTION_ID_GUN10_X_HOME					= 21,// 10号枪头横移至原点位								
	PLC_MOTION_ID_GUN10_X_WORK					= 22,// 10号枪头横移至工作位								
	PLC_MOTION_ID_GUN9_Z_HOME					= 23,// 9号枪头升降至原点位								
	PLC_MOTION_ID_GUN9_Z_WORK					= 24,// 9号枪头升降至工作位								
	PLC_MOTION_ID_GUN10_Z_HOME					= 25,// 10号枪头升降至原点位								
	PLC_MOTION_ID_GUN10_Z_WORK					= 26,// 10号枪头升降至工作位								
	PLC_MOTION_ID_LR_LF_PIN_FIXED_HOME			= 27,// 左前车身定位销至原点位										
	PLC_MOTION_ID_LR_LF_PIN_FIXED_WORK			= 28,// 左前车身定位销至工作位										
	PLC_MOTION_ID_LR_LR_PIN_FIXED_HOME			= 29,// 左后车身定位销至原点位										
	PLC_MOTION_ID_LR_LR_PIN_FIXED_WORK			= 30,// 左后车身定位销至工作位										
	PLC_MOTION_ID_LR_RR_PIN_FIXED_HOME			= 31,// 右后车身定位销至原点位										
	PLC_MOTION_ID_LR_RR_PIN_FIXED_WORK			= 32,// 右后车身定位销至工作位										
	PLC_MOTION_ID_DOOR_01_CLOSE					= 33,// 左开合门关闭								
	PLC_MOTION_ID_DOOR_01_OPEN					= 34,// 左开合门打开								
	PLC_MOTION_ID_DOOR_02_CLOSE					= 35,// 右开合门关闭								
	PLC_MOTION_ID_DOOR_02_OPEN					= 36,// 右开合门打开								
	PLC_MOTION_ID_LR_POSITION1					= 37,// 加解锁平台抬升至原点位								
	PLC_MOTION_ID_LR_POSITION2					= 38,// 加解锁平台抬升至卡销位								
	PLC_MOTION_ID_LR_POSITION3					= 39,// 加解锁平台抬升至销子位								
	PLC_MOTION_ID_LR_POSITION4					= 40,// 加解锁平台抬升至插头位								
	PLC_MOTION_ID_LR_POSITION5					= 41,// 加解锁平台抬升至加解锁位								
	PLC_MOTION_ID_PL_MOVE_HOME					= 42,// 平台板移动至原点位								
	PLC_MOTION_ID_PL_MOVE_WORK					= 43,// 平台板移动至工作位								
	PLC_MOTION_ID_PL_F_GUIDE_HOME				= 44,// 停车平台前导向条至原点位									
	PLC_MOTION_ID_PL_F_GUIDE_WORK				= 45,// 停车平台前导向条至工作位									
	PLC_MOTION_ID_PL_R_GUIDE_HOME				= 46,// 停车平台后导向条至原点位									
	PLC_MOTION_ID_PL_R_GUIDE_WORK				= 47,// 停车平台后导向条至工作位									
	PLC_MOTION_ID_BL_HOME						= 48,// 升降仓至原点位							
	PLC_MOTION_ID_BL_WORK						= 49,// 升降仓至工作位							
	PLC_MOTION_ID_FORK_X_HOME					= 50,// 货叉至原点位								
	PLC_MOTION_ID_FORK_X_WORK					= 51,// 货叉至工作位								
	PLC_MOTION_ID_STACKER_MOVE_WORK				= 52,// 堆垛机平移至工作位									
	PLC_MOTION_ID_STACKER_LIFT_HOME				= 53,// 堆垛机升降至目标仓低位									
	PLC_MOTION_ID_STACKER_LIFT_WORK				= 54,// 堆垛机升降至目标仓高位									
	PLC_MOTION_ID_MANUAL_GUN_LOCK_START			= 55,// 单轴加锁点动										
	PLC_MOTION_ID_MANUAL_GUN_UNLOCK_START		= 56,// 单轴解锁点动											
	PLC_MOTION_ID_ALL_LOCK_START				= 57,// 一键加锁									
	PLC_MOTION_ID_ALL_UNLOCK_START				= 58,// 一键解锁									
	PLC_MOTION_ID_BL_TO_BUFFER					= 59,// 电池从升降仓至右缓存位							
	PLC_MOTION_ID_BUFFER_TO_BL					= 60,// 电池从右缓存位至升降仓							
	PLC_MOTION_ID_BUFFER_TO_PL					= 61,// 电池从右缓存位至停车平台								
	PLC_MOTION_ID_PL_TO_BL						= 62,// 电池从停车平台至升降仓
	PLC_MOTION_ID_BL_TO_PL						= 63,// 电池从升降仓至停车平台								
	PLC_MOTION_ID_SLOT_01_LIQ_PLUG_EXTEND_01	= 64,// #1仓水插头伸出1												
	PLC_MOTION_ID_SLOT_01_LIQ_PLUG_RETRACT_01	= 65,// #1仓水插头缩回1												
	PLC_MOTION_ID_SLOT_02_LIQ_PLUG_EXTEND_01	= 66,// #2仓水插头伸出1												
	PLC_MOTION_ID_SLOT_02_LIQ_PLUG_RETRACT_01	= 67,// #2仓水插头缩回1												
	PLC_MOTION_ID_SLOT_03_LIQ_PLUG_EXTEND_01	= 68,// #3仓水插头伸出1												
	PLC_MOTION_ID_SLOT_03_LIQ_PLUG_RETRACT_01	= 69,// #3仓水插头缩回1												
	PLC_MOTION_ID_SLOT_04_LIQ_PLUG_EXTEND_01	= 70,// #4仓水插头伸出1												
	PLC_MOTION_ID_SLOT_04_LIQ_PLUG_RETRACT_01	= 71,// #4仓水插头缩回1												
	PLC_MOTION_ID_SLOT_05_LIQ_PLUG_EXTEND_01	= 72,// #5仓水插头伸出1												
	PLC_MOTION_ID_SLOT_05_LIQ_PLUG_RETRACT_01	= 73,// #5仓水插头缩回1												
	PLC_MOTION_ID_SLOT_06_LIQ_PLUG_EXTEND_01	= 74,// #6仓水插头伸出1												
	PLC_MOTION_ID_SLOT_06_LIQ_PLUG_RETRACT_01	= 75,// #6仓水插头缩回1												
	PLC_MOTION_ID_SLOT_07_LIQ_PLUG_EXTEND_01	= 76,// #7仓水插头伸出1												
	PLC_MOTION_ID_SLOT_07_LIQ_PLUG_RETRACT_01	= 77,// #7仓水插头缩回1												
	PLC_MOTION_ID_SLOT_08_LIQ_PLUG_EXTEND_01	= 78,// #8仓水插头伸出1												
	PLC_MOTION_ID_SLOT_08_LIQ_PLUG_RETRACT_01	= 79,// #8仓水插头缩回1												
	PLC_MOTION_ID_SLOT_09_LIQ_PLUG_EXTEND_01	= 80,// #9仓水插头伸出1												
	PLC_MOTION_ID_SLOT_09_LIQ_PLUG_RETRACT_01	= 81,// #9仓水插头缩回1												
	PLC_MOTION_ID_SLOT_10_LIQ_PLUG_EXTEND_01	= 82,// #10仓水插头伸出1												
	PLC_MOTION_ID_SLOT_10_LIQ_PLUG_RETRACT_01	= 83,// #10仓水插头缩回1												
	PLC_MOTION_ID_SLOT_11_LIQ_PLUG_EXTEND_01	= 84,// #11仓水插头伸出1												
	PLC_MOTION_ID_SLOT_11_LIQ_PLUG_RETRACT_01	= 85,// #11仓水插头缩回1												
	PLC_MOTION_ID_SLOT_12_LIQ_PLUG_EXTEND_01	= 86,// #12仓水插头伸出1												
	PLC_MOTION_ID_SLOT_12_LIQ_PLUG_RETRACT_01	= 87,// #12仓水插头缩回1												
	PLC_MOTION_ID_SLOT_13_LIQ_PLUG_EXTEND_01	= 88,// #13仓水插头伸出1												
	PLC_MOTION_ID_SLOT_13_LIQ_PLUG_RETRACT_01	= 89,// #13仓水插头缩回1												
	PLC_MOTION_ID_SLOT_14_LIQ_PLUG_EXTEND_01	= 90,// #14仓水插头伸出1												
	PLC_MOTION_ID_SLOT_14_LIQ_PLUG_RETRACT_01	= 91,// #14仓水插头缩回1												
	PLC_MOTION_ID_SLOT_15_LIQ_PLUG_EXTEND_01	= 92,// #15仓水插头伸出1												
	PLC_MOTION_ID_SLOT_15_LIQ_PLUG_RETRACT_01	= 93,// #15仓水插头缩回1												
	PLC_MOTION_ID_SLOT_16_LIQ_PLUG_EXTEND_01	= 94,// #16仓水插头伸出1												
	PLC_MOTION_ID_SLOT_16_LIQ_PLUG_RETRACT_01	= 95,// #16仓水插头缩回1												
	PLC_MOTION_ID_SLOT_17_LIQ_PLUG_EXTEND_01	= 96,// #17仓水插头伸出1												
	PLC_MOTION_ID_SLOT_17_LIQ_PLUG_RETRACT_01	= 97,// #17仓水插头缩回1												
	PLC_MOTION_ID_SLOT_18_LIQ_PLUG_EXTEND_01	= 98,// #18仓水插头伸出1												
	PLC_MOTION_ID_SLOT_18_LIQ_PLUG_RETRACT_01	= 99,// #18仓水插头缩回1												
	PLC_MOTION_ID_SLOT_19_LIQ_PLUG_EXTEND_01	= 100,// #19仓水插头伸出1												
	PLC_MOTION_ID_SLOT_19_LIQ_PLUG_RETRACT_01	= 101,// #19仓水插头缩回1												
	PLC_MOTION_ID_SLOT_20_LIQ_PLUG_EXTEND_01	= 102,// #20仓水插头伸出1												
	PLC_MOTION_ID_SLOT_20_LIQ_PLUG_RETRACT_01	= 103,// #20仓水插头缩回1												
	PLC_MOTION_ID_SLOT_01_LIQ_PLUG_EXTEND_02	= 104,// #1仓水插头伸出2												
	PLC_MOTION_ID_SLOT_01_LIQ_PLUG_RETRACT_02	= 105,// #1仓水插头缩回2												
	PLC_MOTION_ID_SLOT_02_LIQ_PLUG_EXTEND_02	= 106,// #2仓水插头伸出2												
	PLC_MOTION_ID_SLOT_02_LIQ_PLUG_RETRACT_02	= 107,// #2仓水插头缩回2												
	PLC_MOTION_ID_SLOT_03_LIQ_PLUG_EXTEND_02	= 108,// #3仓水插头伸出2												
	PLC_MOTION_ID_SLOT_03_LIQ_PLUG_RETRACT_02	= 109,// #3仓水插头缩回2												
	PLC_MOTION_ID_SLOT_04_LIQ_PLUG_EXTEND_02	= 110,// #4仓水插头伸出2												
	PLC_MOTION_ID_SLOT_04_LIQ_PLUG_RETRACT_02	= 111,// #4仓水插头缩回2												
	PLC_MOTION_ID_SLOT_05_LIQ_PLUG_EXTEND_02	= 112,// #5仓水插头伸出2												
	PLC_MOTION_ID_SLOT_05_LIQ_PLUG_RETRACT_02	= 113,// #5仓水插头缩回2												
	PLC_MOTION_ID_SLOT_06_LIQ_PLUG_EXTEND_02	= 114,// #6仓水插头伸出2												
	PLC_MOTION_ID_SLOT_06_LIQ_PLUG_RETRACT_02	= 115,// #6仓水插头缩回2												
	PLC_MOTION_ID_SLOT_07_LIQ_PLUG_EXTEND_02	= 116,// #7仓水插头伸出2												
	PLC_MOTION_ID_SLOT_07_LIQ_PLUG_RETRACT_02	= 117,// #7仓水插头缩回2												
	PLC_MOTION_ID_SLOT_08_LIQ_PLUG_EXTEND_02	= 118,// #8仓水插头伸出2												
	PLC_MOTION_ID_SLOT_08_LIQ_PLUG_RETRACT_02	= 119,// #8仓水插头缩回2												
	PLC_MOTION_ID_SLOT_09_LIQ_PLUG_EXTEND_02	= 120,// #9仓水插头伸出2												
	PLC_MOTION_ID_SLOT_09_LIQ_PLUG_RETRACT_02	= 121,// #9仓水插头缩回2												
	PLC_MOTION_ID_SLOT_10_LIQ_PLUG_EXTEND_02	= 122,// #10仓水插头伸出2												
	PLC_MOTION_ID_SLOT_10_LIQ_PLUG_RETRACT_02	= 123,// #10仓水插头缩回2												
	PLC_MOTION_ID_SLOT_11_LIQ_PLUG_EXTEND_02	= 124,// #11仓水插头伸出2												
	PLC_MOTION_ID_SLOT_11_LIQ_PLUG_RETRACT_02	= 125,// #11仓水插头缩回2												
	PLC_MOTION_ID_SLOT_12_LIQ_PLUG_EXTEND_02	= 126,// #12仓水插头伸出2												
	PLC_MOTION_ID_SLOT_12_LIQ_PLUG_RETRACT_02	= 127,// #12仓水插头缩回2												
	PLC_MOTION_ID_SLOT_13_LIQ_PLUG_EXTEND_02	= 128,// #13仓水插头伸出2												
	PLC_MOTION_ID_SLOT_13_LIQ_PLUG_RETRACT_02	= 129,// #13仓水插头缩回2												
	PLC_MOTION_ID_SLOT_14_LIQ_PLUG_EXTEND_02	= 130,// #14仓水插头伸出2												
	PLC_MOTION_ID_SLOT_14_LIQ_PLUG_RETRACT_02	= 131,// #14仓水插头缩回2												
	PLC_MOTION_ID_SLOT_15_LIQ_PLUG_EXTEND_02	= 132,// #15仓水插头伸出2												
	PLC_MOTION_ID_SLOT_15_LIQ_PLUG_RETRACT_02	= 133,// #15仓水插头缩回2												
	PLC_MOTION_ID_SLOT_16_LIQ_PLUG_EXTEND_02	= 134,// #16仓水插头伸出2												
	PLC_MOTION_ID_SLOT_16_LIQ_PLUG_RETRACT_02	= 135,// #16仓水插头缩回2												
	PLC_MOTION_ID_SLOT_17_LIQ_PLUG_EXTEND_02	= 136,// #17仓水插头伸出2												
	PLC_MOTION_ID_SLOT_17_LIQ_PLUG_RETRACT_02	= 137,// #17仓水插头缩回2												
	PLC_MOTION_ID_SLOT_18_LIQ_PLUG_EXTEND_02	= 138,// #18仓水插头伸出2												
	PLC_MOTION_ID_SLOT_18_LIQ_PLUG_RETRACT_02	= 139,// #18仓水插头缩回2												
	PLC_MOTION_ID_SLOT_19_LIQ_PLUG_EXTEND_02	= 140,// #19仓水插头伸出2												
	PLC_MOTION_ID_SLOT_19_LIQ_PLUG_RETRACT_02	= 141,// #19仓水插头缩回2												
	PLC_MOTION_ID_SLOT_20_LIQ_PLUG_EXTEND_02	= 142,// #20仓水插头伸出2												
	PLC_MOTION_ID_SLOT_20_LIQ_PLUG_RETRACT_02	= 143,// #20仓水插头缩回2												
	PLC_MOTION_ID_SLOT_01_PWR_PLUG_EXTEND_01	= 144,// #1电插头伸出1												
	PLC_MOTION_ID_SLOT_01_PWR_PLUG_RETRACT_01	= 145,// #1电插头缩回1												
	PLC_MOTION_ID_SLOT_02_PWR_PLUG_EXTEND_01	= 146,// #2电插头伸出1												
	PLC_MOTION_ID_SLOT_02_PWR_PLUG_RETRACT_01	= 147,// #2电插头缩回1												
	PLC_MOTION_ID_SLOT_03_PWR_PLUG_EXTEND_01	= 148,// #3电插头伸出1												
	PLC_MOTION_ID_SLOT_03_PWR_PLUG_RETRACT_01	= 149,// #3电插头缩回1												
	PLC_MOTION_ID_SLOT_04_PWR_PLUG_EXTEND_01	= 150,// #4电插头伸出1												
	PLC_MOTION_ID_SLOT_04_PWR_PLUG_RETRACT_01	= 151,// #4电插头缩回1												
	PLC_MOTION_ID_SLOT_05_PWR_PLUG_EXTEND_01	= 152,// #5电插头伸出1												
	PLC_MOTION_ID_SLOT_05_PWR_PLUG_RETRACT_01	= 153,// #5电插头缩回1												
	PLC_MOTION_ID_SLOT_06_PWR_PLUG_EXTEND_01	= 154,// #6电插头伸出1												
	PLC_MOTION_ID_SLOT_06_PWR_PLUG_RETRACT_01	= 155,// #6电插头缩回1												
	PLC_MOTION_ID_SLOT_07_PWR_PLUG_EXTEND_01	= 156,// #7电插头伸出1												
	PLC_MOTION_ID_SLOT_07_PWR_PLUG_RETRACT_01	= 157,// #7电插头缩回1												
	PLC_MOTION_ID_SLOT_08_PWR_PLUG_EXTEND_01	= 158,// #8电插头伸出1												
	PLC_MOTION_ID_SLOT_08_PWR_PLUG_RETRACT_01	= 159,// #8电插头缩回1												
	PLC_MOTION_ID_SLOT_09_PWR_PLUG_EXTEND_01	= 160,// #9电插头伸出1												
	PLC_MOTION_ID_SLOT_09_PWR_PLUG_RETRACT_01	= 161,// #9电插头缩回1												
	PLC_MOTION_ID_SLOT_10_PWR_PLUG_EXTEND_01	= 162,// #10电插头伸出1												
	PLC_MOTION_ID_SLOT_10_PWR_PLUG_RETRACT_01	= 163,// #10电插头缩回1												
	PLC_MOTION_ID_SLOT_11_PWR_PLUG_EXTEND_01	= 164,// #11电插头伸出1												
	PLC_MOTION_ID_SLOT_11_PWR_PLUG_RETRACT_01	= 165,// #11电插头缩回1												
	PLC_MOTION_ID_SLOT_12_PWR_PLUG_EXTEND_01	= 166,// #12电插头伸出1												
	PLC_MOTION_ID_SLOT_12_PWR_PLUG_RETRACT_01	= 167,// #12电插头缩回1												
	PLC_MOTION_ID_SLOT_13_PWR_PLUG_EXTEND_01	= 168,// #13电插头伸出1												
	PLC_MOTION_ID_SLOT_13_PWR_PLUG_RETRACT_01	= 169,// #13电插头缩回1												
	PLC_MOTION_ID_SLOT_14_PWR_PLUG_EXTEND_01	= 170,// #14电插头伸出1												
	PLC_MOTION_ID_SLOT_14_PWR_PLUG_RETRACT_01	= 171,// #14电插头缩回1												
	PLC_MOTION_ID_SLOT_15_PWR_PLUG_EXTEND_01	= 172,// #15电插头伸出1												
	PLC_MOTION_ID_SLOT_15_PWR_PLUG_RETRACT_01	= 173,// #15电插头缩回1												
	PLC_MOTION_ID_SLOT_16_PWR_PLUG_EXTEND_01	= 174,// #16电插头伸出1												
	PLC_MOTION_ID_SLOT_16_PWR_PLUG_RETRACT_01	= 175,// #16电插头缩回1												
	PLC_MOTION_ID_SLOT_17_PWR_PLUG_EXTEND_01	= 176,// #17电插头伸出1												
	PLC_MOTION_ID_SLOT_17_PWR_PLUG_RETRACT_01	= 177,// #17电插头缩回1												
	PLC_MOTION_ID_SLOT_18_PWR_PLUG_EXTEND_01	= 178,// #18电插头伸出1												
	PLC_MOTION_ID_SLOT_18_PWR_PLUG_RETRACT_01	= 179,// #18电插头缩回1												
	PLC_MOTION_ID_SLOT_19_PWR_PLUG_EXTEND_01	= 180,// #19电插头伸出1												
	PLC_MOTION_ID_SLOT_19_PWR_PLUG_RETRACT_01	= 181,// #19电插头缩回1												
	PLC_MOTION_ID_SLOT_20_PWR_PLUG_EXTEND_01	= 182,// #20电插头伸出1												
	PLC_MOTION_ID_SLOT_20_PWR_PLUG_RETRACT_01	= 183,// #20电插头缩回1												
	PLC_MOTION_ID_SLOT_21_PWR_PLUG_EXTEND_01	= 184,// #21电插头伸出1												
	PLC_MOTION_ID_SLOT_21_PWR_PLUG_RETRACT_01	= 185,// #21电插头缩回1												
	PLC_MOTION_ID_SLOT_01_PWR_PLUG_EXTEND_02	= 186,// #1电插头伸出2												
	PLC_MOTION_ID_SLOT_01_PWR_PLUG_RETRACT_02	= 187,// #1电插头缩回2												
	PLC_MOTION_ID_SLOT_02_PWR_PLUG_EXTEND_02	= 188,// #2电插头伸出2												
	PLC_MOTION_ID_SLOT_02_PWR_PLUG_RETRACT_02	= 189,// #2电插头缩回2												
	PLC_MOTION_ID_SLOT_03_PWR_PLUG_EXTEND_02	= 190,// #3电插头伸出2												
	PLC_MOTION_ID_SLOT_03_PWR_PLUG_RETRACT_02	= 191,// #3电插头缩回2												
	PLC_MOTION_ID_SLOT_04_PWR_PLUG_EXTEND_02	= 192,// #4电插头伸出2												
	PLC_MOTION_ID_SLOT_04_PWR_PLUG_RETRACT_02	= 193,// #4电插头缩回2												
	PLC_MOTION_ID_SLOT_05_PWR_PLUG_EXTEND_02	= 194,// #5电插头伸出2												
	PLC_MOTION_ID_SLOT_05_PWR_PLUG_RETRACT_02	= 195,// #5电插头缩回2												
	PLC_MOTION_ID_SLOT_06_PWR_PLUG_EXTEND_02	= 196,// #6电插头伸出2												
	PLC_MOTION_ID_SLOT_06_PWR_PLUG_RETRACT_02	= 197,// #6电插头缩回2												
	PLC_MOTION_ID_SLOT_07_PWR_PLUG_EXTEND_02	= 198,// #7电插头伸出2												
	PLC_MOTION_ID_SLOT_07_PWR_PLUG_RETRACT_02	= 199,// #7电插头缩回2												
	PLC_MOTION_ID_SLOT_08_PWR_PLUG_EXTEND_02	= 200,// #8电插头伸出2												
	PLC_MOTION_ID_SLOT_08_PWR_PLUG_RETRACT_02	= 201,// #8电插头缩回2												
	PLC_MOTION_ID_SLOT_09_PWR_PLUG_EXTEND_02	= 202,// #9电插头伸出2												
	PLC_MOTION_ID_SLOT_09_PWR_PLUG_RETRACT_02	= 203,// #9电插头缩回2												
	PLC_MOTION_ID_SLOT_10_PWR_PLUG_EXTEND_02	= 204,// #10电插头伸出2												
	PLC_MOTION_ID_SLOT_10_PWR_PLUG_RETRACT_02	= 205,// #10电插头缩回2												
	PLC_MOTION_ID_SLOT_11_PWR_PLUG_EXTEND_02	= 206,// #11电插头伸出2												
	PLC_MOTION_ID_SLOT_11_PWR_PLUG_RETRACT_02	= 207,// #11电插头缩回2												
	PLC_MOTION_ID_SLOT_12_PWR_PLUG_EXTEND_02	= 208,// #12电插头伸出2												
	PLC_MOTION_ID_SLOT_12_PWR_PLUG_RETRACT_02	= 209,// #12电插头缩回2												
	PLC_MOTION_ID_SLOT_13_PWR_PLUG_EXTEND_02	= 210,// #13电插头伸出2												
	PLC_MOTION_ID_SLOT_13_PWR_PLUG_RETRACT_02	= 211,// #13电插头缩回2												
	PLC_MOTION_ID_SLOT_14_PWR_PLUG_EXTEND_02	= 212,// #14电插头伸出2												
	PLC_MOTION_ID_SLOT_14_PWR_PLUG_RETRACT_02	= 213,// #14电插头缩回2												
	PLC_MOTION_ID_SLOT_15_PWR_PLUG_EXTEND_02	= 214,// #15电插头伸出2												
	PLC_MOTION_ID_SLOT_15_PWR_PLUG_RETRACT_02	= 215,// #15电插头缩回2												
	PLC_MOTION_ID_SLOT_16_PWR_PLUG_EXTEND_02	= 216,// #16电插头伸出2												
	PLC_MOTION_ID_SLOT_16_PWR_PLUG_RETRACT_02	= 217,// #16电插头缩回2												
	PLC_MOTION_ID_SLOT_17_PWR_PLUG_EXTEND_02	= 218,// #17电插头伸出2												
	PLC_MOTION_ID_SLOT_17_PWR_PLUG_RETRACT_02	= 219,// #17电插头缩回2												
	PLC_MOTION_ID_SLOT_18_PWR_PLUG_EXTEND_02	= 220,// #18电插头伸出2												
	PLC_MOTION_ID_SLOT_18_PWR_PLUG_RETRACT_02	= 221,// #18电插头缩回2												
	PLC_MOTION_ID_SLOT_19_PWR_PLUG_EXTEND_02	= 222,// #19电插头伸出2												
	PLC_MOTION_ID_SLOT_19_PWR_PLUG_RETRACT_02	= 223,// #19电插头缩回2												
	PLC_MOTION_ID_SLOT_20_PWR_PLUG_EXTEND_02	= 224,// #20电插头伸出2												
	PLC_MOTION_ID_SLOT_20_PWR_PLUG_RETRACT_02	= 225,// #20电插头缩回2												
	PLC_MOTION_ID_SLOT_21_PWR_PLUG_EXTEND_02	= 226,// #21电插头伸出2												
	PLC_MOTION_ID_SLOT_21_PWR_PLUG_RETRACT_02	= 227,// #21电插头缩回2												
	PLC_MOTION_ID_FIRE_F_STOPPER_EXTEND			= 228,// 消防仓前挡块伸出										
	PLC_MOTION_ID_FIRE_F_STOPPER_RETRACT		= 229,// 消防仓前挡块缩回											
	PLC_MOTION_ID_FIRE_R_STOPPER_EXTEND			= 230,// 消防仓后挡块伸出										
	PLC_MOTION_ID_FIRE_R_STOPPER_RETRACT		= 231,// 消防仓后挡块缩回											
	PLC_MOTION_ID_PL_FRONT_STOPPER_EXTEND		= 232,// 平台区前挡块伸出											
	PLC_MOTION_ID_PL_FRONT_STOPPER_RETRACT		= 233,// 平台区前挡块缩回											
	PLC_MOTION_ID_PL_REAR_STOPPER_EXTEND		= 234,// 平台区后挡块伸出											
	PLC_MOTION_ID_PL_REAR_STOPPER_RETRACT		= 235,// 平台区后挡块缩回											
	PLC_MOTION_ID_EC_ENABLE						= 236,// 电磁铁吸合							
	PLC_MOTION_ID_EC_DISABLE					= 237,// 电磁铁松开								
	PLC_MOTION_ID_AUTO_LOCK_BYPASS				= 238,// 自动加锁屏蔽									
	PLC_MOTION_ID_AUTO_UNLOCK_BYPASS			= 239,// 自动解锁屏蔽										
	PLC_MOTION_ID_AUTO_TRANSFER_OUT_SLOT		= 240,// 电池一键转运出仓											
	PLC_MOTION_ID_AUTO_TRANSFER_IN_SLOT			= 241,// 电池一键转运进仓										
	PLC_MOTION_ID_AUTO_TRANSFER_OUT_RACK		= 242,// 电池一键下架											
	PLC_MOTION_ID_VEHICAL_LIFT_TO_HOME_SYNC		= 243,// 车辆举升一键回零点	
	PLC_MOTION_ID_BUF_F_STOPPER_EXTEND			= 244,// 右缓冲区前挡块伸出																				
	PLC_MOTION_ID_BUF_F_STOPPER_RETRACT			= 245,// 右缓冲区前挡块缩回											
	PLC_MOTION_ID_BUF_R_STOPPER_EXTEND			= 246,// 右缓冲区后挡块伸出											
	PLC_MOTION_ID_BUF_R_STOPPER_RETRACT			= 247,// 右缓冲区后挡块缩回											
	PLC_MOTION_ID_PL_TO_L_BUF					= 248,// 电池从停车平台至左缓存位									
	PLC_MOTION_ID_L_BUF_TO_BL					= 249,// 电池从左缓存位至升降仓									
	PLC_MOTION_ID_V_L_STOPPER_EXTEND			= 250,// V槽锁止左挡块伸出											
	PLC_MOTION_ID_V_L_STOPPER_RETRACT			= 251,// V槽锁止左挡块缩回											
	PLC_MOTION_ID_V_R_STOPPER_EXTEND			= 252,// V槽锁止右挡块伸出											
	PLC_MOTION_ID_V_R_STOPPER_RETRACT			= 253,// V槽锁止右挡块缩回	
	PLC_MOTION_ID_ROLLER_DOOR_F_UP				= 254,// 前卷帘门上升
	PLC_MOTION_ID_ROLLER_DOOR_F_DOWN			= 255,// 前卷帘门下降
	PLC_MOTION_ID_ROLLER_DOOR_R_UP				= 256,// 后卷帘门上升
	PLC_MOTION_ID_ROLLER_DOOR_R_DOWN			= 257,// 后卷帘门下降
	PLC_MOTION_ID_ROLLER_DOOR_F_STOP			= 258,// 前卷帘门停止
	PLC_MOTION_ID_ROLLER_DOOR_R_STOP			= 259,// 后卷帘门停止																										                                                   
	PLC_CLAMP_RIGHT_MOVE_START_MOTION			= 260,// 向副驾侧推车
	PLC_CLAMP_LEFT_MOVE_START_MOTION			= 261,// 向主驾侧推车
	PLC_MOTION_ID_AL_DROP						= 262,// 告警仓一键落水
	PLC_MOTION_ID_AL_TO_PL						= 263,// 告警仓至平台
	PLC_MOTION_ID_AL_TO_ST						= 264,// 告警仓至堆垛机
	PLC_MOTION_ID_PL_DROP						= 265,// 平台一键落水
	PLC_MOTION_ID_ST_DROP						= 266,// 堆垛机一键落水
	PLC_MOTION_ID_ST_TO_PL						= 267,// 堆垛机至平台
	PLC_MOTION_ID_MAX
} PLC_MOTION_ID_ENUM;


/** 
 *@brief 变频器ID枚举定义
 **/
typedef enum
{
	PLC_CONVERTER_ID_MIN                     	= 0,
	PLC_CONVERTER_ID_1                       	= 1,// 电池转运
	PLC_CONVERTER_ID_2                       	= 2,// 一键进出仓、下架
	PLC_CONVERTER_ID_3                       	= 3,// 预留
	PLC_CONVERTER_ID_4                       	= 4,// 预留
	PLC_CONVERTER_ID_5                       	= 5,// 预留
	PLC_CONVERTER_ID_MAX
}PLC_CONVERTER_ID_ENUM; 

/** 
 *@brief 继电器ID枚举定义
 **/
typedef enum
{
	PLC_RELAY_ID_MIN                     		= 0,
	PLC_RELAY_ID_1                       		= 1,// 前卷帘门继电器
	PLC_RELAY_ID_2                       		= 2,// 后卷帘门继电器
	PLC_RELAY_ID_MAX
}PLC_RELAY_ID_ENUM; 

/**
 *@brief 电缸ID枚举定义
 **/
typedef enum
{
	PLC_EC_ID_MIN = 0, 
	PLC_EC_ID_1 = 1,								// 1仓水插头type1
	PLC_EC_ID_2 = 2,								// 2仓水插头type1
	PLC_EC_ID_3 = 3,								// 3仓水插头type1
	PLC_EC_ID_4 = 4,								// 4仓水插头type1
	PLC_EC_ID_5 = 5,								// 5仓水插头type1
	PLC_EC_ID_6 = 6,								// 6仓水插头type1
	PLC_EC_ID_7 = 7,								// 7仓水插头type1
	PLC_EC_ID_8 = 8,								// 8仓水插头type1
	PLC_EC_ID_9 = 9,								// 9仓水插头type1
	PLC_EC_ID_10 = 10,								// 10仓水插头type1
	PLC_EC_ID_11 = 11,								// 11仓水插头type1
	PLC_EC_ID_12 = 12,								// 12仓水插头type1	
	PLC_EC_ID_13 = 13,								// 13仓水插头type1
	PLC_EC_ID_14 = 14,								// 14仓水插头type1
	PLC_EC_ID_15 = 15,								// 15仓水插头type1
	PLC_EC_ID_16 = 16,								// 16仓水插头type1
	PLC_EC_ID_17 = 17,								// 17仓水插头type1
	PLC_EC_ID_18 = 18,								// 18仓水插头type1
	PLC_EC_ID_19 = 19,								// 19仓水插头type1
	PLC_EC_ID_20 = 20,								// 20仓水插头type1
	PLC_EC_ID_21 = 21,								// 1仓水插头type2
	PLC_EC_ID_22 = 22,								// 2仓水插头type2
	PLC_EC_ID_23 = 23,								// 3仓水插头type2
	PLC_EC_ID_24 = 24,								// 4仓水插头type2
	PLC_EC_ID_25 = 25,								// 5仓水插头type2
	PLC_EC_ID_26 = 26,								// 6仓水插头type2
	PLC_EC_ID_27 = 27,								// 7仓水插头type2
	PLC_EC_ID_28 = 28,								// 8仓水插头type2
	PLC_EC_ID_29 = 29,								// 9仓水插头type2
	PLC_EC_ID_30 = 30,								// 10仓水插头type2
	PLC_EC_ID_31 = 31,								// 11仓水插头type2
	PLC_EC_ID_32 = 32,								// 12仓水插头type2
	PLC_EC_ID_33 = 33,								// 13仓水插头type2
	PLC_EC_ID_34 = 34,								// 14仓水插头type2
	PLC_EC_ID_35 = 35,								// 15仓水插头type2
	PLC_EC_ID_36 = 36,								// 16仓水插头type2
	PLC_EC_ID_37 = 37,								// 17仓水插头type2
	PLC_EC_ID_38 = 38,								// 18仓水插头type2
	PLC_EC_ID_39 = 39,								// 19仓水插头type2
	PLC_EC_ID_40 = 40,								// 20仓水插头type2
	PLC_EC_ID_41 = 41,								// 1仓电插头type1
	PLC_EC_ID_42 = 42,								// 2仓电插头type1
	PLC_EC_ID_43 = 43,								// 3仓电插头type1
	PLC_EC_ID_44 = 44,								// 4仓电插头type1
	PLC_EC_ID_45 = 45,								// 5仓电插头type1
	PLC_EC_ID_46 = 46,								// 6仓电插头type1
	PLC_EC_ID_47 = 47,								// 7仓电插头type1
	PLC_EC_ID_48 = 48,								// 8仓电插头type1
	PLC_EC_ID_49 = 49,								// 9仓电插头type1
	PLC_EC_ID_50 = 50,								// 10仓电插头type1
	PLC_EC_ID_51 = 51,								// 11仓电插头type1	
	PLC_EC_ID_52 = 52,								// 12仓电插头type1
	PLC_EC_ID_53 = 53,								// 13仓电插头type1
	PLC_EC_ID_54 = 54,								// 14仓电插头type1
	PLC_EC_ID_55 = 55,								// 15仓电插头type1
	PLC_EC_ID_56 = 56,								// 16仓电插头type1
	PLC_EC_ID_57 = 57,								// 17仓电插头type1
	PLC_EC_ID_58 = 58,								// 18仓电插头type1
	PLC_EC_ID_59 = 59,								// 19仓电插头type1
	PLC_EC_ID_60 = 60,								// 20仓电插头type1
	PLC_EC_ID_61 = 61,								// 21仓电插头type1
	PLC_EC_ID_62 = 62,								// 1仓电插头type2
	PLC_EC_ID_63 = 63,								// 2仓电插头type2
	PLC_EC_ID_64 = 64,								// 3仓电插头type2	
	PLC_EC_ID_65 = 65,								// 4仓电插头type2
	PLC_EC_ID_66 = 66,								// 5仓电插头type2
	PLC_EC_ID_67 = 67,								// 6仓电插头type2
	PLC_EC_ID_68 = 68,								// 7仓电插头type2
	PLC_EC_ID_69 = 69,								// 8仓电插头type2
	PLC_EC_ID_70 = 70,								// 9仓电插头type2
	PLC_EC_ID_71 = 71,								// 10仓电插头type2
	PLC_EC_ID_72 = 72,								// 11仓电插头type2
	PLC_EC_ID_73 = 73,								// 12仓电插头type2	
	PLC_EC_ID_74 = 74,								// 13仓电插头type2
	PLC_EC_ID_75 = 75,								// 14仓电插头type2
	PLC_EC_ID_76 = 76,								// 15仓电插头type2	
	PLC_EC_ID_77 = 77,								// 16仓电插头type2
	PLC_EC_ID_78 = 78,								// 17仓电插头type2
	PLC_EC_ID_79 = 79,								// 18仓电插头type2
	PLC_EC_ID_80 = 80,								// 19仓电插头type2
	PLC_EC_ID_81 = 81,								// 20仓电插头type2
	PLC_EC_ID_82 = 82,								// 21仓电插头type2
	PLC_EC_ID_83 = 83,								// 消防仓前挡块
	PLC_EC_ID_84 = 84,								// 消防仓后挡块
	PLC_EC_ID_85 = 85,								// 平台区前挡块	
	PLC_EC_ID_86 = 86,								// 平台区后挡块
	PLC_EC_ID_88 = 88,								// 右缓存位前挡块
	PLC_EC_ID_89 = 89,								// 右缓存位后挡块
	PLC_EC_ID_90 = 90,								// V槽左挡块	
	PLC_EC_ID_91 = 91,								// V槽右挡块
	
	PLC_EC_ID_MAX
}PLC_EC_ID_ENUM;

/**
 *@brief 电池槽ID定义
 **/
typedef enum
{
	PLC_SLOT_ID_MIN   							= 0,
	PLC_SLOT_ID_1     							= 1,
	PLC_SLOT_ID_2     							= 2,
	PLC_SLOT_ID_3     							= 3,
	PLC_SLOT_ID_4     							= 4,
	PLC_SLOT_ID_5     							= 5,
	PLC_SLOT_ID_6     							= 6,
	PLC_SLOT_ID_7     							= 7,
	PLC_SLOT_ID_8     							= 8,
	PLC_SLOT_ID_9     							= 9,
	PLC_SLOT_ID_10    							= 10,
	PLC_SLOT_ID_11    							= 11,
	PLC_SLOT_ID_12    							= 12,
	PLC_SLOT_ID_13    							= 13,
	PLC_SLOT_ID_14    							= 14,
	PLC_SLOT_ID_15    							= 15,
	PLC_SLOT_ID_16    							= 16,
	PLC_SLOT_ID_17    							= 17,
	PLC_SLOT_ID_18    							= 18,
	PLC_SLOT_ID_19    							= 19,
	PLC_SLOT_ID_20    							= 20,
	PLC_SLOT_ID_21    							= 21,
	PLC_SLOT_ID_22    							= 22,
	PLC_SLOT_ID_23    							= 23,
	PLC_SLOT_ID_MAX  
} PLC_SLOT_ID_ENUM; 

/**
 *@brief LR Y方向工位枚举值
 **/
typedef enum
{
	PLC_LR_Y_POS_MIN           					= 0,
	PLC_LR_Y_POS_HOME          					= 1,// 原点位
	PLC_LR_Y_POS_FIX           					= 2,// 卡销位 电池
	PLC_LR_Y_POS_PIN_EXTEND    					= 3,// 销子位 车身
	PLC_LR_Y_POS_PLUG_APPROACH 					= 4,// 插头位 (PLC自控，无需主控下发)
	PLC_LR_Y_POS_LOCK_UNLOCK          			= 5,// 加解锁位
	PLC_LR_Y_POS_UNKNOWN       					= 6,// 未知
	PLC_LR_Y_POS_MAX
}PLC_LR_Y_POS_ENUM;

/**
 *@brief LR X方向工位枚举值
 **/
typedef enum
{
	PLC_LR_X_POS_MIN           					= 0,
	PLC_LR_X_POS_HOME          					= 1,//原点位
	PLC_LR_X_POS_WORK           				= 2,//工作位	
	PLC_LR_X_POS_MAX
}PLC_LR_X_POS_ENUM;


/**
 *@brief LR pin车身定位销枚举值
 **/
// typedef enum
// {
// 	PLC_LR_PIN_MIN   							= 0,
// 	PLC_LR_PIN_L_FRONT 							= 26, //左前
// 	PLC_LR_PIN_L_BACK  							= 27, //左后
// 	PLC_LR_PIN_R_BACK  							= 28, //右后
// 	PLC_LR_PIN_MAX
// }PLC_LR_PIN_ENUM;
    
/**
 *@brief LR pin工位枚举值
 **/
typedef enum
{
	PLC_LR_PIN_POS_MIN           				= 0,
	PLC_LR_PIN_POS_HOME          				= 1,
	PLC_LR_PIN_POS_WORK          				= 2,
	PLC_LR_PIN_POS_UNKNOWN       				= 3,
	PLC_LR_PIN_POS_MAX
}PLC_LR_PIN_POS_ENUM;

/**
 *@brief 升降机Y方向工位枚举值
 **/
typedef enum
{
	PLC_BL_Y_POS_MIN   							= -1,
	PLC_BL_Y_POS_HOME  							= 0,//接驳仓对接位置
	PLC_BL_Y_POS_01     						= 1,
	PLC_BL_Y_POS_02     						= 2,
	PLC_BL_Y_POS_03     						= 3,
	PLC_BL_Y_POS_04     						= 4,
	PLC_BL_Y_POS_05     						= 5,
	PLC_BL_Y_POS_06     						= 6,
	PLC_BL_Y_POS_07     						= 7,
	PLC_BL_Y_POS_08     						= 8,
	PLC_BL_Y_POS_09     						= 9,
	PLC_BL_Y_POS_10     						= 10,
	PLC_BL_Y_POS_11     						= 11,
	PLC_BL_Y_POS_12     						= 12,
	PLC_BL_Y_POS_13     						= 13,
	PLC_BL_Y_POS_14     						= 14,
	PLC_BL_Y_POS_15     						= 15,
	PLC_BL_Y_POS_16     						= 16,
	PLC_BL_Y_POS_17     						= 17,
	PLC_BL_Y_POS_18     						= 18,
	PLC_BL_Y_POS_19     						= 19,
	PLC_BL_Y_POS_20    							= 20,
	PLC_BL_Y_POS_21     						= 21,						
	PLC_BL_Y_POS_MAX
}PLC_BL_Y_POS_ENUM;


/**
 *@brief 开合门工位枚举值
 **/
typedef enum
{
	PLC_DOOR_ID_MIN  							= 0,
	PLC_DOOR_ID_01   							= 1,// 左开合门
	PLC_DOOR_ID_02   							= 2,// 右开合门
	PLC_DOOR_ID_MAX
}PLC_DOOR_ID_ENUM;
    
/**
 *@brief 开合门动作枚举值
 **/
typedef enum
{
	PLC_DOOR_STATE_MIN      					= 0,
	PLC_DOOR_STATE_CLOSE    					= 1,// 关闭
	PLC_DOOR_STATE_OPEN     					= 2,// 打开
	PLC_DOOR_STATE_MAX
}PLC_DOOR_STATE_ENUM;
    
/**
 *@brief 运动状态枚举值
 **/
typedef enum
{
	PLC_MOTION_STATE_MIN      					= -1,
	PLC_MOTION_STATE_IDLE     					= 0,
	PLC_MOTION_STATE_ONGOING  					= 1,
	PLC_MOTION_STATE_FINISHED 					= 2,
	PLC_MOTION_STATE_UNKNOWN,
	PLC_MOTION_STATE_MAX
}PLC_MOTION_STATE_ENUM;

/**
 *@brief 零点标定状态枚举值
 **/
typedef enum
{
	PLC_ZERO_CALIB_STATE_MIN 					= -1,
	PLC_ZERO_CALIB_STATE_IDLE 					= 0,
	PLC_ZERO_CALIB_STATE_SUCCESS 				= 1,
	PLC_ZERO_CALIB_STATE_FAILED 				= 2,
	PLC_ZERO_CALIB_STATE_UNKNOWN,
	PLC_ZERO_CALIB_STATE_MAX
} PLC_ZERO_CALIB_STATE_ENUM;

/**
 *@brief 一键加解锁状态枚举值
 **/
typedef enum
{
	PLC_ONECLICK_LOCK_UNLOCK_STATE_MIN 			= -1,
	PLC_ONECLICK_LOCK_UNLOCK_STATE_IDLE 		= 0,
	PLC_ONECLICK_LOCK_STATE_SUCCESS 			= 1,
	PLC_ONECLICK_LOCK_STATE_FAILED 				= 2,
	PLC_ONECLICK_UNLOCK_STATE_SUCCESS 			= 3,
	PLC_ONECLICK_UNLOCK_STATE_FAILED 			= 4,
	PLC_ONECLICK_LOCK_UNLOCK_STATE_UNKNOWN,
	PLC_ONECLICK_LOCK_UNLOCK_STATE_MAX
} PLC_ONECLICK_LOCK_UNLOCK_STATE_ENUM;

/**
 *@brief 正反转枚举值
 **/
typedef enum
{
	PLC_DIRECTION_MIN         					= 0,
	PLC_DIRECTION_POSITIVE    					= 1,
	PLC_DIRECTION_NEGATIVE    					= 2,
	PLC_DIRECTION_MAX
}PLC_DIRECTION_ENUM;
    
/**
 *@brief 电缸伸出、缩回枚举值
 **/
typedef enum
{
	PLC_EC_POS_MIN     							= 0,
	PLC_EC_POS_EXTEND   						= 1,
	PLC_EC_POS_RETRACT  						= 2,
	PLC_EC_POS_MAX
}PLC_EC_POS_ENUM;

/**
 *@brief 电磁铁吸合枚举值
 **/
typedef enum
{
	PLC_ELECTROMAGNET_STATE_MIN   				= 0,
	PLC_ELECTROMAGNET_STATE_ENABLE 				= 1,// 吸合
	PLC_ELECTROMAGNET_STATE_DISABLE  			= 2,// 松开
	PLC_ELECTROMAGNET_STATE_MAX
}PLC_ELECTROMAGNET_STATE_ENUM;
    

/**
 *@brief 停车举升平台工位枚举值
 **/
typedef enum
{
	PLC_VP_POS_MIN              				= 0,
	PLC_VP_POS_LIFT_HOME        				,
	PLC_VP_POS_LIFT_TOUCH       				,
	PLC_VP_POS_LIFT_WORK        				,
	PLC_VP_POS_LIFT_TOP         				,//维修位
	PLC_VP_POS_CLAMP_1_HOME     				,
	PLC_VP_POS_CLAMP_1_WORK     				,
	PLC_VP_POS_CLAMP_2_HOME     				,
	PLC_VP_POS_CLAMP_2_WORK     				,
	PLC_VP_POS_CLAMP_3_HOME     				,
	PLC_VP_POS_CLAMP_3_WORK     				,
	PLC_VP_POS_CLAMP_4_HOME     				,
	PLC_VP_POS_CLAMP_4_WORK     				,
	PLC_VP_POS_V_HOME    	    				,
	PLC_VP_POS_V_WORK    	    				,
	PLC_VP_POS_MAX
}PLC_VP_POS_ENUM;
    
/**
 *@brief 电池存在定义
 **/
typedef enum
{
	PLC_BATTERY_EXISTENCE_MIN     				= 0,
	PLC_BATTERY_EXISTENCE_N       				= 1,// 没电池
	PLC_BATTERY_EXISTENCE_Y       				= 2,// 有电池
	PLC_BATTERY_EXISTENCE_UNKNOWN ,					// 未知
	PLC_BATTERY_EXISTENCE_MAX
}PLC_BATTERY_EXISTENCE_ENUM; 

/**
 *@brief 车辆存在定义
 **/
typedef enum
{
	PLC_VEHICLE_EXISTENCE_MIN     				= -1,
	PLC_VEHICLE_EXISTENCE_N       				= 0, 
	PLC_VEHICLE_EXISTENCE_Y       				= 1, 
	PLC_VEHICLE_EXISTENCE_UNKNOWN ,					//未知
	PLC_VEHICLE_EXISTENCE_MAX
}PLC_VEHICLE_EXISTENCE_ENUM; 

/**
 *@brief 设备枚举值
 **/
typedef enum
{
	PLC_DEVICE_MIN      						= -1, 
	PLC_DEVICE_BC       						= 0, // 电池仓
	PLC_DEVICE_BL       						= 1, // 升降机
	PLC_DEVICE_LR       						= 2, // LR
	PLC_DEVICE_VP       						= 3, // 车辆停车平台
	PLC_DEVICE_BF       						= 4, // 缓存台
  	PLC_DEVICE_MAX 
}PLC_DEVICE_ENUM;

/**
 *@brief JOB_ID 枚举
 */
typedef enum
{
	JOB_PREPARE_UNLOAD_BATTERY					= 5,  // 拆电池准备
	JOB_UNLOAD_BATTERY        					= 10, // 拆电池
	JOB_NEW_BATTERY_PREPATE   					= 20, // 新电池准备
	JOB_PREPARE_LOAD_BATTERY  					= 30, // 装电池准备
	JOB_LOAD_BATTERY          					= 40, // 装电池
	JOB_OLD_BATTERY_RETURN    					= 50, // 旧电池回仓
	JOB_AUTO_SWAP             					= 100 // 自动换电
}PLC_JOB_ID_ENUM;

/**
 *@brief DO 枚举
 */
 typedef enum
{
	PLC_DO_MIN               				  	= 0,
	PLC_DO_ALARM_LIGHT       				  	= 1,  // 消防警灯
	PLC_DO_ALARM_BEET        				  	= 2,  // 消防警铃
	PLC_DO_SWAP_RED								= 3,  // 换电站红灯
	PLC_DO_SWAP_GREEN							= 4,  // 换电站绿灯
	PLC_DO_PHAROS_RED        				  	= 5,  // 塔灯红灯
	PLC_DO_PHAROS_BEET       				  	= 6,  // 塔灯蜂鸣
	PLC_DO_E_STOP            				  	= 7,  // 消防急停断电
	PLC_DO_VISUAL_LIGHT      				  	= 8,  // 视觉光源
	PLC_DO_RESET_CDC							= 9,  // 充电板重启
	PLC_DO_OIL_PUMP								= 10, // 油泵启动
	PLC_DO_NPA_LIQ_PLUG_01  					= 11, // NPA水接头1
	PLC_DO_NPD_LIQ_PLUG_01  					= 12, // NPD水接头1
	PLC_DO_NPA_LIQ_PLUG_02  					= 13, // NPA水接头2
	PLC_DO_NPD_LIQ_PLUG_02  					= 14, // NPD水接头2
	PLC_DO_NPA_LIQ_PLUG_03  					= 15, // NPA水接头3
	PLC_DO_NPD_LIQ_PLUG_03  					= 16, // NPD水接头3
	PLC_DO_NPA_LIQ_PLUG_04  					= 17, // NPA水接头4
	PLC_DO_NPD_LIQ_PLUG_04  					= 18, // NPD水接头4
	PLC_DO_NPA_LIQ_PLUG_05  					= 19, // NPA水接头5
	PLC_DO_NPD_LIQ_PLUG_05  					= 20, // NPD水接头5
	PLC_DO_NPA_LIQ_PLUG_06  					= 21, // NPA水接头6
	PLC_DO_NPD_LIQ_PLUG_06  					= 22, // NPD水接头6
	PLC_DO_NPA_LIQ_PLUG_07  					= 23, // NPA水接头7
	PLC_DO_NPD_LIQ_PLUG_07  					= 24, // NPD水接头7
	PLC_DO_NPA_LIQ_PLUG_08  					= 25, // NPA水接头8
	PLC_DO_NPD_LIQ_PLUG_08  					= 26, // NPD水接头8
	PLC_DO_NPA_LIQ_PLUG_09  					= 27, // NPA水接头9
	PLC_DO_NPD_LIQ_PLUG_09  					= 28, // NPD水接头9
	PLC_DO_NPA_LIQ_PLUG_10  					= 29, // NPA水接头10
	PLC_DO_NPD_LIQ_PLUG_10  					= 30, // NPD水接头10
	PLC_DO_NPA_LIQ_PLUG_11  					= 31, // NPA水接头11
	PLC_DO_NPD_LIQ_PLUG_11  					= 32, // NPD水接头11
	PLC_DO_NPA_LIQ_PLUG_12  					= 33, // NPA水接头12
	PLC_DO_NPD_LIQ_PLUG_12  					= 34, // NPD水接头12
	PLC_DO_NPA_LIQ_PLUG_13  					= 35, // NPA水接头13
	PLC_DO_NPD_LIQ_PLUG_13  					= 36, // NPD水接头13
	PLC_DO_NPA_LIQ_PLUG_14  					= 37, // NPA水接头14
	PLC_DO_NPD_LIQ_PLUG_14  					= 38, // NPD水接头14
	PLC_DO_NPA_LIQ_PLUG_15  					= 39, // NPA水接头15
	PLC_DO_NPD_LIQ_PLUG_15  					= 40, // NPD水接头15
	PLC_DO_NPA_LIQ_PLUG_16  					= 41, // NPA水接头16
	PLC_DO_NPD_LIQ_PLUG_16  					= 42, // NPD水接头16
	PLC_DO_NPA_LIQ_PLUG_17  					= 43, // NPA水接头17
	PLC_DO_NPD_LIQ_PLUG_17  					= 44, // NPD水接头17
	PLC_DO_NPA_LIQ_PLUG_18  					= 45, // NPA水接头18
	PLC_DO_NPD_LIQ_PLUG_18  					= 46, // NPD水接头18
	PLC_DO_NPA_LIQ_PLUG_19  					= 47, // NPA水接头19
	PLC_DO_NPD_LIQ_PLUG_19  					= 48, // NPD水接头19
	PLC_DO_NPA_LIQ_PLUG_20  					= 49, // NPA水接头20
	PLC_DO_NPD_LIQ_PLUG_20  					= 50, // NPD水接头20
	PLC_DO_LIGHT_LOGO							= 51, // LOGO灯
	PLC_DO_LIGHT_PL_1							= 52, // 停车平台灯组1
	PLC_DO_LIGHT_PL_2							= 53, // 停车平台灯组2
	PLC_DO_LIGHT_BC_A							= 54, // A箱灯
	PLC_DO_LIGHT_BC_B							= 55, // B箱灯
	PLC_DO_LIGHT_BC_C							= 56, // C箱灯
	PLC_DO_LIGHT_ASSIST							= 57  // 辅助照明灯
}PLC_DO_ID_ENUM;

/*******************************************************************************/
/******************************* 主控下发至PLC数据 *******************************/
/*******************************************************************************/

/**
 *@brief 控制命令ID数据结构
 **/
typedef enum
{
	PLC_CMD_ID_MIN           		 			= -1,
	PLC_CMD_ID_HEARTBEAT     		 			= 0,  // 心跳
	PLC_CMD_ID_SETTINGS      		 			= 1,  // 参数下载   
	PLC_CMD_ID_STOP          		 			= 2,  // 停机   
	PLC_CMD_ID_PAUSE         		 			= 3,  // 暂停	
	PLC_CMD_ID_CONTINUE      		 			= 4,  // 继续   
	PLC_CMD_ID_RESET         		 			= 5,  // 复位
	PLC_CMD_ID_CHANGE_MODE   		 			= 6,  // 模式切换
	PLC_CMD_ID_INIT          		 			= 7,  // 初始化
	PLC_CMD_ID_HOME_SET      		 			= 8,  // 零点标定
	PLC_CMD_ID_JOG           		 			= 9,  // JOG
	PLC_CMD_ID_MANUAL        		 			= 10, // 单步控制
	PLC_CMD_ID_JOB           		 			= 11, // 半自动 
	PLC_CMD_ID_SETTING_BC_NUMBER 				= 12, // 仓位号下发
	PLC_CMD_ID_DO_CTRL       		 			= 13, // DO控制
	PLC_CMD_ID_PHOTOGRAPH						= 14, // 视觉拍照
	PLC_CMD_ID_FIRE								= 15, // 消防
	PLC_CMD_ID_FIRE_MODE						= 16, // 消防模式
	PLC_CMD_ID_STATION_TYPE						= 17, // 整站类型
	PLC_CMD_ID_PREHEAT							= 18, // 热枪
	PLC_CMD_ID_RESELECT_TARGET_NUMBER			= 19, // 自动换点过程中重新选择目标仓位
	PLC_CMD_ID_REMOTE_RETRY						= 20, // 远程机械重试
	PLC_CMD_ID_WHEEL_ADAPT						= 21, // 轮毂自适应命令
	PLC_CMD_ID_VEHICLE_TYPE						= 22, // 车型选择
	PLC_CMD_ID_PL_CONTINUE_SWAP					= 23, // 停车平台继续换电
	PLC_CMD_ID_CHANGE_BAT					    = 24, // 满电电池倒仓
	PLC_CMD_ID_DROP_BAT					    	= 25, // 电池扔消防仓
	PLC_CMD_ID_LIFT_TYPE						= 26, // 接驳机类型下发
	PLC_CMD_ID_TEMP								= 27, // 站内温度下发
	PLC_CMD_ID_DUTY_MODE						= 28, // 换电站值守模式
	PLC_CMD_ID_RGV_TORQUE						= 29, // RGV下降挂电池扭矩保护
	PLC_CMD_ID_OCC_DROP_BAT						= 30, // OCC远程消防一键落水
	PLC_CMD_ID_TRAILER_CONFIG					= 31, // 不挂车功能配置
	PLC_CMD_ID_SAFE_LIGHT_CONFIG				= 32, // 安全光幕使能配置
	PLC_CMD_ID_DROP_KEY_CONFIG               	= 33, // 落水按键常开改常闭配置
	PLC_CMD_ID_MAX
}PLC_CMD_ID_ENUM;

/**
 *@brief 心跳请求数据包 
 */
typedef struct
{
	int  st;//心跳
}PLC_HB_REQ_STRUCT;

/**
 *@brief 参数设置（收发结构体相同） 60
 */
typedef struct
{	
	int pl_lf_clamp_pos_work;                		// 左前推杆工作位                                                      
  	int pl_lr_clamp_pos_work;                		// 左后推杆工作位                                    
  	int pl_rf_clamp_pos_work;                		// 右前推杆工作位                                    
  	int pl_rr_clamp_pos_work;                		// 右后推杆工作位                                    
  	int pl_v_pos_work;                       		// V槽工作位                              
  	int pl_move_pos_work_NPA;                		// 加解锁平台平移工作位_NPA                                    
  	int pl_move_pos_work_NPD;                		// 加解锁平台平移工作位_NPD                                    
  	int lr_pos_material_fixed;               		// 加解锁平台抬升至卡销位                                      
  	int lr_pos_pin_extend;                   		// 加解锁平台抬升至销子伸出位                                  
  	int lr_pos_plug_approach;                		// 加解锁平台抬升至接近插头位                                    
  	int lr_pos_lock;                         		// 加解锁平台抬升至加解锁位                            
  	int lr_lf_vehicle_fixed_pin_pos_work;    		// 左前车身定位销伸出位                                                
  	int lr_rr_vehicle_fixed_pin_pos_work;    		// 右后车身定位销伸出位                                                
  	int lr_lr_vehicle_fixed_pin_pos_work;    		// 左后车身定位销伸出位                                                
  	int pl_f_guide_pos_work;                 		// 停车平台前导向条伸出位                                    
  	int pl_r_guide_pos_work;                 		// 停车平台后导向条伸出位                                    
  	int door_01_close_pos;                   		// 左开合门关到位                                  
  	int door_02_close_pos;                   		// 右开合门关到位                                  
  	int pl_lifter_pos_work;                  		// 升降仓工作位                                  
  	int stacker_move_f_pos_work;             		// 堆垛机平移至C1_C5                                        
  	int stacker_move_r_pos_work;             		// 堆垛机平移至C6_C10                                        
  	int fork_X_pos_work_01;                  		// 货叉伸出C1_C5                                
  	int fork_X_pos_work_02;                  		// 货叉伸出A1_A5                                
  	int gun1_Z_pos_work;                     		// 1号枪头伸出至工作位                                
  	int gun2_Z_pos_work;                     		// 2号枪头伸出至工位位                                
  	int gun9_Z_pos_work;                     		// 9号枪头伸出至工作位                                
  	int gun10_Z_pos_work;                    		// 10号枪头伸出至工作位                                
  	int gun9_X_pos_work_02;                  		// 9号枪头横移至NPD位                                  
  	int gun10_X_pos_work_02;                 		// 10号枪头横移至NPD位                                    
  	int gun11_Z_pos_work;                    		// 1'号枪头伸出至工作位                                
  	int gun21_Z_pos_work;                    		// 2'号枪头伸出至工位位                                
  	int soft_pos_limit;                      		// 伺服软限位                              
  	int fork_X_pos_work_03;                  		// 货叉接驳位伸出工作位                                  
  	int stacker_lift_low_pos_C1;             		// 堆垛机C1仓低位                                        
  	int stacker_lift_low_pos_C2;             		// 堆垛机C2仓低位                                        
  	int stacker_lift_low_pos_C3;             		// 堆垛机C3仓低位                                        
  	int stacker_lift_low_pos_C4;             		// 堆垛机C4仓低位                                        
  	int stacker_lift_low_pos_C5;             		// 堆垛机C5仓低位                                        
  	int stacker_lift_low_pos_C6;             		// 堆垛机C6仓低位                                        
  	int stacker_lift_low_pos_C7;             		// 堆垛机C7仓低位                                        
  	int stacker_lift_low_pos_C8;             		// 堆垛机C8仓低位                                        
  	int stacker_lift_low_pos_C9;             		// 堆垛机C9仓低位                                        
  	int stacker_lift_low_pos_C10;            		// 堆垛机C10仓低位                                        
  	int stacker_lift_low_pos_A1;             		// 堆垛机A1仓低位                                        
  	int stacker_lift_low_pos_A2;             		// 堆垛机A2仓低位                                        
  	int stacker_lift_low_pos_A3;             		// 堆垛机A3仓低位                                        
  	int stacker_lift_low_pos_A4;             		// 堆垛机A4仓低位                                        
  	int stacker_lift_low_pos_A5;             		// 堆垛机A5仓低位                                        
  	int stacker_lift_low_pos_A6;             		// 堆垛机A6仓低位                                        
  	int stacker_lift_low_pos_A7;             		// 堆垛机A7仓低位                                        
  	int stacker_lift_low_pos_A8;             		// 堆垛机A8仓低位                                        
  	int stacker_lift_low_pos_A9;             		// 堆垛机A9仓低位                                        
  	int stacker_lift_low_pos_A10;            		// 堆垛机A10仓低位                                        
  	int stacker_lift_low_pos_A11;            		// 堆垛机A11仓低位                                        
  	int stacker_lift_low_pos_A12;            		// 消防仓低位  
	int stacker_move_A12_pos_work;           		// 堆垛机平移消防仓位 
  	int fork_X_pos_work_A12;                 		// 货叉消防仓伸出工作位
	int fork_X_pos_work_C6;							// 货叉伸出C6_C10
	int fork_X_pos_work_A6;							// 货叉伸出A6_A11
	int stacker_move_pos_work_A1;					// 堆垛机平移至A1_A5
	int stacker_move_pos_work_A6;					// 堆垛机平移至A6_A11
	int gun_1_8_sign_speed;							// 1~8、1'、2'枪标定速度
	int gun_1_8_sign_torque;						// 1~8、1'、2'枪标定扭矩
	int gun_9_10_sign_speed;						// 9、10枪标定速度
	int gun_9_10_sign_torque;   					// 9、10枪标定扭矩                             
	int reserved[5];                         		// 预留                                          
}PLC_SETTING_STRUCT;


/**
 *@brief 停机 请求数据包 
 */
typedef struct
{
    
}PLC_STOP_REQ_STRUCT;
/**
 *@brief 暂停 请求数据包 
 */
typedef struct
{

}PLC_PAUSE_REQ_STRUCT;
/**
 *@brief 继续 请求数据包 
 */
typedef struct
{
   
}PLC_CONTINUE_REQ_STRUCT;

/**
 *@brief 复位 请求数据包 
 */
typedef struct
{

}PLC_RESET_REQ_STRUCT;

/**
 *@brief 模式切换 请求数据包 
 */
typedef struct
{    
	int mode;//模式切换
	 
}PLC_CHANGE_MODE_REQ_STRUCT;

/**
 *@brief 零点标定 请求数据包 
 */
typedef struct
{    
	int id;//轴号
	 
}PLC_HOME_REQ_STRUCT;

/**
 *@brief JOG 请求数据包 
 */
typedef struct
{    
	int device_type;
	int id;//编号    
	int param3;
	int param4;
	int param5;
	int param6;
	int param7;
	int param8;
	 
}PLC_JOG_REQ_STRUCT;

/**
 *@brief MANUAL 请求数据包 
 */
typedef struct
{    
	int device_type;
	int id;//编号    
	int param3;
	int param4;
	int param5;
	int param6;
	int param7;
	int param8;
}PLC_MANUAL_REQ_STRUCT;

/**
 *@brief JOB 请求数据包 
 */
typedef struct
{    
	int id;	
	int param2;
	int param3;
	int param4;
	int param5;
	int param6;
	int param7;
	int param8;
}PLC_JOB_REQ_STRUCT;

/**
 *@brief DO控制数据包 
 */
typedef struct
{  
	int id;
	int param2;
}PLC_CMD_DO_CTRL_STRUCT;

/**
 *@brief 视觉拍照请求数据包
 */
typedef struct
{
	int param1;	 //车辆定位_01_定位状态
	int param2;	 //亏电池下表面视觉状态
	int param3;	 //服务电池上表面视觉状态
	int param4;	 //车辆定位_02_定位状态
	int param5;	 //服务电池下表面视觉状态
	int param6;	 //亏电电池上表面视觉状态
	int reserved[9]; //预留
}PLC_PHOTOGRAPH_REQ_STRUCT;

/**
 *@brief 消防请求数据包 
 */
typedef struct
{
	int param1;  //消防仓位号
	int param2;  //是否有车 0：无，1：有
	int param3;	//是否扔水箱 0:不使能，1:使能
	int param4;	// 消防转运类型 1:本地自动转运，2:云端远程转运
}PLC_FIRE_REQ_STRUCT;


/*******************************************************************************/
/******************************* PLC上送至主控数据 *******************************/
/*******************************************************************************/
 
/**
 *@brief 接收PLC数据长度
 */
typedef struct 
{
	int16_t msg_size;
}PLC_MSG_SIZE_STRUCT;

/**
 *@brief 接收PLC模式
 */
typedef struct 
{
	int16_t work_mode;
}PLC_MODE_STRUCT;

/**
 *@brief 轴的数据结构定义
 */
typedef struct
{
	bool moving;
	bool stand_still;
	bool syn_mode;
	bool stopping;
	bool fault;
	bool warning;
	int16_t id;
	int32_t fault_id;
	int16_t warning_id; 
	int16_t servo_mode;
	int16_t torque_actual_value;
	int64_t pos_actual_value; 
	int32_t velocity_actual_value;
}PLC_AXIS_STRUCT;

/**
 *@brief 加解锁平台数据结构定义 25个轴
 */
typedef struct
{
	PLC_AXIS_STRUCT axis[25]; 							// 1-12：12个枪；13：左前定位销；14：右后定位销；15：左后定位销；16：加解锁平台升降；17：加解锁平台平移18：1枪升降；19：2枪升降；20：9枪平移；21：9枪升降；22：10枪平移；23：10枪升降；24：1'枪升降；25：2'枪升降；
	bool battery_exist;
}PLC_LR_STRUCT;

/**
 *@brief 电池仓数据结构定义 4个轴
 */
typedef struct
{
  PLC_AXIS_STRUCT axis[4];								// 1：堆垛机平移；2：堆垛机升降；3：货叉;4：升降仓
  bool battery_exist[24];								// 0：堆垛机；1-21：仓位；22:消防仓；23:升降仓；
}PLC_BC_STRUCT;

/**
 *@brief 停车平台数据结构定义 9个轴
 */
typedef struct
{
	PLC_AXIS_STRUCT axis[9]; 							// 1：左前推杆；2：右前推杆；3：左后推杆；4：右后推杆；5：V槽；6：前导向条；7：后导向条；8：左开合门；9：右开合门
	bool vehicle_exist;
}PLC_VP_STRUCT;

/**
 *@brief 传感器数据结构定义 500个
 */
typedef struct
{
	bool roller_door_01_up_limt;						// 前卷帘门上到位										
	bool roller_door_01_down_limt;						// 前卷帘门下到位										
	bool roller_door_02_up_limt;						// 后卷帘门上到位										
	bool roller_door_02_down_limt;						// 后卷帘门下到位										
	bool front_roller_door_safety_01;					// 前卷帘门安全保护1											
	bool front_roller_door_safety_02;					// 前卷帘门安全保护2											
	bool rear_roller_door_safety_01;					// 后卷帘门安全保护1											
	bool rear_roller_door_safety_02;					// 后卷帘门安全保护2											
	bool maintain_area_safety_01;						// 维护门安全继电器反馈							
	bool maintain_area_safety_02;						// 维护门传感器		    									
	bool pl_buffer_dece_sensor_1;						// 左缓存区电池减速										
	bool pl_buffer_sensor_f_1;							// 左缓存区前电池到位									
	bool pl_buffer_sensor_r_1;							// 左缓存区后电池到位									
	bool pl_lf_clamp_home_sensor;						// 左前轮推杆原点										
	bool pl_lf_V_check_sensor;							// 左前轮进槽									
	bool pl_l_V_lock_extend_sensor;						// V槽左锁止上到位										
	bool pl_l_V_lock_retract_sensor;					// V槽左锁止下到位											
	bool pl_rf_clamp_home_sensor;						// 右前轮推杆原点										
	bool pl_rf_V_check_sensor;							// 右前轮进槽									
	bool pl_r_V_lock_extend_sensor;						// V槽右锁止上到位										
	bool pl_r_V_lock_retract_sensor;					// V槽右锁止下到位											
	bool pl_f_guide_work_sensor;						// 前导向条前到位										
	bool pl_f_guide_home_sensor;						// 前导向条后到位										
	bool pl_r_guide_work_sensor;						// 后导向条前到位										
	bool pl_r_guide_home_sensor;						// 后导向条后到位										
	bool pl_lr_clamp_home_sensor;						// 左后轮推杆原点										
	bool pl_rr_clamp_home_sensor;						// 右后轮推杆原点										
	bool pl_door_01_open_sensor;						// 左开合门开到位										
	bool pl_door_01_close_sensor;						// 左开合门关到位										
	bool pl_door_02_open_sensor;						// 右开合门开到位										
	bool pl_door_02_close_sensor;						// 右开合门关到位										
	bool pl_door_close_safe_sensor;						// 开合门闭合安全										
	bool bc_lift_dece_sensor;							// 接驳位减速									
	bool bc_lift_reach_sensor_f;						// 接驳位前到位										
	bool bc_lift_reach_sensor_r;						// 接驳位后到位										
	bool bc_lift_work_sensor;							// 接驳位举升工作位									
	bool pl_buffer_dece_sensor_2;						// 右缓存区电池减速										
	bool pl_buffer_sensor_f_2;							// 右缓存区前电池到位									
	bool pl_buffer_sensor_r_2;							// 右缓存区后电池到位									
	bool buffer_stopper_01_extend_sensor_02;			// 右缓存区前电池阻挡工作位													
	bool buffer_stopper_01_retract_sensor_02;			// 右缓存区前电池阻挡原点位													
	bool buffer_stopper_02_extend_sensor_02;			// 右缓存区后电池阻挡工作位													
	bool buffer_stopper_02_retract_sensor_02;			// 右缓存区后电池阻挡原点位													
	bool RGV_bc_reach_sensor_01;						// 电池平整1										
	bool RGV_bc_reach_sensor_02;						// 电池平整2										
	bool RGV_bc_reach_sensor_03;						// 电池平整3										
	bool RGV_bc_reach_sensor_04;						// 电池平整4										
	bool RGV_bc_reach_sensor_05;						// 电池平整5										
	bool RGV_bc_reach_sensor_06;						// 电池平整6										
	bool lf_pin_extend_sensor;							// 左前车身定位销上到位									
	bool lf_pin_retract_sensor;							// 左前车身定位销下到位									
	bool lf_pin_touch_sensor;							// 左前车身定位销接触车身									
	bool rr_pin_extend_sensor;							// 右后车身定位销上到位									
	bool rr_pin_retract_sensor;							// 右后车身定位销下到位									
	bool rr_pin_touch_sensor;							// 右后车身定位销接触车身									
	bool lr_pin_extend_sensor;							// 左后车身定位销上到位									
	bool lr_pin_retract_sensor;							// 左后车身定位销下到位									
	bool lr_pin_touch_sensor;							// 左后车身定位销接触车身									
	bool gun1_lift_work_sensor;							// 1#升降上到位									
	bool gun1_lift_home_sensor;							// 1#升降下到位									
	bool gun2_lift_work_sensor;							// 2#升降上到位									
	bool gun2_lift_home_sensor;							// 2#升降下到位									
	bool gun9_move_home_sensor;							// 9#平移位置1									
	bool gun9_move_work_sensor;							// 9#平移位置2									
	bool gun9_lift_work_sensor;							// 9#升降上到位									
	bool gun9_lift_home_sensor;							// 9#升降下到位									
	bool gun10_move_home_sensor;						// 10#平移位置1										
	bool gun10_move_work_sensor;						// 10#平移位置2										
	bool gun10_lift_work_sensor;						// 10#升降上到位										
	bool gun10_lift_home_sensor;						// 10#升降下到位										
	bool gun11_lift_work_sensor;						// 11#升降上到位										
	bool gun11_lift_home_sensor;						// 11#升降下到位										
	bool gun12_lift_work_sensor;						// 12#升降上到位										
	bool gun12_lift_home_sensor;						// 12#升降下到位										
	bool RGV_work_sensor;								// RGV举升工作位								
	bool RGV_maintain_sensor;							// RGV举升维护位									
	bool pl_stopper_01_home_sensor;						// 前电池阻挡升降原点位										
	bool pl_stopper_01_work_sensor;						// 前电池阻挡升降工作位										
	bool pl_stopper_01_reach_sensor;					// 前电池阻挡电池到位											
	bool pl_stopper_02_home_sensor;						// 后电池阻挡升降原点位										
	bool pl_stopper_02_work_sensor;						// 后电池阻挡升降工作位										
	bool pl_stopper_02_reach_sensor;					// 后电池阻挡电池到位											
	bool pl_move_work_sensor_1;							// RGV平移 传送位									
	bool pl_move_work_sensor_2;							// RGV平移 NPA位									
	bool pl_move_work_sensor_3;							// RGV平移 NPD位									
	bool pl_move_work_sensor_4;							// RGV平移备用1									
	bool pl_move_work_sensor_5;							// RGV平移备用2	
	bool pl_stopper_01_dece_sensor;						// 前电池阻挡电池减速						
	bool bc_slot1_ec_retract_sensor_1;					// 1仓NPA电插头上到位											
	bool bc_slot1_ec_extend_sensor_1;					// 1仓NPA电插头下到位											
	bool bc_slot1_lc_retract_sensor_1;					// 1仓NPA水插头上到位											
	bool bc_slot1_lc_extend_sensor_1;					// 1仓NPA水插头下到位											
	bool bc_slot1_ec_retract_sensor_2;					// 1仓NPD电插头上到位											
	bool bc_slot1_ec_extend_sensor_2;					// 1仓NPD电插头下到位											
	bool bc_slot1_lc_retract_sensor_2;					// 1仓NPD水插头上到位											
	bool bc_slot1_lc_extend_sensor_2;					// 1仓NPD水插头下到位											
	bool bc_slot1_check_sensor_1;						// 1仓电池区分NPA										
	bool bc_slot1_check_sensor_2;						// 1仓电池区分NPD										
	bool bc_slot1_reached_sensor;						// 1仓电池落到位										
	bool bc_slot1_smoke_sensor;							// 1仓烟雾报警									
	bool bc_slot1_liq_flow_switch_st;					// 1仓水冷流量开关											
	bool bc_sum_smoke_sensor;							// 电池仓整体烟雾									
	bool bc_slot2_ec_retract_sensor_1;					// 2仓NPA电插头上到位											
	bool bc_slot2_ec_extend_sensor_1;					// 2仓NPA电插头下到位											
	bool bc_slot2_lc_retract_sensor_1;					// 2仓NPA水插头上到位											
	bool bc_slot2_lc_extend_sensor_1;					// 2仓NPA水插头下到位											
	bool bc_slot2_ec_retract_sensor_2;					// 2仓NPD电插头上到位											
	bool bc_slot2_ec_extend_sensor_2;					// 2仓NPD电插头下到位											
	bool bc_slot2_lc_retract_sensor_2;					// 2仓NPD水插头上到位											
	bool bc_slot2_lc_extend_sensor_2;					// 2仓NPD水插头下到位											
	bool bc_slot2_check_sensor_1;						// 2仓电池区分NPA										
	bool bc_slot2_check_sensor_2;						// 2仓电池区分NPD										
	bool bc_slot2_reached_sensor;						// 2仓电池落到位										
	bool bc_slot2_smoke_sensor;							// 2仓烟雾报警									
	bool bc_slot2_liq_flow_switch_st;					// 2仓水冷流量开关											
	bool bc_slot3_ec_retract_sensor_1;					// 3仓NPA电插头上到位											
	bool bc_slot3_ec_extend_sensor_1;					// 3仓NPA电插头下到位											
	bool bc_slot3_lc_retract_sensor_1;					// 3仓NPA水插头上到位											
	bool bc_slot3_lc_extend_sensor_1;					// 3仓NPA水插头下到位											
	bool bc_slot3_ec_retract_sensor_2;					// 3仓NPD电插头上到位											
	bool bc_slot3_ec_extend_sensor_2;					// 3仓NPD电插头下到位											
	bool bc_slot3_lc_retract_sensor_2;					// 3仓NPD水插头上到位											
	bool bc_slot3_lc_extend_sensor_2;					// 3仓NPD水插头下到位											
	bool bc_slot3_check_sensor_1;						// 3仓电池区分NPA										
	bool bc_slot3_check_sensor_2;						// 3仓电池区分NPD										
	bool bc_slot3_reached_sensor;						// 3仓电池落到位										
	bool bc_slot3_smoke_sensor;							// 3仓烟雾报警									
	bool bc_slot3_liq_flow_switch_st;					// 3仓水冷流量开关											
	bool bc_slot4_ec_retract_sensor_1;					// 4仓NPA电插头上到位											
	bool bc_slot4_ec_extend_sensor_1;					// 4仓NPA电插头下到位											
	bool bc_slot4_lc_retract_sensor_1;					// 4仓NPA水插头上到位											
	bool bc_slot4_lc_extend_sensor_1;					// 4仓NPA水插头下到位											
	bool bc_slot4_ec_retract_sensor_2;					// 4仓NPD电插头上到位											
	bool bc_slot4_ec_extend_sensor_2;					// 4仓NPD电插头下到位											
	bool bc_slot4_lc_retract_sensor_2;					// 4仓NPD水插头上到位											
	bool bc_slot4_lc_extend_sensor_2;					// 4仓NPD水插头下到位											
	bool bc_slot4_check_sensor_1;						// 4仓电池区分NPA										
	bool bc_slot4_check_sensor_2;						// 4仓电池区分NPD										
	bool bc_slot4_reached_sensor;						// 4仓电池落到位										
	bool bc_slot4_smoke_sensor;							// 4仓烟雾报警									
	bool bc_slot4_liq_flow_switch_st;					// 4仓水冷流量开关											
	bool bc_slot5_ec_retract_sensor_1;					// 5仓NPA电插头上到位											
	bool bc_slot5_ec_extend_sensor_1;					// 5仓NPA电插头下到位											
	bool bc_slot5_lc_retract_sensor_1;					// 5仓NPA水插头上到位											
	bool bc_slot5_lc_extend_sensor_1;					// 5仓NPA水插头下到位											
	bool bc_slot5_ec_retract_sensor_2;					// 5仓NPD电插头上到位											
	bool bc_slot5_ec_extend_sensor_2;					// 5仓NPD电插头下到位											
	bool bc_slot5_lc_retract_sensor_2;					// 5仓NPD水插头上到位											
	bool bc_slot5_lc_extend_sensor_2;					// 5仓NPD水插头下到位											
	bool bc_slot5_check_sensor_1;						// 5仓电池区分NPA										
	bool bc_slot5_check_sensor_2;						// 5仓电池区分NPD										
	bool bc_slot5_reached_sensor;						// 5仓电池落到位										
	bool bc_slot5_smoke_sensor;							// 5仓烟雾报警									
	bool bc_slot5_liq_flow_switch_st;					// 5仓水冷流量开关											
	bool bc_slot1_5_pressure_switch_st;					// 1~5仓水冷压力开关											
	bool bc_slot6_ec_retract_sensor_1;					// 6仓NPA电插头上到位											
	bool bc_slot6_ec_extend_sensor_1;					// 6仓NPA电插头下到位											
	bool bc_slot6_lc_retract_sensor_1;					// 6仓NPA水插头上到位											
	bool bc_slot6_lc_extend_sensor_1;					// 6仓NPA水插头下到位											
	bool bc_slot6_ec_retract_sensor_2;					// 6仓NPD电插头上到位											
	bool bc_slot6_ec_extend_sensor_2;					// 6仓NPD电插头下到位											
	bool bc_slot6_lc_retract_sensor_2;					// 6仓NPD水插头上到位											
	bool bc_slot6_lc_extend_sensor_2;					// 6仓NPD水插头下到位											
	bool bc_slot6_check_sensor_1;						// 6仓电池区分NPA										
	bool bc_slot6_check_sensor_2;						// 6仓电池区分NPD										
	bool bc_slot6_reached_sensor;						// 6仓电池落到位										
	bool bc_slot6_smoke_sensor;							// 6仓烟雾报警									
	bool bc_slot6_liq_flow_switch_st;					// 6仓水冷流量开关											
	bool bc_slot7_ec_retract_sensor_1;					// 7仓NPA电插头上到位											
	bool bc_slot7_ec_extend_sensor_1;					// 7仓NPA电插头下到位											
	bool bc_slot7_lc_retract_sensor_1;					// 7仓NPA水插头上到位											
	bool bc_slot7_lc_extend_sensor_1;					// 7仓NPA水插头下到位											
	bool bc_slot7_ec_retract_sensor_2;					// 7仓NPD电插头上到位											
	bool bc_slot7_ec_extend_sensor_2;					// 7仓NPD电插头下到位											
	bool bc_slot7_lc_retract_sensor_2;					// 7仓NPD水插头上到位											
	bool bc_slot7_lc_extend_sensor_2;					// 7仓NPD水插头下到位											
	bool bc_slot7_check_sensor_1;						// 7仓电池区分NPA										
	bool bc_slot7_check_sensor_2;						// 7仓电池区分NPD										
	bool bc_slot7_reached_sensor;						// 7仓电池落到位										
	bool bc_slot7_smoke_sensor;							// 7仓烟雾报警									
	bool bc_slot7_liq_flow_switch_st;					// 7仓水冷流量开关											
	bool bc_slot8_ec_retract_sensor_1;					// 8仓NPA电插头上到位											
	bool bc_slot8_ec_extend_sensor_1;					// 8仓NPA电插头下到位											
	bool bc_slot8_lc_retract_sensor_1;					// 8仓NPA水插头上到位											
	bool bc_slot8_lc_extend_sensor_1;					// 8仓NPA水插头下到位											
	bool bc_slot8_ec_retract_sensor_2;					// 8仓NPD电插头上到位											
	bool bc_slot8_ec_extend_sensor_2;					// 8仓NPD电插头下到位											
	bool bc_slot8_lc_retract_sensor_2;					// 8仓NPD水插头上到位											
	bool bc_slot8_lc_extend_sensor_2;					// 8仓NPD水插头下到位											
	bool bc_slot8_check_sensor_1;						// 8仓电池区分NPA										
	bool bc_slot8_check_sensor_2;						// 8仓电池区分NPD										
	bool bc_slot8_reached_sensor;						// 8仓电池落到位										
	bool bc_slot8_smoke_sensor;							// 8仓烟雾报警									
	bool bc_slot8_liq_flow_switch_st;					// 8仓水冷流量开关											
	bool bc_slot9_ec_retract_sensor_1;					// 9仓NPA电插头上到位											
	bool bc_slot9_ec_extend_sensor_1;					// 9仓NPA电插头下到位											
	bool bc_slot9_lc_retract_sensor_1;					// 9仓NPA水插头上到位											
	bool bc_slot9_lc_extend_sensor_1;					// 9仓NPA水插头下到位											
	bool bc_slot9_ec_retract_sensor_2;					// 9仓NPD电插头上到位											
	bool bc_slot9_ec_extend_sensor_2;					// 9仓NPD电插头下到位											
	bool bc_slot9_lc_retract_sensor_2;					// 9仓NPD水插头上到位											
	bool bc_slot9_lc_extend_sensor_2;					// 9仓NPD水插头下到位											
	bool bc_slot9_check_sensor_1;						// 9仓电池区分NPA										
	bool bc_slot9_check_sensor_2;						// 9仓电池区分NPD										
	bool bc_slot9_reached_sensor;						// 9仓电池落到位										
	bool bc_slot9_smoke_sensor;							// 9仓烟雾报警									
	bool bc_slot9_liq_flow_switch_st;					// 9仓水冷流量开关											
	bool bc_slot10_ec_retract_sensor_1;					// 10仓NPA电插头上到位											
	bool bc_slot10_ec_extend_sensor_1;					// 10仓NPA电插头下到位											
	bool bc_slot10_lc_retract_sensor_1;					// 10仓NPA水插头上到位											
	bool bc_slot10_lc_extend_sensor_1;					// 10仓NPA水插头下到位											
	bool bc_slot10_ec_retract_sensor_2;					// 10仓NPD电插头上到位											
	bool bc_slot10_ec_extend_sensor_2;					// 10仓NPD电插头下到位											
	bool bc_slot10_lc_retract_sensor_2;					// 10仓NPD水插头上到位											
	bool bc_slot10_lc_extend_sensor_2;					// 10仓NPD水插头下到位											
	bool bc_slot10_check_sensor_1;						// 10仓电池区分NPA										
	bool bc_slot10_check_sensor_2;						// 10仓电池区分NPD										
	bool bc_slot10_reached_sensor;						// 10仓电池落到位										
	bool bc_slot10_smoke_sensor;						// 10仓烟雾报警										
	bool bc_slot10_liq_flow_switch_st;					// 10仓水冷流量开关											
	bool bc_slot6_10_pressure_switch_st;					// 6~10仓水冷压力开关											
	bool stacker_low_sensor_1;							// 堆垛机仓位对接1层									
	bool stacker_low_sensor_2;							// 堆垛机仓位对接2层									
	bool stacker_low_sensor_3;							// 堆垛机仓位对接3层									
	bool stacker_low_sensor_4;							// 堆垛机仓位对接4层									
	bool stacker_low_sensor_5;							// 堆垛机仓位对接5层									
	bool stacker_low_sensor_6;							// 堆垛机仓位对接6层									
	bool stacker_low_sensor_0;							// 堆垛机接驳位对接位									
	bool stacker_move_f_sensor;							// 堆垛机行走前仓位									
	bool stacker_move_r_sensor;							// 堆垛机行走后仓位									
	bool stacker_move_RGV_sensor;						// 堆垛机行走RGV对接位										
	bool stacker_left_safe_sensor_1;					// 货叉上层左超程											
	bool stacker_right_safe_sensor_1;					// 货叉上层右超程											
	bool stacker_left_safe_sensor_2;					// 货叉下层左超程											
	bool stacker_right_safe_sensor_2;					// 货叉下层右超程											
	bool fork_retract_sensor_1;							// 货叉主叉臂中点									
	bool fork_retract_sensor_2;							// 货叉辅叉臂中点									
	bool fork_left_extend_sensor_1;						// 货叉叉臂左到位1										
	bool fork_left_extend_sensor_2;						// 货叉叉臂左到位2										
	bool fork_right_extend_sensor_1;					// 货叉叉臂右到位											
	bool fork_bc_exist_sensor_1;						// 货叉有电池1										
	bool fork_bc_exist_sensor_2;						// 货叉有电池2										
	bool vehaicl_l_work_sensor;							// 左车辆举升工作位									
	bool vehaicl_l_maintain_sensor;						// 左车辆举升维护位										
	bool vehaicl_l_safe_sensor;							// 左车辆举升安全									
	bool vehaicl_l_bc_safe_sensor;						// 左车辆举升电池安全										
	bool vehaicl_r_work_sensor;							// 右车辆举升工作位									
	bool vehaicl_r_maintain_sensor;						// 右车辆举升维护位										
	bool vehaicl_r_safe_sensor;							// 右车辆举升安全									
	bool vehaicl_r_bc_safe_sensor;						// 右车辆举升电池安全										
	bool bc_slot11_ec_retract_sensor_1;					// 11仓NPA电插头上到位											
	bool bc_slot11_ec_extend_sensor_1;					// 11仓NPA电插头下到位											
	bool bc_slot11_lc_retract_sensor_1;					// 11仓NPD水插头上到位											
	bool bc_slot11_lc_extend_sensor_1;					// 11仓NPD水插头下到位											
	bool bc_slot11_ec_retract_sensor_2;					// 11仓NPA电插头上到位											
	bool bc_slot11_ec_extend_sensor_2;					// 11仓NPA电插头下到位											
	bool bc_slot11_lc_retract_sensor_2;					// 11仓NPD水插头上到位											
	bool bc_slot11_lc_extend_sensor_2;					// 11仓NPD水插头下到位											
	bool bc_slot11_check_sensor_1;						// 11仓电池区分NPA										
	bool bc_slot11_check_sensor_2;						// 11仓电池区分NPD										
	bool bc_slot11_reached_sensor;						// 11仓电池落到位										
	bool bc_slot11_smoke_sensor;						// 11仓烟雾报警										
	bool bc_slot11_liq_flow_switch_st;					// 11仓水冷流量开关											
	bool bc_slot12_ec_retract_sensor_1;					// 12仓NPA电插头上到位											
	bool bc_slot12_ec_extend_sensor_1;					// 12仓NPA电插头下到位											
	bool bc_slot12_lc_retract_sensor_1;					// 12仓NPA水插头上到位											
	bool bc_slot12_lc_extend_sensor_1;					// 12仓NPA水插头下到位											
	bool bc_slot12_ec_retract_sensor_2;					// 12仓NPD电插头上到位											
	bool bc_slot12_ec_extend_sensor_2;					// 12仓NPD电插头下到位											
	bool bc_slot12_lc_retract_sensor_2;					// 12仓NPD水插头上到位											
	bool bc_slot12_lc_extend_sensor_2;					// 12仓NPD水插头下到位											
	bool bc_slot12_check_sensor_1;						// 12仓电池区分NPA										
	bool bc_slot12_check_sensor_2;						// 12仓电池区分NPD										
	bool bc_slot12_reached_sensor;						// 12仓电池落到位										
	bool bc_slot12_smoke_sensor;						// 12仓烟雾报警										
	bool bc_slot12_liq_flow_switch_st;					// 12仓水冷流量开关											
	bool bc_slot13_ec_retract_sensor_1;					// 13仓NPA电插头上到位											
	bool bc_slot13_ec_extend_sensor_1;					// 13仓NPA电插头下到位											
	bool bc_slot13_lc_retract_sensor_1;					// 13仓NPA水插头上到位											
	bool bc_slot13_lc_extend_sensor_1;					// 13仓NPA水插头下到位											
	bool bc_slot13_ec_retract_sensor_2;					// 13仓NPD电插头上到位											
	bool bc_slot13_ec_extend_sensor_2;					// 13仓NPD电插头下到位											
	bool bc_slot13_lc_retract_sensor_2;					// 13仓NPD水插头上到位											
	bool bc_slot13_lc_extend_sensor_2;					// 13仓NPD水插头下到位											
	bool bc_slot13_check_sensor_1;						// 13仓电池区分NPA										
	bool bc_slot13_check_sensor_2;						// 13仓电池区分NPD										
	bool bc_slot13_reached_sensor;						// 13仓电池落到位										
	bool bc_slot13_smoke_sensor;						// 13仓烟雾报警										
	bool bc_slot13_liq_flow_switch_st;					// 13仓水冷流量开关											
	bool bc_slot14_ec_retract_sensor_1;					// 14仓NPA电插头上到位											
	bool bc_slot14_ec_extend_sensor_1;					// 14仓NPA电插头下到位											
	bool bc_slot14_lc_retract_sensor_1;					// 14仓NPA水插头上到位											
	bool bc_slot14_lc_extend_sensor_1;					// 14仓NPA水插头下到位											
	bool bc_slot14_ec_retract_sensor_2;					// 14仓NPD电插头上到位											
	bool bc_slot14_ec_extend_sensor_2;					// 14仓NPD电插头下到位											
	bool bc_slot14_lc_retract_sensor_2;					// 14仓NPD水插头上到位											
	bool bc_slot14_lc_extend_sensor_2;					// 14仓NPD水插头下到位											
	bool bc_slot14_check_sensor_1;						// 14仓电池区分NPA										
	bool bc_slot14_check_sensor_2;						// 14仓电池区分NPD										
	bool bc_slot14_reached_sensor;						// 14仓电池落到位										
	bool bc_slot14_smoke_sensor;						// 14仓烟雾报警										
	bool bc_slot14_liq_flow_switch_st;					// 14仓水冷流量开关											
	bool bc_slot15_ec_retract_sensor_1;					// 15仓NPA电插头上到位											
	bool bc_slot15_ec_extend_sensor_1;					// 15仓NPA电插头下到位											
	bool bc_slot15_lc_retract_sensor_1;					// 15仓NPA水插头上到位											
	bool bc_slot15_lc_extend_sensor_1;					// 15仓NPA水插头下到位											
	bool bc_slot15_ec_retract_sensor_2;					// 15仓NPD电插头上到位											
	bool bc_slot15_ec_extend_sensor_2;					// 15仓NPD电插头下到位											
	bool bc_slot15_lc_retract_sensor_2;					// 15仓NPD水插头上到位											
	bool bc_slot15_lc_extend_sensor_2;					// 15仓NPD水插头下到位											
	bool bc_slot15_check_sensor_1;						// 15仓电池区分NPA										
	bool bc_slot15_check_sensor_2;						// 15仓电池区分NPD										
	bool bc_slot15_reached_sensor;						// 15仓电池落到位										
	bool bc_slot15_smoke_sensor;						// 15仓烟雾报警										
	bool bc_slot15_liq_flow_switch_st;					// 15仓水冷流量开关											
	bool bc_slot16_ec_retract_sensor_1;					// 16仓NPA电插头上到位											
	bool bc_slot16_ec_extend_sensor_1;					// 16仓NPA电插头下到位											
	bool bc_slot16_lc_retract_sensor_1;					// 16仓NPA水插头上到位											
	bool bc_slot16_lc_extend_sensor_1;					// 16仓NPA水插头下到位											
	bool bc_slot16_ec_retract_sensor_2;					// 16仓NPD电插头上到位											
	bool bc_slot16_ec_extend_sensor_2;					// 16仓NPD电插头下到位											
	bool bc_slot16_lc_retract_sensor_2;					// 16仓NPD水插头上到位											
	bool bc_slot16_lc_extend_sensor_2;					// 16仓NPD水插头下到位											
	bool bc_slot16_check_sensor_1;						// 16仓电池区分NPA										
	bool bc_slot16_check_sensor_2;						// 16仓电池区分NPD										
	bool bc_slot16_reached_sensor;						// 16仓电池落到位										
	bool bc_slot16_smoke_sensor;						// 16仓烟雾报警										
	bool bc_slot16_liq_flow_switch_st;					// 16仓水冷流量开关											
	bool bc_slot17_ec_retract_sensor_1;					// 17仓NPA电插头上到位											
	bool bc_slot17_ec_extend_sensor_1;					// 17仓NPA电插头下到位											
	bool bc_slot17_lc_retract_sensor_1;					// 17仓NPA水插头上到位											
	bool bc_slot17_lc_extend_sensor_1;					// 17仓NPA水插头下到位											
	bool bc_slot17_ec_retract_sensor_2;					// 17仓NPD电插头上到位											
	bool bc_slot17_ec_extend_sensor_2;					// 17仓NPD电插头下到位											
	bool bc_slot17_lc_retract_sensor_2;					// 17仓NPD水插头上到位											
	bool bc_slot17_lc_extend_sensor_2;					// 17仓NPD水插头下到位											
	bool bc_slot17_check_sensor_1;						// 17仓电池区分NPA										
	bool bc_slot17_check_sensor_2;						// 17仓电池区分NPD										
	bool bc_slot17_reached_sensor;						// 17仓电池落到位										
	bool bc_slot17_smoke_sensor;						// 17仓烟雾报警										
	bool bc_slot17_liq_flow_switch_st;					// 17仓水冷流量开关											
	bool bc_slot18_ec_retract_sensor_1;					// 18仓NPA电插头上到位											
	bool bc_slot18_ec_extend_sensor_1;					// 18仓NPA电插头下到位											
	bool bc_slot18_lc_retract_sensor_1;					// 18仓NPA水插头上到位											
	bool bc_slot18_lc_extend_sensor_1;					// 18仓NPA水插头下到位											
	bool bc_slot18_ec_retract_sensor_2;					// 18仓NPD电插头上到位											
	bool bc_slot18_ec_extend_sensor_2;					// 18仓NPD电插头下到位											
	bool bc_slot18_lc_retract_sensor_2;					// 18仓NPD水插头上到位											
	bool bc_slot18_lc_extend_sensor_2;					// 18仓NPD水插头下到位											
	bool bc_slot18_check_sensor_1;						// 18仓电池区分NPA										
	bool bc_slot18_check_sensor_2;						// 18仓电池区分NPD										
	bool bc_slot18_reached_sensor;						// 18仓电池落到位										
	bool bc_slot18_smoke_sensor;						// 18仓烟雾报警										
	bool bc_slot18_liq_flow_switch_st;					// 18仓水冷流量开关											
	bool bc_slot19_ec_retract_sensor_1;					// 19仓NPA电插头上到位											
	bool bc_slot19_ec_extend_sensor_1;					// 19仓NPA电插头下到位											
	bool bc_slot19_lc_retract_sensor_1;					// 19仓NPA水插头上到位											
	bool bc_slot19_lc_extend_sensor_1;					// 19仓NPA水插头下到位											
	bool bc_slot19_ec_retract_sensor_2;					// 19仓NPD电插头上到位											
	bool bc_slot19_ec_extend_sensor_2;					// 19仓NPD电插头下到位											
	bool bc_slot19_lc_retract_sensor_2;					// 19仓NPD水插头上到位											
	bool bc_slot19_lc_extend_sensor_2;					// 19仓NPD水插头下到位											
	bool bc_slot19_check_sensor_1;						// 19仓电池区分NPA										
	bool bc_slot19_check_sensor_2;						// 19仓电池区分NPD										
	bool bc_slot19_reached_sensor;						// 19仓电池落到位										
	bool bc_slot19_smoke_sensor;						// 19仓烟雾报警										
	bool bc_slot19_liq_flow_switch_st;					// 19仓水冷流量开关											
	bool bc_slot20_ec_retract_sensor_1;					// 20仓NPA电插头上到位											
	bool bc_slot20_ec_extend_sensor_1;					// 20仓NPA电插头下到位											
	bool bc_slot20_lc_retract_sensor_1;					// 20仓NPA水插头上到位											
	bool bc_slot20_lc_extend_sensor_1;					// 20仓NPA水插头下到位											
	bool bc_slot20_ec_retract_sensor_2;					// 20仓NPD电插头上到位											
	bool bc_slot20_ec_extend_sensor_2;					// 20仓NPD电插头下到位											
	bool bc_slot20_lc_retract_sensor_2;					// 20仓NPD水插头上到位											
	bool bc_slot20_lc_extend_sensor_2;					// 20仓NPD水插头下到位											
	bool bc_slot20_check_sensor_1;						// 20仓电池区分NPA										
	bool bc_slot20_check_sensor_2;						// 20仓电池区分NPD										
	bool bc_slot20_reached_sensor;						// 20仓电池落到位										
	bool bc_slot20_smoke_sensor;						// 20仓烟雾报警										
	bool bc_slot20_liq_flow_switch_st;					// 20仓水冷流量开关											
	bool bc_slot21_ec_retract_sensor_1;					// 21仓NPA电插头上到位											
	bool bc_slot21_ec_extend_sensor_1;					// 21仓NPA电插头下到位											
	bool bc_slot21_ec_retract_sensor_2;					// 21仓NPD电插头上到位											
	bool bc_slot21_ec_extend_sensor_2;					// 21仓NPD电插头下到位											
	bool bc_slot21_check_sensor_1;						// 21仓电池区分NPA										
	bool bc_slot21_check_sensor_2;						// 21仓电池区分NPD										
	bool bc_slot21_reached_sensor;						// 21仓电池落到位										
	bool bc_slot21_smoke_sensor;						// 21仓烟雾报警										
	bool bc_slot11_15_pressure_switch_st;				// 11~15仓 水冷压力开关												
	bool bc_slot16_20_pressure_switch_st;				// 16~20仓 水冷压力开关												
	bool bc_fire_push_retract_sensor_1;					// 消防接驳前推杆缩回到位											
	bool bc_fire_push_extend_sensor_1;					// 消防接驳前推杆伸出到位											
	bool bc_fire_push_retract_sensor_2;					// 消防接驳后推杆缩回到位											
	bool bc_fire_push_extend_sensor_2;					// 消防接驳后推杆伸出到位											
	bool fire_liq_check;								// 消防液位检测								
	bool fork_X_left_limit_sensor;						// 堆垛机货叉左限位										
	bool fork_X_right_limit_sensor;						// 堆垛机货叉右限位										
	bool fork_X_home_sensor;							// 堆垛机货叉原点									
	bool stacker_move_f_limit_sensor;					// 堆垛机行走前限位											
	bool stacker_move_r_limit_sensor;					// 堆垛机行走后限位											
	bool stacker_move_home_sensor;						// 堆垛机行走原点										
	bool stacker_lift_up_limit_sensor;					// 堆垛机升降上限位											
	bool stacker_lift_down_limit_sensor;				// 堆垛机升降下限位												
	bool stacker_lift_home_sensor;						// 堆垛机升降原点										
	bool pl_move_f_limit_sensor;						// 加解锁平台平移前限位										
	bool pl_move_r_limit_sensor;						// 加解锁平台平移后限位										
	bool pl_move_home_sensor;							// 加解锁平台平移原点									
	bool lr_lift_up_limit_sensor;						// 加解锁平台升降上限位										
	bool lr_lift_down_limit_sensor;						// 加解锁平台升降下限位										
	bool lr_lift_home_sensor;							// 加解锁平台升降原点									
	bool vehical_f_up_limit_sensor;						// 左车辆举升上限位										
	bool vehical_f_down_limit_sensor;					// 左车辆举升下限位											
	bool vehical_f_home_sensor;							// 左车辆举升原点									
	bool vehical_r_up_limit_sensor;						// 右车辆举升上限位										
	bool vehical_r_down_limit_sensor;					// 右车辆举升下限位											
	bool vehical_r_home_sensor;							// 右车辆举升原点									
	bool bc_lift_up_limit_sensor;						// 升降仓上限位										
	bool bc_lift_down_limit_sensor;						// 升降仓下限位										
	bool bc_lift_home_sensor;							// 升降仓原点	
	bool bc_lift_safe_sensor;                  			// 接驳位举升电池安全
  	bool left_buffer_safe_sensor;              			// 左缓存电池安全
  	bool right_buffer_safe_sensor;             			// 右缓存电池安全 
	bool bc_slot22_reached_sensor;        				// 消防仓电池落到位
	bool bc_lift_exist_sensor;							// 接驳位上有电池检测
	bool rgv_bc_reach_sensor_07;						// 电池平整7
	bool rgv_bc_reach_sensor_08;						// 电池平整8
	bool liq_lift_zero_sensor;							// 液压举升原点位
  	bool reserved[73];                         			// 预留									
	
}PLC_SENSOR_STRUCT;

/**
 *@brief DI数据结构定义 100个
 */
typedef struct
{  
	bool emergency_stop_switch_01;						// 急停					
	bool liq_level_warning;								// 液位报警			
	bool I_power_st_1;									// 扩展箱控制供电脱扣报警		
	bool I_power_st_2;									// 扩展箱动力供电脱扣报警		
	bool I_power_st_3;									// 堆垛机货叉伺服供电脱扣报警		
	bool I_power_st_4;									// 堆垛机行走伺服供电脱扣报警		
	bool I_power_st_5;									// 堆垛机升降伺服供电脱扣报警		
	bool I_power_st_6;									// 刹车开关电源后端配电脱扣报警		
	bool I_power_st_7;									// 前轮推杆伺服供电脱扣报警		
	bool I_power_st_8;									// 后轮推杆伺服供电脱扣报警		
	bool I_power_st_9;									// V槽&导向条伺服供电脱扣报警		
	bool I_power_st_10;									// 车身定位销伺服供电脱扣报警		
	bool I_power_st_11;									// 拧紧枪1 伺服供电脱扣报警		
	bool I_power_st_12;									// 拧紧枪2 伺服供电脱扣报警		
	bool I_power_st_13;									// 拧紧枪3&4 伺服供电脱扣报警		
	bool I_power_st_14;									// 拧紧枪5&6 伺服供电脱扣报警		
	bool I_power_st_15;									// 拧紧枪7&8 伺服供电脱扣报警		
	bool I_power_st_16;									// 拧紧枪9 伺服供电脱扣报警		
	bool I_power_st_17;									// 拧紧枪10 伺服供电脱扣报警		
	bool I_power_st_18;									// 拧紧枪11 伺服供电脱扣报警		
	bool I_power_st_19;									// 拧紧枪12 伺服供电脱扣报警		
	bool I_power_st_20;									// 开阖门伺服供电脱扣报警		
	bool I_power_st_21;									// RGV伺服供电脱扣报警		
	bool I_power_st_22;									// 车辆举升伺服供电脱扣报警		
	bool I_power_st_23;									// 接驳位举升伺服供电脱扣报警		
	bool I_power_st_24;									// 变频器供电脱扣报警		
	bool A01_A1_check;									// A01A1检测		
	bool A01_A2_check;									// A01A2检测		
	bool A01_A3_check;									// A01A3检测		
	bool A01_A4_check;									// A01A4检测		
	bool A01_A5_check;									// A01A5检测		
	bool A01_A6_check;									// A01A6检测		
	bool A01_A7_check;									// A01A7检测		
	bool A01_A8_check;									// A01A8检测		
	bool A01_A9_check;									// A01A9检测		
	bool A01_A10_check;									// A01A10检测		
	bool A02_A1_module_status;							// A02A1模块状态				
	bool A02_A2_module_status;							// A02A2模块状态				
	bool A02_A3_module_status;							// A02A3模块状态				
	bool A02_A4_module_status;							// A02A4模块状态				
	bool A02_A5_module_status;							// A02A5模块状态				
	bool A02_A6_module_check;							// A02A6模块状态															
	bool reserved[58];									// 预留
}PLC_DI_STRUCT;

/**
 *@brief alarm数据结构定义 2000个
 */
typedef struct
{
	bool error_code[PLC_ALARM_NUM_MAX];
}PLC_ALARM_STRUCT;

/**
 *@brief motion的数据结构定义 250个
 */
 typedef struct
 {
	int16_t id;
	int16_t interlock_number;
	bool interlock_condition[20];
	bool start;
	bool finished;	 
	bool interlock;
	bool error;	 
	bool is_running;	 
 }PLC_MOTION_PARAMETER_STRUCT;

/**
 *@brief JOB_STATE数据结构定义
 */
typedef struct
{
	int16_t bc_job_id;
	int16_t bc_job_step;
	bool    bc_job_finish;	
	int16_t pl_job_id;
	int16_t pl_job_step;
	bool    pl_job_finish;
}PLC_JOB_STATUS_STRUCT;

/**
 *@brief system cmd status 结构定义
 */
typedef struct
{
	bool setting;
	bool stop;
	bool pause;	
	bool continue_st;
	bool reset;
	bool change_mode;
	bool initialize;
	bool homing;
}PLC_SYS_CMD_STATUS_STRUCT;

/**
 *@brief PLC软件版本号 
 */
typedef struct 
{
	char version[11];
}PLC_VERSION_STRUCT;

/**
 *@brief 变频器数据类型
 */
typedef struct
{
	int16_t error_code;	//故障码
	int16_t power;		//功率
	int16_t current;	//电流
	int16_t frequency;	//频率	
}PLC_CONVERTER_TYPE_STRUCT;

/**
 *@brief 变频器数据包
 */
typedef struct
{
	PLC_CONVERTER_TYPE_STRUCT converter_tranship;			// 接驳位变频器
	PLC_CONVERTER_TYPE_STRUCT converter_pl_r_buffer;		// 停车平台右缓存位变频器
	PLC_CONVERTER_TYPE_STRUCT converter_pl_roller;			// 停车平台滚筒变频器
	PLC_CONVERTER_TYPE_STRUCT converter_pl_l_buffer;		// 停车平台左缓存位变频器
}PLC_CONVERTER_STRUCT;

/**
 *@brief 选定电池当前仓位号 反馈
 */
typedef struct 
{
	int8_t pos;
}PLC_FB_BAT_POS_STRUCT;

/**
 *@brief 视觉拍照步骤反馈
 */
typedef struct
{
	bool step1;  											// 车辆定位_01_定位状态
	bool step2;  											// 亏电池下表面视觉状态
	bool step3;  											// 服务电池上表面视觉状态
	bool step4;  											// 车辆定位_02_定位状态
	bool step5;  											// 服务电池下表面视觉状态
	bool step6;  											// 亏电电池上表面视觉状态
}PLC_FB_PHOTOGRAPH_STRUCT;


/**
 *@brief 消防完成标志位反馈 
 */
typedef struct 
{
	bool door_status;										// 开合门关闭反馈 
	bool status;											// 消防完成标志(落水箱)
	bool bat_arrived;										// 电池是否到达消防仓		
	bool trans_finish;  									// 消防电池转运完成（无人值守）		用不到2023/08/23
	bool button_status;										// 一键落水机械按键状态
	bool pl_action_finish;  								// 停车平台动作完成（有人值守）		用不到2023/08/23
}PLC_FB_FIRE_FINISH_STRUCT;

/**
 *@brief 零点标定标志位反馈 
 */
typedef struct 
{
	int8_t status;
}PLC_FB_HOME_FINISH_STRUCT;

/**
 *@brief 一键加/解锁失败数据包 
 */
typedef struct
{
	bool status[13];										// [0]加解锁判断标志位,1：加锁，0：解锁;[1~12]代表1～12轴加解锁
}PLC_FB_ONE_LOCK_UNLOCK_STRUCT;

/**
 *@brief 堆垛机当前仓位号 
 */
typedef struct 
{
	uint8_t pos;
}PLC_FB_STACKER_POS_STRUCT;

/**
 *@brief PLC整站类型匹配反馈 
 */
typedef struct 
{
	int8_t type;
}PLC_FB_STATION_TYPE_STRUCT;

/**
 *@brief PLC轮毂自适应结果反馈 
 */
typedef struct 
{
	int8_t result;
}PLC_FB_WHEEL_ADAPT_STRUCT;

/**
 *@brief PLC车辆类型结果反馈 
 */
typedef struct 
{
	int8_t type;
}PLC_FB_VEHICLE_TYPE_STRUCT;

/**
 *@brief PLC仓内电池类型结果反馈 
 */
typedef struct 
{
	int8_t type[21];
}PLC_FB_BAT_TYPE_STRUCT;

/**
 *@brief PLC停车平台可继续动作结果反馈 
 */
typedef struct 
{
	int8_t result;
}PLC_FB_PL_SWAP_CONTINUE_STRUCT;

/**
 *@brief PLC倒仓结果反馈 
 */
typedef struct 
{
	int8_t step;											// 倒仓步骤号
	bool ongoing;											// 是否在倒仓中
	bool finished;											// 是否倒仓完成
}PLC_FB_CHANGE_BAT_STRUCT;

/**
 *@brief PLC车身定位销压力结果反馈 
 */
typedef struct 
{
	int32_t lf_value;										// 左前车身定位销压力值
	int32_t lr_value;										// 左后车身定位销压力值
	int32_t rr_value;										// 右后车身定位销压力值
}PLC_FB_PRESSURE_STRUCT;

/**
 *@brief PLC加解锁方向结果反馈 
 */
typedef struct 
{
	int8_t direction;	//0-default；1-加锁；2-解锁
}PLC_FB_LOCK_DIRECTION_STRUCT;

/**
 *@brief PLC允许车辆自检结果反馈 
 */
typedef struct 
{
	int8_t allow;		//1-允许车辆自检；其他值-不允许
}PLC_FB_VEHICLE_DIAGNOSE_STRUCT;

/**
 *@brief PLC接驳机结构类型结果反馈 
 */
typedef struct 
{
	int8_t type;		//0-初始值；1-刚性链；2-丝杠
}PLC_FB_BC_LIFT_TYPE_STRUCT;

/**
 *@brief PLC卷帘门执行结果反馈 
 */
typedef struct 
{
	int8_t front_up;												// 前卷帘门上升反馈
	int8_t front_stop;												// 前卷帘门停止反馈
	int8_t front_down;												// 前卷帘门下降反馈
	int8_t back_up;													// 后卷帘门上升反馈
	int8_t back_stop;												// 后卷帘门停止反馈
	int8_t back_down;												// 后卷帘门下降反馈
}PLC_FB_ROLLING_DOOR_STRUCT;

/**
 *@brief PLC不挂车及回退状态反馈 
 */
typedef struct 
{
	int8_t trailer_state;											// 不挂车配置反馈
	int8_t swap_rollback;											// 换电失败回退状态
}PLC_FB_SWAP_ROLLBACK_STRUCT;

/**
 *@brief PLC安全光幕使能状态反馈 
 */
typedef struct 
{
	int8_t state;													// 安全光幕使能状态反馈 0:关闭，1:使能
}PLC_FB_SAFE_LIGHT_STRUCT;

/**
 *@brief PLC消防模式状态反馈 
 */
typedef struct 
{
	int8_t mode;													// PLC消防模式状态反馈 0:非消防中，1:消防中
}PLC_FB_FIRE_MODE_STRUCT;

/**
 *@brief PLC整站模式维护/运营反馈 
 */
typedef struct 
{
	int8_t mode;													// PLC整站模式维护/运营反馈 1:运营模式，2:维护模式
}PLC_FB_STATION_MODE_STRUCT;

/**
 *@brief PLC伺服温度反馈 
 */
typedef struct 
{
	int16_t temp[38];												// PLC伺服温度反馈 
}PLC_FB_SERVO_TEMP_STRUCT;

/**
 *@brief PLC消防状态步骤反馈 
 */
typedef struct 
{
	int8_t transfer_type;											// 消防转运类型，1:系统自动转运，2:云端远程转运
	int8_t drop_type;												// 消防落水类型，1:远程落水，2:机械按键落水
	int8_t step;													// 消防转运步骤
	int8_t slot;													// 消防仓位号
}PLC_FB_FIRE_STATUS_STRUCT;

/**
 *@brief PLC落水按键改造反馈
 */
typedef struct 
{
	int8_t result;													// 落水按键改造反馈，0:未改造，1:已改造
}PLC_FB_DROP_KEY_RESULT_STRUCT;

/**
 *@brief PLC水电插头运动状态反馈
 */
typedef struct 
{
	bool npa_liq_state[21];											// NPA水插头运动状态反馈，0:未运动，1:运动中
	bool npa_pwr_state[21];											// NPA电插头运动状态反馈，0:未运动，1:运动中
	bool npd_liq_state[21];											// NPD水插头运动状态反馈，0:未运动，1:运动中
	bool npd_pwr_state[21];											// NPD电插头运动状态反馈，0:未运动，1:运动中
}PLC_FB_PLUG_MOVING_STRUCT;

/**
 *@brief PLC命令状态反馈 
 */
typedef struct 
{
	PLC_FB_BAT_POS_STRUCT 			fb_bat_pos;						// PLC电池当前仓位号反馈
	PLC_FB_PHOTOGRAPH_STRUCT		fb_photograph;					// PLC视觉拍照步骤反馈
	PLC_FB_FIRE_FINISH_STRUCT		fb_fire;						// PLC消防完成标志位反馈
	PLC_FB_HOME_FINISH_STRUCT		fb_home;						// PLC零点标定标志位反馈
	PLC_FB_ONE_LOCK_UNLOCK_STRUCT 	fb_lock_unlock;					// PLC一键加/解锁失败反馈
	PLC_FB_STACKER_POS_STRUCT		fb_stacker_pos;					// PLC堆垛机当前仓位号反馈
	PLC_FB_STATION_TYPE_STRUCT		fb_station;						// PLC整站类型反馈
	PLC_FB_WHEEL_ADAPT_STRUCT 		fb_adapt;						// PLC轮毂自适应结果反馈
	PLC_FB_VEHICLE_TYPE_STRUCT		fb_vehicle;						// PLC车辆类型结果反馈
	PLC_FB_BAT_TYPE_STRUCT			fb_bat_type;					// PLC仓内电池类型反馈
	PLC_FB_PL_SWAP_CONTINUE_STRUCT	fb_pl_swap_continue;			// PLC停车平台可继续动作结果反馈
	PLC_FB_CHANGE_BAT_STRUCT		fb_change_bat;					// PLC倒仓结果反馈
	PLC_FB_PRESSURE_STRUCT			fb_pin_pressure;				// PLC车身定位销压力结果反馈
	PLC_FB_LOCK_DIRECTION_STRUCT	fb_lock_direction;				// PLC加解锁方向结果反馈
	PLC_FB_VEHICLE_DIAGNOSE_STRUCT 	fb_vehicle_diagnose;			// PLC允许车辆自检结果反馈
	PLC_FB_BC_LIFT_TYPE_STRUCT		fb_bc_lift_type;				// PLC接驳机结构类型结果反馈
	PLC_FB_ROLLING_DOOR_STRUCT		fb_rolling_door;				// PLC卷帘门执行结果反馈
	PLC_FB_SWAP_ROLLBACK_STRUCT		fb_swap_rollback;				// PLC不挂车及回退状态反馈
	PLC_FB_SAFE_LIGHT_STRUCT		fb_safe_light;					// PLC安全光幕使能状态反馈
	PLC_FB_FIRE_MODE_STRUCT			fb_fire_mode;					// PLC消防模式状态反馈
	PLC_FB_STATION_MODE_STRUCT		fb_station_mode;				// PLC整站模式维护/运营反馈
	PLC_FB_SERVO_TEMP_STRUCT		fb_servo_temp;					// PLC伺服温度反馈
	PLC_FB_FIRE_STATUS_STRUCT		fb_fire_status;					// PLC消防状态步骤反馈
	PLC_FB_DROP_KEY_RESULT_STRUCT	fb_drop_key;					// PLC落水按键改造反馈
	PLC_FB_PLUG_MOVING_STRUCT		fb_plug_moving_state;			// PLC水电插头运动状态反馈
	int8_t reserved[25];											// 预留
}PLC_CMD_FEEDBACK_STRUCT;



/*****************************************************************************************************************************
 *@brief 主控接收PLC数据结构定义;
 */
typedef struct
{   
	PLC_MSG_SIZE_STRUCT				plc_msg_size;					// PLC字节长度
	PLC_MODE_STRUCT               	mode;							// PLC模式
	PLC_LR_STRUCT         		    lr;								// 拆卸机器人数据
	PLC_BC_STRUCT         		    bc;								// 电池仓数据
	PLC_VP_STRUCT        		    vp;								// 停车平台数据
	PLC_SENSOR_STRUCT    		    sensor;							// 传感器数据
	PLC_DI_STRUCT         		    di;								// DI数据
	PLC_ALARM_STRUCT      		    alarm;							// 告警数据
	PLC_MOTION_PARAMETER_STRUCT 	motion[PLC_MOTION_NUM_MAX]; 	// 运动控制数据
	PLC_JOB_STATUS_STRUCT 		    job_status;						// 一键换电步骤状态数据
	PLC_SETTING_STRUCT 		  		settings;						// 参数设置数据
	PLC_SYS_CMD_STATUS_STRUCT    	sys_cmd_st;						// 系统命令状态
	PLC_VERSION_STRUCT              plc_version;					// 版本号
	PLC_CONVERTER_STRUCT			plc_converter;					// 变频器数据
	PLC_CMD_FEEDBACK_STRUCT			plc_cmd_fd;						// PLC命令状态反馈

}PLC_STATUS_REP_STRUCT;

/*****************************************************************************************************************************
 * @brief 主控下发消息结构体
 */
typedef struct
{
	PLC_REQ_HEADER_STRUCT request_header;	
	union
	{			
		PLC_HB_REQ_STRUCT 			hb_req_msg;						// 心跳
		PLC_SETTING_STRUCT			settings_req_msg;				// 参数设置
		PLC_STOP_REQ_STRUCT 		stop_req_msg;					// 预留
		PLC_PAUSE_REQ_STRUCT 		pause_req_msg;					// 预留
		PLC_CONTINUE_REQ_STRUCT 	continue_req_msg;				// 预留
		PLC_RESET_REQ_STRUCT 		reset_req_msg;					// 预留
		PLC_CHANGE_MODE_REQ_STRUCT 	change_mode_req_msg;			// 模式切换
		PLC_HOME_REQ_STRUCT 		home_req_msg;					// 零点标定
		PLC_JOG_REQ_STRUCT 			jog_req_msg;					// 点动控制
		PLC_MANUAL_REQ_STRUCT 		manual_req_msg;					// 单步控制
		PLC_JOB_REQ_STRUCT 			job_req_msg;					// JOB控制
		PLC_CMD_DO_CTRL_STRUCT 		do_ctrl_msg;					// DO控制
		PLC_PHOTOGRAPH_REQ_STRUCT	photograph_req_msg;				// 视觉拍照请求数据
		PLC_FIRE_REQ_STRUCT			fire_rep_msg;					// 消防请求数据
	}request_body;
}PLC_REQUSET_STRUCT;

/**
 * @brief 回答消息结构体
 */
typedef struct
{		
	PLC_STATUS_REP_STRUCT status_rep_msg;		
}PLC_REPLY_STRUCT;

#endif // PLC_TYPE_H
