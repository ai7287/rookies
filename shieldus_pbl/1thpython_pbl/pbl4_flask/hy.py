import ftplib  
# FTP 서버 주소	192.168.241.128
# 아이디	msfadmin
# 비밀번호	msfadmin
hostname = "192.168.241.128"
ftp = ftplib.FTP(hostname)
ftp.login('msfadmin','msfadmin')
print(ftp.pwd())
ftp.retrlines('LIST')
print("===============")