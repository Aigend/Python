* 模拟仿真Matrix 
  1. 在主控环境下关闭matrix
      Matrix 添加到systemd服务后，可使用systemctl命令对其进行管理，服务名称为：container-matrix.service 。
        执行 systemctl status container-matrix.service 可查看systemd服务状态
        默认情况下，Matrix服务已添加到systemd的开机自启列表中，无需手动启动。
        Matrix服务手动启动命令为：sudo systemctl start container-matrix.service
        Matrix服务手动停止命令为：sudo systemctl stop container-matrix.service  
  2. 执行python3 matrix_utils.py脚本
  3. 脚本访问Django matrix服务接口，发送所需数据
  4. 备注：django服务通过访问matrix脚本暴露的web服务，更新脚本发送的数据，端口为8091