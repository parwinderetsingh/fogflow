from flask import Flask, abort, request
import sys,os
sys.path.append('/root/TRANSFORMER/Next_transform/fogflow/ngsildAdapter/module')
import json
import pickle
import datetime
import io
import requests
from consts import constant
from LogerHandler import Handler
import logging
class Rest_client:
    def __init__(self,url,payload):
        self.url=url
        self.payload=payload
        self.headers=constant.header
    def post_request(self):
        print("neeraj")
        print(self.payload)
        logger_obj=Handler()
        logger=logger_obj.get_logger()
        response = requests.post(self.url, data=self.payload, headers=self.headers)
        if response.ok: 
            logger.info("Reesponse is ok")
            return response
        else:
            logger.info("Reesponse is None Entity may already exits")
            return None 
    def patch_request(self):
        logger_obj=Handler()
        logger=logger_obj.get_logger()
        response = requests.post(self.url, data=self.payload, headers=self.headers)
        print("neeraj srivastav")
        response = requests.patch(self.url, data=self.payload, headers=self.headers)
        if response.ok:
           logger.info("Response is ok")
           return response
        else:
            logger.info("Response is None Entity there may some problem in entity")
            return None
            
         
