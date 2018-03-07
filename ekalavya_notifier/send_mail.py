import json
import smtplib, time
from urllib.request import urlopen
from email.mime.text import MIMEText

class GmailHandler():
	"""
	enable 'foreign-access' for the gmail account to get this to work
	"""
	def __init__(self, gmail, password):
		self.gmail = gmail
		self.password = password

	def send_mail(self, receivers, subject, text):
		if not isinstance(receivers, list):
			receivers = [receivers]
		smtp = smtplib.SMTP("smtp.gmail.com", 587)
		smtp.ehlo(), smtp.starttls(), smtp.ehlo()
		smtp.login(self.gmail, self.password)

		for receiver in receivers:
			msg = MIMEText(text)
			msg['Subject'] = subject
			msg['From'] = self.gmail
			msg['To'] = receiver
			smtp.sendmail(self.gmail, receiver, str(msg))
			smtp.quit()


account_info, to_notify = {}, ["dummy@dummy.com"]
with open('account.json', 'r') as file:
	account_info = json.loads(file.read())

url = "http://ekalavya.it.iitb.ac.in/summerinternship2017/animationlist.html"
web_page = urlopen(url).read()

i, j = web_page.find(r'"animations"'), web_page.find(r'</table>')
n, cnt= web_page[i:j+1].count(r"<tr>") - 1, 0

while True:
	print("iteration #%d"%cnt)
	cnt+=1
	web_page = urlopen(url).read()
	i, j = web_page.find(r'"animations"'), web_page.find(r'</table>')
	l = web_page[i:j+1].count(r"<tr>")-1
	if n!=l or web_page[i:j+1].count("vailable")>0:
		handler = GmailHandler(account_info.email, account_info.password)
		handler.send_mail(to_notify, "something changed!", url)
		break

	the_time = time.localtime()
	print("sleeping", end=' ')
	print("%d:%d:%d"%(the_time.tm_hour, the_time.tm_min, the_time.tm_sec))

	time.sleep(600)