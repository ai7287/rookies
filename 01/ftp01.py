import ftplib

hostname = "192.168.241.128"
ftp = ftplib.FTP(hostname)
ftp.login('msfadmin','msfadmin')
print(ftp.pwd())
ftp.retrlines('LIST')
print("===========================")
ftp.rmd("new_folder")
ftp.retrlines('LIST')
print("===========================")
ftp.cwd("vulnerable")
ftp.retrlines('LIST')
ftp.quit()
