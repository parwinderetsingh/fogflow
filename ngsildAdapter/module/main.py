#!/usr/bin/python
from flask import Flask, abort, request
import json
import pickle
import datetime
import io
import ConfigParser
from common_utilities.config import config_data
from common_utilities.rest_client import Rest_client
from common_utilities.LogerHandler import Handler
import requests
from consts import constant
from data_model.ld_generate import ngsi_data_creation
from data_model.orian_ld_genrate import orian_convert_data
from data_model.orian_ld_genrate import orian_convert_data
import copy
import logging
from consts import constant
app = Flask(__name__)
File_data={}
storage=[]
class patch_post:
    def __init__(self):
	pass

    def take_backup(self):
        logger_obj=Handler()
        logger=logger_obj.get_logger()
        try:
            id_file=open("data_model/storage/data_file.txt",'r+')
        except FileNotFoundError as fnf_error:
            message=fnf_error
            logger.error(message)
        logger.info("storing created Entity from file")    
        for x in id_file:
            x=x.rstrip("\n")
            File_data[x]=1
        logger.info("Clossing the file")
        id_file.close()
    def data_convert_invoker(self,context,dataObj):
        logger_obj=Handler()
        logger=logger_obj.get_logger()
        patch_context= copy.deepcopy(context)
        del patch_context["type"]
        del patch_context["id"]
        entity_id=dataObj.get_entityId()
        configobj=config_data()
        entity_url=configobj.get_entity_url()
        url1 =constant.http+entity_url+constant.entity_uri
        url2=constant.http+entity_url+constant.entity_uri+entity_id+'/attrs'
        if entity_id in File_data.keys():
            logger.info("sending update request")
            payload=json.dumps(patch_context)
            robj=Rest_client(url2,payload)
            r=robj.patch_request()
            if r.status_code==constant.update_status:
                logger.info("Entity has been updated to NGB")
        else:
            logger.info("Sending create request")
            payload=json.dumps(context)
            robj=Rest_client(url1,payload)
            r=robj.post_request()
            if r.status_code==constant.create_status:
                logger.info("Entity has been created in NGB")
                id_file=open("data_model/storage/data_file.txt",'a+')
                id_file.write(entity_id+'\n')
                File_data[entity_id]=1
                id_file.close()
@app.route('/notifyContext',methods=['POST'])
def noify_server():
    data=request.get_json()
    logger_obj=Handler()
    logger=logger_obj.get_logger()
    message='notify data'+str(data)
    logger.info(message)
    dataObj=ngsi_data_creation(data)
    context=dataObj.get_ngsi_ld()
    logger.info("Data is converted to ngsi-ld")
    obj=patch_post()
    obj.data_convert_invoker(context,dataObj)
    return "notify"
@app.route('/notifyContext1',methods=['POST'])
def notify_server_for_orian():
    logger_obj=Handler()
    logger=logger_obj.get_logger()
    data=request.get_json()
    message='notify data'+str(data)
    logger.info(message)
    dataObj=orian_convert_data(data)
    context=dataObj.get_data()
    logger.info("Data is converted to ngsi-ld")
    obj=patch_post()
    obj.data_convert_invoker(context,dataObj)
    return "notify"
@app.route('/subscribeContext',methods=['POST'])
def rest_client():
    data=request.get_json()
    configobj=config_data()
    fog_url=configobj.get_fogflow_subscription_endpoint()
    url=constant.http+fog_url+constant.subscribe_uri
    payload = json.dumps(data)
    robj=Rest_client(url,payload)
    r=robj.post_request()
    return "subscribe"
if __name__ == '__main__':
    obj=patch_post()
    obj.take_backup()
    app.run(host= '0.0.0.0', port=8888, debug=True)

