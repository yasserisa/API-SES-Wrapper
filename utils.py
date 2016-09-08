# -*- coding: utf-8 -*-
from jsonschema import validate
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import hashlib

class check_body:

    def __init__(self):
        pass

    def check_body_json(self, body, schema):
        try:
            validate(body, schema)
            return True
        except:
            return False


class check_checksum:

    def __init__(self):
        pass

    def check_sha256_file(self, files_attach):
        for file_attach in files_attach:
            m = hashlib.sha256()
            m.update(str(file_attach['content']).decode("base64"))
            if not m.hexdigest() == file_attach['checksum']:
                return False
        return True


class MIME_utils:

    def __init__(self):
        pass

    def set_message(self, body):

        # Info message
        msg = MIMEMultipart()
        msg['Subject'] = body['subject'].decode('base64')
        msg['From'] = body['from']
        try:
            msg['Bcc'] = ', '.join(body['bcc'])
        except:
            pass
        try:
            msg['Cc'] = ', '.join(body['cc'])
        except:
            pass
        recipients = body['to']
        msg['To'] = ', '.join(recipients)
        msg.preamble = 'Multipart message.\n'
        # Body Message in HTML
        part2 = MIMEText(body['body'].decode('base64'), 'html')
        msg.attach(part2)
        try:
            # The attachment
            for file_attach in body['files']:
                part3 = MIMEApplication(file_attach['content'].decode('base64'))
                part3.add_header('Content-Disposition', 'attachment', filename=file_attach['file_name'])
                msg.attach(part3)
                return msg
        except:
            return msg
