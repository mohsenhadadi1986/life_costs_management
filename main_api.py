from flask import Flask, request
import flask
from core.api.import_page import import_dropdown_query, import_data_query
from core.api.report_page import report_table_query
import json
from loguru import logger


app = Flask(__name__)
app.config["DEBUG"] = True
HTTP_SUCCESSFUL_CODE = 200
HTTP_FAILED_CODE = 400
HTTP_ERROR_CODE = 500
HTTP_UNAUTHORIZED_CODE = 401


@app.route('/api/v1/dropdown_options', methods=['GET'])
def api_dropdown_options():
    '''
    This GET api provides a dictionary as following 
        dict = {
        category1: [reason0, reason1, ...],
        category2: [reason0, reason1, ...], ...
        }
    '''
    options = import_dropdown_query()
    return options


@app.route('/api/v1/import_data', methods=['POST'])
def api_dropdown_import_data():
    '''
    This POST api forward the following data into db 
        category,reason, value, import_date

    Returns:
           True or False
    '''
    try:
        if isinstance(request.json, str):
            json_data = json.loads(request.json)
        elif isinstance(request.json, dict):
            json_data = request.json
        else:
            raise IOError('Unsupported data format')
        category = json_data['category']
        reason = json_data['reason']
        value = json_data['value']
        import_date = json_data['import_date']
        import_list = (category, reason, value, import_date)
        result = import_data_query(import_list)
        if result is True:
            response = flask.jsonify({
                'response': 'the data has inserted successfully.'
            })
            return response, HTTP_SUCCESSFUL_CODE
    except Exception as e:
        logger.info(f'{e}')
        response = flask.jsonify(False)
        return response, HTTP_ERROR_CODE


@app.route('/api/v1/report/<year>', methods=['GET'])
def api_report(year: str):
    '''
    This GET api provides a csv file stored in datasets folder is called by report_year.csv
    '''
    try:
        report = report_table_query(year)
        if report is True:
            response = flask.jsonify({
                'response': 'the data has loaded successfully for year {}'.format(year)
            })
            return response, HTTP_SUCCESSFUL_CODE
    except Exception as e:
        logger.info(f'{e}')
        response = flask.jsonify(False)
        return response, HTTP_ERROR_CODE


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)
# app.run(debug=True)   # http://127.0.0.1:5000/
