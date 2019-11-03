from flask import Flask,request
from flask_restful import Resource, Api
import hashlib

app = Flask(__name__)
api = Api(app)

class NifiFunction(Resource):

    def post(self):
        inputdata = request.get_json(force=True)
        if inputdata[0]["issourcevalid"] == "VALID_SOURCE" and inputdata[0]["isdatavalid"] == "VALID_DATA":
            inputdata[0]["data"] = inputdata[0]["data"]+" Added from Function to valid data"
            inputdata[0]["oldhashkey"] = inputdata[0]["hashkey"]
            inputdata[0]["hashkey"] =  hashlib.md5(inputdata[0]["data"].encode()).hexdigest().upper()
        else:
            inputdata[0]["data"] = inputdata[0]["data"] + " Added from Function to invalid data"
        return inputdata


api.add_resource(NifiFunction, '/')


if __name__ == '__main__':
    app.run(debug=True,port=50020)