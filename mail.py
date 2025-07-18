import email, smtplib, imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os



class Mail():
    def __init__(self, smtp: str, imap: str, login: str, password: str):
        """
        Инициализация класса Mail
        :param smtp: SMTP сервер
        :param imap: IMAP сервер
        :param login: логин
        :param password: пароль
        """
        self.smtp = smtp
        self.imap = imap
        self.login = login
        self.password = password

    def send_email(self, recipients: list[str], subject: str, message: str):
        """
        Отправка письма
        :param recipients: список получателей
        :param subject: тема письма
        :param message: текст письма
        :return:
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.login
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(message))

            mail_server = smtplib.SMTP(self.smtp, 587)
            # identify ourselves to smtp gmail client
            # mail_server.ehlo()
            # secure our email with tls encryption
            mail_server.starttls()
            # re-identify ourselves as an encrypted connection
            mail_server.ehlo()
            # Здесь ещё всё хорошо
            mail_server.login(self.login, self.password) # А здесь нет
            text = msg.as_string()
            mail_server.sendmail(self.login, recipients, text)

        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            mail_server.quit()

    def receive_email(self, header: str = None):
        """
        Получение писем
        :param header: Критерии по заголовку
        :return:
        """
        try:
            mail_server = imaplib.IMAP4_SSL(self.imap)
            mail_server.login(self.login, self.password)
            mail_server.list()
            mail_server.select("inbox")
            criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
            result, data = mail_server.search(None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            result, data = mail_server.fetch(latest_email_uid, '(RFC822)')
            raw_email = data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email)
            mail_server.close()
            mail_server.logout()
            return email_message
        except imaplib.IMAP4.error as err:
            print(f"Ошибка IMAP: {err}")
            raise err
        except Exception as err:
            print('Что - то пошло не так...')
            raise err



if __name__ == '__main__':
    load_dotenv()

    GMAIL_SMTP = os.getenv('GMAIL_SMTP')
    GMAIL_IMAP = os.getenv('GMAIL_IMAP')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')

    mail1 = Mail(GMAIL_SMTP, GMAIL_IMAP, LOGIN, PASSWORD)
    recipients = ['vasya@email.com', 'petya@email.com']
    subject = 'Subject'
    message = 'Message'
    header = None

    mail1.send_email(recipients, subject, message)

    print(mail1.receive_email(header))

