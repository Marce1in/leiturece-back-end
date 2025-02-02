import ssl
from contextlib import asynccontextmanager
from aiosmtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from typing import Annotated, AsyncGenerator

from fastapi.params import Depends

from ...settings import config


class EmailHandler:
    def __init__(self):
        self.__sender_email = config.EMAIL_SENDER

        self.__server_host = config.EMAIL_SERVER_HOST
        self.__server_port = config.EMAIL_SERVER_PORT

        self.__password = config.EMAIL_PASSWORD
        self.__username = config.EMAIL_USERNAME

        self.__domain = config.BACKEND_DOMAIN

        self.__context = ssl.create_default_context()

    def message_maker(self, receiver_email, subject, html_body, text_body):
        message = MIMEMultipart("alternative")

        message["From"] = self.__sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = make_msgid(domain=self.__domain)
        message["MIME-Version"] = "1.0"

        message.attach(MIMEText(text_body, "plain", "utf-8"))
        message.attach(MIMEText(html_body, "html", "utf-8"))

        message.add_header("Content-Type", 'text/html; charset="UTF-8"')

        return message

    @asynccontextmanager
    async def get_smtp_connection(self) -> AsyncGenerator[SMTP]:
        smtp = SMTP(
            hostname=self.__server_host,
            port=self.__server_port,
            tls_context=self.__context,
        )
        try:
            await smtp.connect()
            await smtp.login(self.__username, self.__password)
            yield smtp
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
        finally:
            await smtp.quit()

    async def send_email(self, subject, receiver_email, html_body, text_body):
        message = self.message_maker(receiver_email, subject, html_body, text_body)

        async with self.get_smtp_connection() as smtp:
            await smtp.send_message(message)

    def send_email_with_file(self):
        pass


email_handler = EmailHandler()


def get_email_handler():
    return email_handler


email_dependency = Annotated[EmailHandler, Depends(get_email_handler)]
