# -*- coding: utf-8 -*-
from flask import Flask, request
import json
from dbm import Connector_DBM
from responses import response
from utils_ses import BotoSES
from utils import check_body, MIME_utils, check_checksum

# init app
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Connections
dbm = Connector_DBM(app.config['DBM_HOST'], app.config['DBM_PORT'], app.config[
                    'DBM_USER'], app.config['DBM_PASSWORD'], app.config['DBM_DB'])
conn = BotoSES(app.config['REGION'], app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])


@app.route(app.config['PATH'] + '/' + app.config['VERSION'] + '/send', methods=['POST'])
def api_send():
    # Check Content-Type, Body and required keys in json body
    try:
        body = json.loads(request.get_data().decode('utf-8'))
        if not check_body().check_body_json(body, app.config['BODY_SCHEMA_PROD']):
            raise
    except:
        return response().invalid_request()
    # Check is APP is registered
    name_app = dbm.verify_app(body['token_app'])
    if name_app is not None:
        body['name_app'] = name_app
    else:
        return response().unauthorized()
    # Verify checksum
    if "files" in body:
        if not check_checksum().check_sha256_file(body['files']):
            return response().checksum_error()
    # Delete key Files to insert in DBM
    try:
        insert = body.copy()
        del insert['files']
        del insert['body']
    except:
        pass
    # Insert JSON in DBM
    try:
        id_row = dbm.insert_email(insert, False)
        trace = True
    except:
        trace = False
    # Set mail
    try:
        msg = MIME_utils().set_message(body)
    except Exception, e:
        print str(e)
        return response().internal_error()
    # Send mail
    try:
        MessageId = conn.send_email_raw(msg, body['to'])
    except Exception, e:
        try:
            dbm.log_error(str(e))
        except:
            pass
        if "Email address is not verified" in str(e):
            return response().not_verified()
        return response().internal_error()
    # Save id in DBM
    if trace:
        try:
            dbm.update_email(id_row, MessageId)
            return response().return_id_ses(MessageId)
        except:
            return response().trace_error_in_dbm()
    else:
        return response().trace_error_in_dbm()

@app.route(app.config['PATH'] + '/' + app.config['VERSION'] +  '/send-test', methods=['POST'])
def api_send_test():
    # Check Content-Type, Body and required keys in json body
    try:
        body = json.loads(request.get_data().decode('utf-8'))
        if not check_body().check_body_json(body, app.config['BODY_SCHEMA_TEST']):
            raise
    except:
        return response().invalid_request()
    # Check is APP is registered
    name_app = dbm.verify_app(body['token_app'])
    if name_app is not None:
        body['name_app'] = name_app
    else:
        return response().unauthorized()
    # Verify checksum
    if "files" in body:
        if not check_checksum().check_sha256_file(body['files']):
            return response().checksum_error()
    # Delete key Files to insert in DBM
    try:
        insert = body.copy()
        del insert['files']
        del insert['body']
    except:
        pass
    # Insert JSON in DBM
    try:
        id_row = dbm.insert_email(insert, True)
        trace = True
    except:
        trace = False
    # Set mail
    try:
        body['to'] = body['test_email_receiver']
        if "bcc" in body:
            body['bcc'] = body['test_email_receiver']
        if "cc" in body:
            body['cc'] = body['test_email_receiver']
        msg = MIME_utils().set_message(body)
    except Exception, e:
        print str(e)
        return response().internal_error()
    # Send mail
    try:
        MessageId = conn.send_email_raw(msg, body['to'])
    except Exception, e:
        try:
            dbm.log_error(str(e))
        except:
            pass
        if "Email address is not verified" in str(e):
            return response().not_verified()
        return response().internal_error()
    # Save id in DBM
    if trace:
        try:
            dbm.update_email(id_row, MessageId)
            return response().return_id_ses(MessageId)
        except:
            return response().trace_error_in_dbm()
    else:
        return response().trace_error_in_dbm()

if __name__ == '__main__':
    # Start app
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
