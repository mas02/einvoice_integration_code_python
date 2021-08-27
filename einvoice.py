import os
import sys
import random
import string
import pytz
import json
import traceback
import base64  # import base64 encodool0
from time import sleep
from datetime import datetime, timedelta
from bson import ObjectId
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from einvoice_sdk import security as views
from common import Common
import constants as CONSTANTS


def get_access_token():
    
    asp_user_data ={}
    response = {}
    requestData = {}    
    decodeResult = {} 
    asp_user_data['username'] = CONSTANTS.accessTokenInfo['username']
    asp_user_data['password'] = CONSTANTS.accessTokenInfo['password']
    asp_user_data['client_id'] = CONSTANTS.accessTokenInfo['client_id']
    asp_user_data['client_secret'] = CONSTANTS.accessTokenInfo['client_secret']
    asp_user_data['grant_type'] = CONSTANTS.accessTokenInfo['grant_type']
    
    json_data = json.dumps(asp_user_data)
    common_obj = Common()
    # generate 16 digit random key
    asp_app_key = common_obj.get_random_code(16) 
    # encrypt the credential data with 16 digit random key
    credential_data = views.encrypt_with_asp_key(asp_app_key, json_data)
    # encrypt 16 digit random key with the masters india sever.crt file
    encpt_asp_app_key = views.encrypt_with_public_key(asp_app_key, 'gst')             
    requestData['credentials_data'] = credential_data.decode('utf8')
    requestData['app_key'] = encpt_asp_app_key.decode('utf8')            
    url = CONSTANTS.gstr_urls["ACCESS_TOKEN"]

    payload = json.dumps(requestData) 
    result = views.send_request(url, payload, 'POST')
    decodeResult = json.loads(result)
    decodeResult['asp_app_key'] = asp_app_key
    
    return decodeResult
    # print(decodeResult)
    # exit()

# Authenticate from NIC
def einv_auth_token():
    token = get_access_token()
    other_params = {
                    'access_token': token['accessToken']
                }
    other_parameters = json.dumps(other_params)
    # Other parameters
    encrptedOthrParam = views.encrypt_with_asp_key(token['asp_app_key'], other_parameters)

    common_obj = Common()
    app_key_data = common_obj.get_random_code(32)
    flat_app_key = base64.b64encode(app_key_data.encode('utf8')).decode()
    
    fields = dict()
    req_data = dict()
    req_data['UserName'] = CONSTANTS.GstinInfo['einv_username']
    req_data['Password'] = CONSTANTS.GstinInfo['einv_password']    
    req_data['AppKey'] = flat_app_key     
    req_data['ForceRefreshAccessToken'] = False
    request = (base64.b64encode(json.dumps(req_data).encode('utf8'))).decode('utf8')
    encrpted_data = views.encrypt_with_public_key(request, 'qa-gst')

    fields['Data'] =encrpted_data.decode('utf8') 
    fields['other_parameters'] = encrptedOthrParam.decode('utf8')    
    payload = json.dumps(fields)

    header = dict()    
    header['client-id'] = CONSTANTS.accessTokenInfo['client_id']
    header['Gstin'] = CONSTANTS.GstinInfo['gstin']    

    url = CONSTANTS.gstr_urls['auth_url']    
    result = views.send_request(url, payload, 'POST',header)
    
    if result:        
        decodeResult = json.loads(result)        
        response = {}
        if 'Status' in decodeResult and decodeResult['Status'] == 1:
            
            response['ClientId'] = decodeResult['Data']['ClientId']
            response['UserName'] = decodeResult['Data']['UserName']
            response['Sek'] = decodeResult['Data']['Sek']
            response['AuthToken'] = decodeResult['Data']['AuthToken'] 
            response['TokenExpiry'] = decodeResult['Data']['TokenExpiry']
            response['Status'] = decodeResult['Status']
            response['ErrorDetails'] = decodeResult['ErrorDetails']
            response['flat_app_key'] = flat_app_key            
            response['other_parameters'] = encrptedOthrParam.decode('utf8')            
            response['error'] = False
        else:                
            if 'ErrorDetails' in decodeResult and decodeResult['ErrorDetails'] is not None:
                response['ErrorDetails'] = decodeResult['ErrorDetails']
                response['Status'] = decodeResult['Status'] 
                response['error'] = True              
                
    else:
        msg = 'Service unavailable. Please try again later'
        response['error'] = True
        response['message'] = msg


    # return response
    print("response===>",response)
    exit()

def generate_irn():    
    
    token = get_access_token()
    other_params = {
                    'access_token': token['accessToken']
                }
    other_parameters = json.dumps(other_params)
    # Other parameters
    encrptedOthrParam = views.encrypt_with_asp_key(token['asp_app_key'], other_parameters)

    # einvoice_auth_token = einv_auth_token()
    # flat_app_key = einvoice_auth_token['flat_app_key']    
    # 32 random character(base64 encode) which is used in auth token API
    flat_app_key = 'UzNpakNTZTFpN3FlcVM4OHpwZXRCdEZkb215amgzOUM='

    # auth token received in auth token API  
    # auth_token = einvoice_auth_token['AuthToken']
    auth_token = 'alTFt3n6XoAjGw5EdtBQQYGk6'

    # Sek received in auth token API     
    # sek = einvoice_auth_token['Sek']     
    sek = 'axAUznCA+e2bjnYbbLKjPxoY8rf5K+O9b/UGRIO8OrlQbQNZUaEvMN3l6k7rDFIE'
    
    ek = base64.b64encode(views.decrypt_data(sek, flat_app_key, 'byte')).decode('utf8')
    data_json =  CONSTANTS.data_json
    
    data = views.encrypt_data(data_json, ek, type = 'str')
    
    encrpted_data = data.decode('utf8')
    
    fields={}
    fields['Data'] =encrpted_data
    
    fields['other_parameters'] = encrptedOthrParam.decode('utf8')
    
    payload = json.dumps(fields)
    url = CONSTANTS.gstr_urls['gen_einv']
    header = {}
    header['AuthToken']= auth_token
    header['user_name']= CONSTANTS.GstinInfo['einv_username']
    header['Gstin']= CONSTANTS.GstinInfo['gstin']
    header['client-id']=CONSTANTS.accessTokenInfo['client_id']
    method = 'POST' 
    result= views.send_request(url, payload, method, header)

    if result:
        response={}
        decodeResult = json.loads(result)
        if 'Status' in decodeResult and decodeResult['Status'] == 1:
            data = views.decrypt_data(decodeResult['Data'], ek)
            response['data'] = data.decode('utf8')
            response['error'] = False
            
        else:  
            response['data'] = decodeResult
            response['error'] = True             
            
    else:
        msg = 'Service unavailable. Please try again later'
        response['error'] = True
        response['message'] = msg

    print("response===>",response)
    exit()
    return response

def cancel_irn():    
    
    token = get_access_token()
    other_params = {
                    'access_token': token['accessToken']
                }
    other_parameters = json.dumps(other_params)
    # Other parameters
    encrptedOthrParam = views.encrypt_with_asp_key(token['asp_app_key'], other_parameters)

    # einvoice_auth_token = einv_auth_token()
    # flat_app_key = einvoice_auth_token['flat_app_key']    
    # 32 random character(base64 encode) which is used in auth token API
    flat_app_key = 'UzNpakNTZTFpN3FlcVM4OHpwZXRCdEZkb215amgzOUM='

    # auth token received in auth token API  
    # auth_token = einvoice_auth_token['AuthToken']
    auth_token = 'alTFt3n6XoAjGw5EdtBQQYGk6'

    # Sek received in auth token API     
    # sek = einvoice_auth_token['Sek']     
    sek = 'axAUznCA+e2bjnYbbLKjPxoY8rf5K+O9b/UGRIO8OrlQbQNZUaEvMN3l6k7rDFIE'
    
    ek = base64.b64encode(views.decrypt_data(sek, flat_app_key, 'byte')).decode('utf8')
    data_json =  CONSTANTS.cancel_irn_json
    
    data = views.encrypt_data(data_json, ek, type = 'str')
    
    encrpted_data = data.decode('utf8')
    
    fields={}
    fields['Data'] =encrpted_data
    
    fields['other_parameters'] = encrptedOthrParam.decode('utf8')
    
    payload = json.dumps(fields)
    url = CONSTANTS.gstr_urls['cancel_einv']
    header = {}
    header['AuthToken']= auth_token
    header['user_name']= CONSTANTS.GstinInfo['einv_username']
    header['Gstin']= CONSTANTS.GstinInfo['gstin']
    header['client-id']=CONSTANTS.accessTokenInfo['client_id']
    method = 'POST'
    result= views.send_request(url, payload, method, header)
   
    
    if result:
        response={}
        decodeResult = json.loads(result)
        if 'Status' in decodeResult and decodeResult['Status'] == 1:
            data = views.decrypt_data(decodeResult['Data'], ek)
            response['data'] = data.decode('utf8')
            response['error'] = False
            
        else:  
            response['data'] = decodeResult
            response['error'] = True             
            
    else:
        msg = 'Service unavailable. Please try again later'
        response['error'] = True
        response['message'] = msg

    print("cancel response===>",response)
    exit()
    return response


def get_irn():

    token = get_access_token()
    other_params = {
                    'access_token': token['accessToken']
                }
    other_parameters = json.dumps(other_params)
    # Other parameters
    encrptedOthrParam = views.encrypt_with_asp_key(token['asp_app_key'], other_parameters)

    # einvoice_auth_token = einv_auth_token()

    # 32 random character(base64 encode) which is used in auth token API
    # flat_app_key = einvoice_auth_token['flat_app_key']    
    flat_app_key = 'UzNpakNTZTFpN3FlcVM4OHpwZXRCdEZkb215amgzOUM='

    # auth token received in auth token API  
    # auth_token = einvoice_auth_token['AuthToken']
    auth_token = 'alTFt3n6XoAjGw5EdtBQQYGk6'

    # Sek received in auth token API     
    # sek = einvoice_auth_token['Sek']     
    sek = 'axAUznCA+e2bjnYbbLKjPxoY8rf5K+O9b/UGRIO8OrlQbQNZUaEvMN3l6k7rDFIE'
    
    ek = base64.b64encode(views.decrypt_data(sek, flat_app_key, 'byte')).decode('utf8')

    irn_no ="0657ea66f6461c473a05754b5cdee3531032924fe81635a6433fdd9313125b1b"
    
    url = CONSTANTS.gstr_urls['get_einv']
    url = url+irn_no+'?other_parameters='+encrptedOthrParam.decode('utf8')
    header = {}
    header['AuthToken']= auth_token
    header['user_name']= CONSTANTS.GstinInfo['einv_username']
    header['Gstin']= CONSTANTS.GstinInfo['gstin']
    header['client-id']=CONSTANTS.accessTokenInfo['client_id']
    
    
    result= views.send_request(url, '', '', header)    
    if result:
        response={}
        decodeResult = json.loads(result)
        if 'Status' in decodeResult and decodeResult['Status'] == 1:
            data = views.decrypt_data(decodeResult['Data'], ek)
            response['data'] = data.decode('utf8')
            response['error'] = False
            
        else:  
            response['data'] = decodeResult
            response['error'] = True             
            
    else:
        msg = 'Service unavailable. Please try again later'
        response['error'] = True
        response['message'] = msg

    print("Get IRN response===>",response)
    exit()
    return response



if __name__ == "__main__":
    # get_access_token()
    einv_auth_token()
    # generate_irn()
    # cancel_irn()
    # get_irn()