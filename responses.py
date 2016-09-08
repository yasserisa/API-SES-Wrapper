# -*- coding: utf-8 -*-
from flask import jsonify


class response:

    def __init__(self):
        pass

    def return_id_ses(self,id_ses):
        mensaje = {"MessageId": id_ses}
        return jsonify(mensaje), 200

    def trace_error_in_dbm(self):
        mensaje = {"error": "Message sent, but it was not possible to save the id"}
        return jsonify(mensaje), 202

    def invalid_request(self):
        mensaje = {"error": "Bad Request"}
        return jsonify(mensaje), 400

    def internal_error(self):
        mensaje = {"error": "Internal Error"}
        return jsonify(mensaje), 500

    def checksum_error(self):
        mensaje = {"error": "Checksum error"}
        return jsonify(mensaje), 409

    def not_verified(self):
        mensaje = {"error": "Source Email address is not verified"}
        return jsonify(mensaje), 403

    def unauthorized(self):
        mensaje = {"error": "This app is not Authorized"}
        return jsonify(mensaje), 401
