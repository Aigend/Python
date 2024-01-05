## Use package

`pip3 install nio-messages -i http://nexus.nioint.com/repository/pypi-all/simple/ --trusted-host nexus.nioint.com`   

or

`pipenv install nio-messages`



## Update package

1. Add or update proto files
2. compile proto files to pb2.py  
    `cd nio_messages &&./protoc.sh`
3. update setup.py package version like version='0.0.3'
4. make package and upload package
    `python setup.py sdist bdist`

    `pip install twine`   
    
    vi ~/.pypirc
     ```buildoutcfg
    [distutils]
    index-servers =
        my_nexus

    
    [my_nexus]
    repository: http://nexus.nioint.com/repository/pypi-host
    username: nexus.swc
    password: CPU7[burbled
        
    ```
    
    `twine upload  -r nexus dist/*`
    
    确保dist目录下没有以前的文件，不然上传为报400


