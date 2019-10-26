import hashlib
import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
 
class Validator(StreamCallback):

  def process(self, inputStream, outputStream):
    data = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    jsondata = json.loads(data)
    #validate the data based on checksum
    if jsondata[0]["issourcevalid"] == "VALID_SOURCE":
        datatohash = jsondata[0]["data"]
        if jsondata[0]["hashkey"] == hashlib.md5(datatohash.encode()).hexdigest().upper():
            jsondata[0]["isdatavalid"] = "VALID_DATA"
        else:
            jsondata[0]["isdatavalid"] = "INVALID_DATA"
    else:
        jsondata[0]["isdatavalid"] = "INVALID_DATA"
    # write result
    outputStream.write(bytearray(json.dumps(jsondata, indent=3).encode('utf-8')))
 
flowFileSession = session.get()
if flowFileSession:
  flowFileSession = session.write(flowFileSession, Validator())
  flowFileSession = session.putAttribute(flowFileSession, "filename", flowFileSession.getAttribute('filename').split('.')[0]+'_secureresult.json')
session.transfer(flowFileSession, REL_SUCCESS)
session.commit()