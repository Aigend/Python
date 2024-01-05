rm -rf allure-results
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_start_charge_15904.py
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_stop_charge_15905.py
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_complete_charge_15906.py
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_flexible_charge_15908.py
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_begin_charge_oss_14008.py
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_finish_charge_oss_14008.py
python3 -m pytest -v -s ./test_cases/test_power_charge/test_power_discharge_oss_14008.py




