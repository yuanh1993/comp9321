# -*- coding: utf-8 -*-

from flask import Flask, Response, request, Blueprint
from flask_restplus import Resource, Api, apidoc
from dbManipulation import (write_db, feature_map, get_slicedData,
                            RankFeatures, FeatureRankDB, readFeatureRank,
                            save_Learning_curve, get_Curve_DB)
from TrainModel import saveModel, readModel
from json import loads, dumps
from flask_cors import CORS
from WashDog import sweep, decoration

db_name = 'heart_disease.db'
total_feature = 14
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:4200", "http://localhost:4200"]}})
blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint, version='1.0', title='Heart Disease',
          description='Data set clean and heart disease prediction',)
app.register_blueprint(blueprint)


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
@api.doc(params = {'bucket_size': 'bucket_size'})
class getData(Resource):
    def get(self, data_type):
        try:
            request.args = request.args.to_dict()
            bucket_size = int(request.args['bucket_size'])
        except:
            bucket_size = 10
        try:
            data_type = int(data_type)
            if data_type not in range(3, total_feature):
                return Response(status=404, response="Data type label should in range 3-" + str(total_feature - 1))
        except:
            return Response(status=404, response="Data type label should in range 1-14 in integer.")
        context = get_slicedData(data_type, bucket_size=bucket_size)
        return Response(status=200, response=dumps(context,sort_keys=False,indent=4))

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/rankFeature', endpoint="rankFeature")
@api.doc(params = {'method': 'method'})
class rankFeature(Resource):
    def get(self):
        request.args = request.args.to_dict()
        try:
            method = request.args['method'].lower().strip()
            print(method)
            if method != 'knn' and method != 'drop':
                return Response(status=404, response='Only support KNN or drop method.')
        except:
            method = 'drop'
        context = readFeatureRank(method)
        return Response(status=200, response=dumps(context,
                                                    sort_keys=False,
                                                    indent=4))

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/rankFeature_toDB', endpoint="rankFeature_toDB")
@api.doc(params = {'method': 'method'})
class rankFeature_toDB(Resource):
    def get(self):
        request.args = request.args.to_dict()
        try:
            method = request.args['method'].lower().strip()
            print(method)
            if method != 'knn' and method != 'drop':
                return Response(status=404, response='Only support KNN or drop method.')
        except:
            method = 'drop'
        context = FeatureRankDB(method)
        return Response(status=200, response=dumps(context,
                                                    sort_keys=False,
                                                    indent=4))

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/saveCleanDataDB', endpoint="saveCleanDataDB")
@api.doc(params = {'method': 'method'})
class saveCleanDataDB(Resource):
    def get(self):
        request.args = request.args.to_dict()
        try:
            method = request.args['method'].lower().strip()
            print(method)
            if method != 'knn' and method != 'drop':
                return Response(status=404, response='Only support KNN or drop method.')
        except:
            method = 'drop'
        if method == 'drop':
            sweep()
            context = "Data cleaned with drop dirty data and saved to DB"
        else:
            decoration()
            context = "Data cleaned with KNN predict dirty data and saved to DB"
        return Response(status=200, response=context)

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/saveLearningCurve', endpoint="saveLearningCurve")
@api.doc(params = {'method': 'method', 'model_type':'model_type'})
class saveLearningCurve(Resource):
    def get(self):
        request.args = request.args.to_dict()
        try:
            method = request.args['method'].lower().strip()
            model_type = request.args['model_type'].lower().strip()
            if method != 'knn' and method != 'drop':
                return Response(status=404, response='Only support KNN or drop method.')
        except:
            method = 'drop'
            model_type = 'stack'
        save_Learning_curve(method = method, model_type = model_type)
        context = "Learning saved to DB"
        return Response(status=200, response=context)

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/saveModels', endpoint="saveModels")
@api.doc(params = {'method': 'method', 'model_type':'model_type'})
class saveModels(Resource):
    def get(self):
        request.args = request.args.to_dict()
        try:
            method = request.args['method'].lower().strip()
            model_type = request.args['model_type'].lower().strip()
            if method != 'knn' and method != 'drop':
                return Response(status=404, response='Only support KNN or drop method.')
        except:
            method = 'drop'
            model_type = 'stack'
        saveModel(method = method, model_type = model_type)
        context = "model saved as .sav"
        return Response(status=200, response=context)

@api.response(200, 'OK')
@api.response(404, 'Not found')
@api.route('/getCurve', endpoint="getCurve")
@api.doc(params = {'model_type':'model_type'})
class getCurve(Resource):
    def get(self):
        request.args = request.args.to_dict()
        try:
            model_type = request.args['model_type'].lower().strip()
        except:
            model_type = 'stack'
        context = get_Curve_DB(model_type = model_type)
        if context == None:
            return Response(status=404, response="Please train model before get curve.")
        return Response(status=200, response=dumps(context,
                                                   sort_keys=False,
                                                    indent=4))

if __name__ == '__main__':
    app.run(debug=True)
