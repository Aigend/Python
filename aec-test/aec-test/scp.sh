sshpass -p 'NIOpower68!@#$' scp ./report/*.json nio@192.168.1.13:/home/nio/
sshpass -p 'NIOpower68!@#$' scp ./scripts/scp_log.py nio@192.168.1.13:/home/nio/
sshpass -p 'NIOpower68!@#$' ssh nio@192.168.1.13 "sudo python3 ./scp_log.py"
sshpass -p 'NIOpower68!@#$' scp nio@192.168.1.13:/home/nio/ec_ai_app* ./logs/
sshpass -p 'NIOpower68!@#$' scp nio@192.168.1.13:/home/nio/mcs_info_processor* ./logs/