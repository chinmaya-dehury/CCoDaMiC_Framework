import hashlib
import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback


class Authorizer(StreamCallback):

    def process(self, inputStream, outputStream):
        data = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        jsondata = json.loads(data)
        # we keep the informationof authorized source.
        # in real implementation it is the details from the sensors
        authorized_source = ['SENSOR_TEMP00X912', 'SENSOR_HUM00H212', 'SENSOR_CAM00S212']
        # check if source is present in our authorized list
        if jsondata[0]["source"] in authorized_source:
            jsondata[0]["issourcevalid"] = "VALID_SOURCE"
        else:
            jsondata[0]["issourcevalid"] = "INVALID_SOURCE"
        # write result
        outputStream.write(bytearray(json.dumps(jsondata, indent=3).encode('utf-8')))


flowFileSession = session.get()
if flowFileSession:
    flowFileSession = session.write(flowFileSession, Authorizer())
    flowFileSession = session.putAttribute(flowFileSession, "filename",
                                           flowFileSession.getAttribute('filename').split('.')[
                                               0] + '_secureresult.json')
session.transfer(flowFileSession, REL_SUCCESS)
session.commit()