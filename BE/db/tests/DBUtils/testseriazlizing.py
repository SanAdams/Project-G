import json
from serializing import serialized

ex = serialized()
exjson = json.dumps(ex.__dict__)

print(exjson)


