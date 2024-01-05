"""

Cases:
验证当出现status_connect表中车辆连接状态(cgw/adc/cdc)(cdc暂时不支持)和nmp数据库中不一致时,可以发送邮件通知
验证发送邮件告警邮件10分钟发送一次,包括当前出现不一致的全车辆在nmp系统中各客户端(cgw/adc/cdc)连接状态
验证通过内部接口可以修改rvs数据库车辆的客户端(cgw/adc/cdc)的连接状态(on/off)
验证通过内部接口可以查看对应车辆再nmp系统和rvs服务中个客户端(cgw/adc/cdc)的连接状态


"""