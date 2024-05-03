import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class mail_sender:
    def __init__(self, receiver_email: str, sender_email: str, sender_password: str):
        self.receiver_email = receiver_email

        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 465

        self.sender_email = sender_email
        self.sender_password = sender_password

    def send(self, attachment_path: str):
        message = self.__create_message__(attachment_path)

        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
        print('이메일이 성공적으로 전송되었습니다.')

    def __create_message__(self, attachment_path: str) -> MIMEMultipart:
        subject = '폴리포니 졸업식 환송회 이미지 분류 사진'
        body = f'실행 시작 시간 : {datetime.now()}'

        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        if not attachment_path:
            return message

        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), 'gzip')
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
            message.attach(attachment)

        return message
