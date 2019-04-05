# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask_restplus import Resource, Api, apidoc
from dbManipulation import write_db, feature_map, get_slicedData
from json import loads, dumps

db_name = 'heart_disease.db'
total_feature = 14
app = Flask(__name__)
api = Api(app, version='1.0', title='Heart Disease',
          description='Data set clean and heart disease prediction',)

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

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/getData/<data_type>', endpoint="getData")
class getData(Resource):
    def get(self, data_type):
        try:
            data_type = int(data_type)
            if data_type not in range(3, total_feature):
                return Response(status=404, response="Data type label should in range 3-" + str(total_feature - 1))
        except:
            return Response(status=404, response="Data type label should in range 1-14 in integer.")
        context = get_slicedData(data_type)
        return Response(status=200, response=dumps(context,
                                                    sort_keys=False,
                                                    indent=4))

if __name__ == '__main__':
    app.run(debug=True)