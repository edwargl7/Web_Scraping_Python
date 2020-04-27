from flask import Flask, jsonify
from flask_restful import Api

from web_scraping import WebScraping

app = Flask(__name__)
api = Api(app)
scraping = WebScraping()
base_url = 'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro='


# 00000000013887


@app.route('/basic-data/<id>')
def get_basic_data(id):
    try:
        url = base_url + str(id)
        scraping.get_data_without_filter(url)
        data, msg = scraping.get_basic_data(url)
        if data:
            response = {'data': data, 'message': msg}
            return jsonify(response), 200
        else:
            msg = 'data not found, ' + msg
            response = {'data': data, 'message': msg}
            return jsonify(response), 404
    except Exception as ex:
        msg = 'data not found, ' + str(ex)
        response = {'message': msg}
        return jsonify(response), 404


@app.route('/institutions/<id>')
def get_institutions(id):
    try:
        url = base_url + str(id)
        scraping.get_data_without_filter(url)
        data, msg = scraping.get_list_of_institutions(url)
        if data:
            response = {'data': data, 'message': msg}
            return jsonify(response), 200
        else:
            msg = 'data not found, ' + msg
            response = {'data': data, 'message': msg}
            return jsonify(response), 404
    except Exception as ex:
        response = {'message': str(ex)}
        return jsonify(response), 404


@app.route('/strategic_plan/<id>')
def get_strategic_plan(id):
    try:
        url = base_url + str(id)
        scraping.get_data_without_filter(url)
        data, msg = scraping.get_strategic_plan(url)
        if data:
            response = {'data': data, 'message': msg}
            return jsonify(response), 200
        else:
            msg = 'data not found, ' + msg
            response = {'data': data, 'message': msg}
            return jsonify(response), 404
    except Exception as ex:
        response = {'message': str(ex)}
        return jsonify(response), 404


@app.route('/lines_of_investigation/<id>')
def get_lines_investigation(id):
    try:
        url = base_url + str(id)
        scraping.get_data_without_filter(url)
        data, msg = scraping.get_lines_of_investigation(url)
        if data:
            response = {'data': data, 'message': msg}
            return jsonify(response), 200
        else:
            msg = 'data not found, ' + msg
            response = {'data': data, 'message': msg}
            return jsonify(response), 404
    except Exception as ex:
        response = {'message': str(ex)}
        return jsonify(response), 404


@app.route('/members/<id>')
def get_members(id):
    try:
        url = base_url + str(id)
        scraping.get_data_without_filter(url)
        data, msg = scraping.get_members(url)
        if data:
            response = {'data': data, 'message': msg}
            return jsonify(response), 200
        else:
            msg = 'data not found, ' + msg
            response = {'data': data, 'message': msg}
            return jsonify(response), 404
    except Exception as ex:
        response = {'message': str(ex)}
        return jsonify(response), 404


if __name__ == '__main__':
    app.run(debug=True)
