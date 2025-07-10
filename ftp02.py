import ftplib

def upload_file(ftp, filename):
    with open(filename, 'rb') as f:
        ftp.storbinary('STOR ' + filename,f)
# f'STOR {filename}', f)

hostname = "192.168.241.128"
ftp = ftplib.FTP(hostname)
ftp.login('msfadmin','msfadmin')
upload_file(ftp, 'malware.xlsx')
ftp.quit()
