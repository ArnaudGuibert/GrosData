# Script AWS

## Installation :
- sudo yum install python3 -y
- sudo python3 -m pip install boto3
- sudo python3 -m pip install numpy
- sudo python3 -m pip install pandas
- sudo python3 -m pip install joblib
- sudo python3 -m pip install sklearn

## Configuration :
You can configure :
- file names
- bucket names
- FIFO URL
To do that, modify variable on first lines of each python files :
- script.py
- receivePredict.py
- sendResults.py

## Start :
- python3 script.py