from calendar import month
import requests
from requests.auth import HTTPBasicAuth
import datetime
import regex
url_Website = "http://192.168.50.16:8080" 
auth_Website = HTTPBasicAuth('admin', 'Vbpo@12345')

def get_notification():
    response = requests.request("GET", url_Website+"/manager/notification", auth=auth_Website)
    return response.json()

def post_notification(payload):
    response = requests.request("POST", url_Website+"/manager/notification", auth=auth_Website, data=payload)
    print(response.text)


while True:
    list_notification = get_notification()
    datetime_current = datetime.datetime.now()
    for i_notification in list_notification:
        datetime_before = datetime.datetime.strptime(i_notification['created_at'].split('.')[0],'%Y-%m-%dT%H:%M:%S')
        if "tháng" in i_notification['product']['estimate']:
            int_count = int(regex.findall(r'\d*',i_notification['product']['estimate'])[0])
            datetime_before = datetime_before + datetime.timedelta(days=int_count * 365/12)
            if datetime_before > datetime_current - datetime.timedelta(days=1):
                str_content = i_notification['product']['product'] + " sắp hết hạn"
                post_notification({"content":str_content,"user":i_notification['user'],"customer":i_notification['order']['customer'],"order":i_notification['order']['id'],"idproduct":i_notification['id']})
        
        elif "ngày" in i_notification['product']['estimate']:
            int_count = int(regex.findall(r'\d*',i_notification['product']['estimate'])[0])
            datetime_before = datetime_before + datetime.timedelta(days=int_count)
            if datetime_before > datetime_current - datetime.timedelta(days=1):
                str_content = i_notification['product']['product'] + " sắp hết hạn"
                post_notification({"content":str_content,"user":i_notification['user'],"customer":i_notification['order']['customer'],"order":i_notification['order']['id'],"idproduct":i_notification['id']})

        else:
            pass
    break
