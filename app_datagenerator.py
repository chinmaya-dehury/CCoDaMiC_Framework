from flask import Flask,request
from flask_restful import Resource, Api
import string
import numpy as np
import random
import hashlib

app = Flask(__name__)
api = Api(app)

class DataSourceGenerator(Resource):

    def invalid_source(self):
        invalidsource = ['SENSOR_00X912', 'SENSOR_TVM00H212']
        return invalidsource[np.random.randint(2)]

    def get_source(self):
        authorized_source = ['SENSOR_TEMP00X912', 'SENSOR_HUM00H212', 'SENSOR_CAM00S212']
        return authorized_source[np.random.randint(3)]

    def generateRandomString(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(80))

    def generateMD5hash(self, inputString):
        return hashlib.md5(inputString.encode()).hexdigest().upper()

    def post(self):

        inputdata = request.get_json(force=True)
        if inputdata["user"] == "tekraj" and inputdata["password"] =="1235@S":
            if inputdata["request"] == "GENERATE_DATA":

                if np.random.sample() > 0.3:
                    source = self.get_source()
                else:
                    source = self.invalid_source()

                generatedString = self.generateRandomString()
                generatedhash = self.generateMD5hash(generatedString)

                generated_data = {
                        "source":source,
                        "data": generatedString,
                        "hash":generatedhash
                    }
                return generated_data


api.add_resource(DataSourceGenerator, '/')


if __name__ == '__main__':
    app.run(debug=True)