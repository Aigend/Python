# EVM Test

## Install Dependency
```
1、安装pyenv
    https://github.com/pyenv/pyenv#basic-github-checkout  
2、安装python3.6
    pyenv install 3.6.4
3、安装pipenv
    pip install pipenv
4、安装虚拟环境
    cd ev_monitor_nioauto
    pyenv local 3.6.4
    pipenv --python 3.6.4
    pipenv install --ignore-pipfile --skip-lock
    
 ```   
       
## Run cases
```
cd ev_monitor_nioauto
1、跑case的基础方法
    pipenv run py.test tests/ --env=test
2、增加allure报告
    pipenv run py.test tests/ --env=test --alluredir=allure-results
    allure open tests/allure-report/{case_result_allure_dir}
3、上传allure报告
```