## 告警同步功能测试

### 需求

基于线下沟通，因DEI实际业务需求：需要在之前实现的获取车辆wti信息的需求的基础上，将vehicle_info数据库vehicle_list表中vin车辆的wti报警信息自2022年1月1日至3月10日的数据一次性写入到vehicle_wti_info 表单

### 测试步骤
1. 从rvs数据库history_wti_alarm表查找历史告警记录
2. 根据history_wti_alarm表中vid从vehicle_profile表中查找到对应vin
3. 将筛选的车辆写入wti_sync_database_test库中vehicle_list表
4. 统计history_wti_alarm表告警数量
4. 进入phonix-server pod中执行命令
5. 执行完成后，检查wti_sync_database_test库中vehicle_wti_info表同步过来的数据两边做对比


### 参考资料

phoenix 告警同步数据库

```
[wti_sync_database_test]
host = srd-qcsh-mysql01-test.nioint.com
user = phx_master_data_test_rw
password = l961XXZbdDq9r
db_name = phx_master_data_test
```


-----------test-----------

rvs告警记录
``` 
SELECT vehicle_id,alarm_id, count(alarm_id) wti_count
FROM `history_wti_alarm`
WHERE start_time >= '2020-10-30 14:09:35'
AND start_time <= '2022-03-24 14:09:33'
and  vehicle_id in ("866c718a4b934275ab22d974637041b3","6eb567aca87c43f0853074a4c99a6c87","2a11f73d5a77449db53a8f49e7f35ad8","3e95c0dd2c34450488efecfe389ac704","1f1cbbd53aeb45d9850e5803ad667446","9347f56bb63e4af190c1cfe744f8c45e")
group by vehicle_id
order by  wti_count desc
```

同步目标库告警统计
```
select vin, count(1) count_wti,min(start_time),max(start_time)
from vehicle_wti_info
group by vin
order by count_wti desc
```
服务端命令
```
./phoenix_server --cmdName=sync_wti_alarm_data --startTime="2020-10-30 22:09:35" --endTime="2022-03-24 22:09:33" 2>&1 &

```
------------stg-----------


```
select vin, count(1) count_wti,min(start_time),max(start_time)
from vehicle_wti_info
where vin in (
"DSTEST2UXJ5302305",
"SQETEST0054390639",
"SQETEST0356424898",
"SQETEST0952876751"
)
group by vin
order by count_wti desc
```

```
SELECT vehicle_id,alarm_id, count(alarm_id) wti_count
FROM `history_wti_alarm`
WHERE start_time >= '2020-10-30 14:09:35'
AND start_time <= '2022-04-01 14:09:33'
and  vehicle_id in ("15ea87e41ad241109e70ae06589e0878","4169900d472243a28c2ad7b61dc79884","56f2b667e1824c3cae39d571de90c638","4d18ed00e36c4d738bfb4e7f3386c5d5")
group by vehicle_id
order by  wti_count desc
```

```
./phoenix_server --cmdName=sync_wti_alarm_data --startTime="2020-10-30 22:09:35" --endTime="2022-04-01 22:09:33" 2>&1 &

```


