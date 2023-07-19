import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from django.contrib.auth.hashers import check_password, make_password
from .models import CustomUser
class Utils:
    @staticmethod
    def sendMail(data):
        # port = 465 
        # smtp_server = "smtp.gmail.com"
        sender_email = "abdul.test87@gmail.com"
        receiver_email = data.get('to_email')
        password = '1Fatimat@'
        subject = "Hi {name}, kindly very your mail".format(name=data.get('user'))
        body = "Use the link {link} to verify your email address".format(link=data.get('link'))
        msg=f'Subject: {subject} \n\n {body}'
        message = """\
                    Subject: Anand.com
                    Use the link {link} to verify your email address
                """.format(link=data.get('link'))
 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465 ) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg)

    @staticmethod
    def validate_login_parameters(data, Model):
        password = data.get('password')
        email = data.get('email')

        if not password or not email:
            raise ValueError("Password or Email must be provided")
        try:
            user = Model.objects.get(email=email)
        except Model.DoesNotExist:
            raise ValueError("User does not exist")
        
        if not check_password(password, user.password):
            raise ValueError("Incorrect Password, please retry")
        
        return user