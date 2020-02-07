import smtplib
from email.mime.text import MIMEText
import argparse
from threading import Thread
import time


parser = argparse.ArgumentParser()
parser.add_argument('sender')
parser.add_argument('receiver')
parser.add_argument('password')
parser.add_argument('file')
res = parser.parse_args()

def send_notification(sender,receiver,password):
    content = "error from http://138.197.129.191"
    msg = MIMEText("")
    msg['Subject'] = content
    msg['From'] = sender
    msg['To'] = receiver
    
    
    smtp_host = 'smtp.live.com'
    
    s = smtplib.SMTP(smtp_host, 587, timeout=10)
    s.set_debuglevel(1)
    try:
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, receiver, msg.as_string())
    finally:
        s.quit()



class MyThread(Thread):
    def __init__(self,file):
        Thread.__init__(self,daemon=True)
        self.running = True
        self.file = file
        self.fcount = self.count()

    def run(self):
        while self.running:
            if (self.count()-self.fcount > 10):
                send_notification(res.sender,res.receiver,res.password)
                self.stop()
            time.sleep(1800)
            
    def stop(self):
        self.running = False
        
    def count(self):
        count = 0
        with open(self.file, 'r') as f:
            for line in f:
                count += 1
        return count

th = MyThread(res.file)
th.run()
