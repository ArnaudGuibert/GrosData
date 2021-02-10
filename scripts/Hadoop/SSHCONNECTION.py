#-------------------------------------------------------------------------------
# Name:        ConnectTOHadoop
# Purpose:
#
# Author:      remi huguenot
#
# Created:     22/01/2021
# Copyright:   (c) remi huguenot 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import paramiko
import time
import os
from scp import SCPClient

def connect(host,portNum , user, pswd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   
    client.connect(host, portNum,user,pswd)
    
    return client


def getFileFromHadoop(client,filename,username,host,port):
    client.exec_command("hadoop fs -get /user/data/"+filename+ " "+ filename)
    scp = SCPClient(client.get_transport())
    
    scp.get( "/home/"+username+"/"+filename)
    
    client.exec_command("rm /home/"+username+"/"+filename)
    
    
    
def closeClient(client):
    client.close()


def ConnectAndRetrieveFile(host,port,user,password,filename):
    cli = connect(host,port,user,password)
    getFileFromHadoop(cli,filename,user,host,port)
    closeClient(cli)
    


"""
ConnectAndRetrieveFile("localhost",2222,"maria_dev","maria_dev","data.json")
print("THE END")
"""
