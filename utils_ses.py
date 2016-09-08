# -*- coding: utf-8 -*-
import boto.ses


class BotoSES:

    def __init__(self):
        pass

    def __init__(self, region, aws_access_key_id, aws_secret_access_key):
        self.__conn = boto.ses.connect_to_region(region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def send_email_raw(self, msg, recipients):
        return str(self.__conn.send_raw_email(msg.as_string(), source=msg['From'], destinations=[])['SendRawEmailResponse']['SendRawEmailResult']['MessageId'])
