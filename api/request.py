import requests
from rest_framework.utils import json

header = {'content-type': 'application/json'}


r = requests.post(url="http://127.0.0.1:8007/api/login/",
                  data= json.dumps({'id':'2', 'password':'1234'})
                  , headers=header)
token = r.json()['token']
print(token)
#
header1 = {'content_type':'application/json', 'token':token}
# #
r = requests.get(url="http://127.0.0.1:8007/api/colleges/Amirkabir/departments/CEIT/courses/DB/sections/2/stds/", headers=header1)
#


print(r.json())