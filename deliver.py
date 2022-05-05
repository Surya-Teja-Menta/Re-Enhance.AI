import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class Deliver:
    
    def send_email(self,email_address,path,user_root):
        try:    
            receiver=email_address
            print(receiver,type(receiver))
            sender='reenhanceai@gmail.com'
            msg=MIMEMultipart()
            msg['From']=sender
            msg['To']=receiver
            msg['Subject']='Re-Enhance AI'
            body='Hi,\n\nWe have Enhance your Requested image.\n Here, we have attached your image. \n\nThanks,\n\nTeam Re-Enchance.Ai'
            msg.attach(MIMEText(body,'plain'))
            attachment=open(path,'rb')
            ext=path.split('.')[-1]
            p=MIMEBase('application','octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition','attachment',filename=f'Enhanced_image.{ext}')
            msg.attach(p)
            s=smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login(sender,'**********')
            text=msg.as_string()
            s.sendmail(sender,receiver,text)
            s.quit()
            print('Email sent successfully')
            for i in os.listdir(f'outputs/{user_root}/'):
                os.remove(os.path.join(f'outputs/{user_root}',i))
            for i in os.listdir(f'inputs/{user_root}/'):
                os.remove(os.path.join(f'inputs/{user_root}',i))
            for i in os.listdir(f'results/{user_root}/'):
                os.remove(os.path.join(f'results/{user_root}',i))
            for i in os.listdir(f'web/{user_root}/'):
                os.remove(os.path.join(f'web/{user_root}',i))
            os.rmdir(f'outputs/{user_root}')
            os.rmdir(f'inputs/{user_root}')
            os.rmdir(f'web/{user_root}')
            os.rmdir(f'results/{user_root}') 
            print('All files/folders deleted successfully')    
            
        except Exception as e:
            print(e)

