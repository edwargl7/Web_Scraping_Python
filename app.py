from flask import Flask, jsonify
from flask_restplus import Api, Resource

from web_scraping import WebScraping

_DESCRIPTION = """
Esta API permite extraer información de los grupos registrados en \
el GrupLac, cuya información es tomada de la URL: 
https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/\
visualizagr.jsp?nro=ID \
,donde el ID es el número que identifica al grupo.
"""

app = Flask(__name__)
api = Api(app=app,
          version="1.0",
          title="API de Extracción de Datos del GrupLac de Colciencias",
          description=_DESCRIPTION, doc='/api/'
          )

name_space = api.namespace('api', description='Endpoints')
scraping = WebScraping()
base_url = 'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro='


# 00000000013887


@name_space.route('/basic-data/<id>')
class BasicData(Resource):
    @api.doc(
        responses={
            200: 'OK', 404: 'Data not found',
            500: 'It is not possible to obtain data from this url'},
        params={
            'id': 'Specify the Id associated with the group in Colciencias'})
    def get(self, id):
        try:
            url = base_url + str(id)
            req, msg = scraping.get_data_without_filter(url)
            if req:
                data, msg = scraping.get_basic_data(url)
                if data:
                    response = {'data': data, 'message': msg}
                    return response, 200
                else:
                    msg = 'data not found, ' + msg
                    response = {'data': data, 'message': msg}
                    return response, 404
            else:
                response = {'message': msg}
                return response, 500
        except Exception as ex:
            msg = 'data not found, ' + str(ex)
            response = {'message': msg}
            return response, 404


@name_space.route('/institutions/<id>')
class Institution(Resource):
    @api.doc(
        responses={
            200: 'OK', 404: 'Data not found',
            500: 'It is not possible to obtain data from this url'},
        params={
            'id': 'Specify the Id associated with the group in Colciencias'})
    def get(self, id):
        try:
            url = base_url + str(id)
            req, msg = scraping.get_data_without_filter(url)
            if req:
                data, msg = scraping.get_list_of_institutions(url)
                if data:
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 200
                else:
                    msg = 'data not found, ' + msg
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 404
            else:
                response = {'message': msg}
                return response, 500
        except Exception as ex:
            response = {'message': str(ex)}
            return jsonify(response), 404


@name_space.route('/strategic_plan/<id>')
class StrategicPlan(Resource):
    @api.doc(
        responses={
            200: 'OK', 404: 'Data not found',
            500: 'It is not possible to obtain data from this url'},
        params={
            'id': 'Specify the Id associated with the group in Colciencias'})
    def get(self, id):
        try:
            url = base_url + str(id)
            req, msg = scraping.get_data_without_filter(url)
            if req:
                data, msg = scraping.get_strategic_plan(url)
                if data:
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 200
                else:
                    msg = 'data not found, ' + msg
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 404
            else:
                response = {'message': msg}
                return response, 500
        except Exception as ex:
            response = {'message': str(ex)}
            return jsonify(response), 404


@name_space.route('/lines_of_investigation/<id>')
class LinesInvestigation(Resource):
    @api.doc(
        responses={
            200: 'OK', 404: 'Data not found',
            500: 'It is not possible to obtain data from this url'},
        params={
            'id': 'Specify the Id associated with the group in Colciencias'})
    def get(self, id):
        try:
            url = base_url + str(id)
            req, msg = scraping.get_data_without_filter(url)
            if req:
                data, msg = scraping.get_lines_of_investigation(url)
                if data:
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 200
                else:
                    msg = 'data not found, ' + msg
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 404
            else:
                response = {'message': msg}
                return response, 500
        except Exception as ex:
            response = {'message': str(ex)}
            return jsonify(response), 404


@name_space.route('/members/<id>')
class Member(Resource):
    @api.doc(
        responses={
            200: 'OK', 404: 'Data not found',
            500: 'It is not possible to obtain data from this url'},
        params={
            'id': 'Specify the Id associated with the group in Colciencias'})
    def get(self, id):
        try:
            url = base_url + str(id)
            req, msg = scraping.get_data_without_filter(url)
            if req:
                data, msg = scraping.get_members(url)
                if data:
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 200
                else:
                    msg = 'data not found, ' + msg
                    response = {'data': data, 'message': msg}
                    return jsonify(response), 404
            else:
                response = {'message': msg}
                return response, 500
        except Exception as ex:
            response = {'message': str(ex)}
            return jsonify(response), 404


if __name__ == '__main__':
    app.run(debug=False)
