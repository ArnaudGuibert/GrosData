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

import paraminko

def connect(hostname, username, password):
    client = paramiko.SSHClient()
    """ potentiellement besoin de chiffrer la clée
    key = paramiko.RSAKey(data=base64.b64decode(b'AAA...'))
    client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
    """

    client.connect(hostname, username, password)
    return client


def getFileFromHadoop(client, path):
    client.exec_command("fs -get "+path+" /HadoopDump/lastfile" )
    sftp_client = client.open_sftp()
    remote_file= sftp_client.open("/HadoopDump/lastfile")
    return_file = remote_file.read()

    remote_file.close()

    client.exec_command("rm /HadoopDump/lastfile")
    return return_file
def closeClient(client):
    client.close()




