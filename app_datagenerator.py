from flask import Flask,request
from flask_restful import Resource, Api
import string
import numpy as np
import random
import hashlib
import datetime
app = Flask(__name__)
api = Api(app)

class NifiFunction(Resource):

    def get_source(self):
        authorized_source = ['SENSOR_TEMP00X912', 'SENSOR_HUM00H212', 'SENSOR_CAM00S212']
        return authorized_source[np.random.randint(3)]

    def generateRandomString(self):
        n = 1024 ** 2  # 1 Mb of text
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(n))

    def generateMD5hash(self, inputString):
        return hashlib.md5(inputString.encode()).hexdigest().upper()

    def post(self):

        inputdata = request.get_json(force=True)

        if inputdata["user"] == "tekraj" and inputdata["password"] =="1235@S":
            if inputdata["request"] == "GENERATE_DATA":
                source = self.get_source()
                generatedString = self.generateRandomString()
                generatedhash = self.generateMD5hash(generatedString)

                generated_data = {
                        "source":source,
                         "data_gen_time": str(datetime.datetime.now()),
                        "hash":generatedhash,
                         "data": generatedString,
                    }

                return generated_data


api.add_resource(NifiFunction, '/')


if __name__ == '__main__':
    app.run(debug=True)