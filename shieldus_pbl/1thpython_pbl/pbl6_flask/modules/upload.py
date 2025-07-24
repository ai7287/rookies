from ftplib import FTP

def connect_ftp(host, user, password):
    ftp = FTP(host)
    ftp.login(user=user, passwd=password)
    return ftp

def upload_to_ftp(ftp: FTP, filepath: str, remote_name: str):
    with open(filepath, 'rb') as f:
        ftp.storbinary(f'STOR ' + remote_name, f)
