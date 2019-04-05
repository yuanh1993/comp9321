# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask_restplus import Resource, Api, apidoc
from dbManipulation import write_db

db_name = 'heart_disease.db'
app = Flask(__name__)
api = Api(app, version='1.0', title='Heart Disease',
          description='Data set clean and heart disease prediction',)

feature_map = {
    0: 'index',
    1: 'age real',
    2: 'sex real',
    3: 'pain_type real',
    4: 'blood_pressure real',
    5: 'cholestoral real',
    6: 'blood_sugar real',
    7: 'electrocardiographic real',
    8: 'heart_rate real',
    9: 'angina real',
    10: 'oldpeak real',
    11: 'ST_segment real',
    12: 'vessels real',
    13: 'thal real',
    14: 'target integer'
}

@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/writeDB', endpoint="writeDB")
class writeDB(Resource):
    def get(self):
        write_db()
        return Response(status=200, response="Done: load data to database.")
if __name__ == '__main__':
    app.run()