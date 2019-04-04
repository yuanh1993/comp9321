# -*- coding: utf-8 -*-
from flask import Flask, Response
from flask_restplus import Resource, Api, apidoc

db_name = 'heart_disease.db'
app = Flask(__name__)
api = Api(app, version='0.1', title='Heart Disease',
          description='Data set clean and heart disease prediction')

@api.documentation
def swagger_UI():
    return apidoc.ui_for(api)

if __name__ == '__main__':
    app.run()