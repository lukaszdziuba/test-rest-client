from testrestclient.restcall import RestCall

request_details="""
GET https://jsonplaceholder.typicode.com/posts/1
HEADERS:
PARAMS:
BODY:
"""

restCall = RestCall(request_details)
restCall.makeCall()

