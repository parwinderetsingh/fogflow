import pickle
import os,sys
sys.path.append('/root/TRANSFORMER/Next_transform/fogflow/ngsildAdapter/module')
import datetime
import io
import requests
import sys
import json
from consts import constant
from common_utilities.LogerHandler import Handler
class ngsi_data_creation:
    def __init__(self,data):
        self.data=data 
        self.context={}
    def get_ngsi_ld(self):
        logger_obj=Handler()
        logger=logger_obj.get_logger()
        logger.info("Start converting ngsiv1 data to NGSI-LD")
        data=self.data
        data2=data['contextResponses'][0]
        data3=data2['contextElement']
        meta_data=data3['domainMetadata'][0]
        entity_data=data3['entityId']
        entity_data_type=entity_data['type']
        entity_data_id=entity_data['id']
        relations=[]
        relation_url={}
        relations.append(constant.context_url)
        relation_url[entity_data_type]=constant.brand_url+entity_data_type
        attribute_data=data3['attributes']
        length=len(attribute_data)
        for i in range(length):
            attribute_data=data3['attributes'][i]
            attribute_data_contextvalue=attribute_data['contextValue']
            attribute_data_type=attribute_data['type']
            attribute_data_name=attribute_data['name']
            relation_url[attribute_data_name]=constant.brand_url+attribute_data_name
        relations.append(relation_url)
        self.context['@context']=relations
        attribute_data=data3['attributes'][0]
        for i in range(length):
            attribute_data=data3['attributes'][i]
            attribute_name=attribute_data['name']
            brand_type={}
            brand_type['type']="Property"
            brand_type['value']=attribute_data['contextValue']
            self.context[attribute_name]=brand_type
        self.context['id']=constant.id_value+entity_data_id
        self.context['type']=entity_data_type
        coordinate=meta_data['value']
        coordinate_data=[]
        coordinate_data.append(coordinate['latitude'])
        coordinate_data.append(coordinate['longitude'])
	d={}
        logger.info("Start converting metadata of ngsiv1 to ngsi-ld metadata")
        meta_data_type=meta_data['type']
	d["type"]="Point"
	d["coordinates"]=coordinate_data
	d2=json.dumps(d)
        location={}
        location['type']="GeoProperty"
        location['value']=d2
        self.context['location']=location
        logger.info("Data has been converted to NGSI-LD")
        return self.context
    def get_entityId(self):
        logger_obj=Handler()
        logger=logger_obj.get_logger()
        logger.info("Creating Entity")
        data=self.data
        data2=data['contextResponses'][0]
        data3=data2['contextElement']
        entity_data=data3['entityId']
        entity_data_id=entity_data['id']
        self.entity_id=constant.id_value+entity_data_id
        logger.info("Entity has been created")
        return self.entity_id
