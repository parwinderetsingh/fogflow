import sys, os
sys.path.append('/root/TRANSFORMER/Next_transform/fogflow/ngsildAdapter/module')
from common_utilities.rest_client import Rest_client
from common_utilities import rest_client
from data_model.ld_generate  import ngsi_data_creation
from data_model.orian_ld_genrate import orian_convert_data
import json
import unittest
import requests
import mock 
from mock import patch
from consts import constant
from common_utilities.config import config_data
ngsi_data=\
 {
	"originator": "",
	"subscriptionId": "d0c08d50-6296-4ef3-9b0f-ff48b3cd5528",
	"contextResponses": [{
		"contextElement": {
			"attributes": [{
				"contextValue": 34,
				"type": "float",
				"name": "tempo"
			}],
			"entityId": {
				"type": "Tempr",
				"id": "Temprature702"
			},
			"domainMetadata": [{
				"type": "point",
				"name": "location",
				"value": {
					"latitude": 49.406393,
					"longitude": 8.684208
				}
			}]
		},
		"statusCode": {
			"code": 200,
			"reasonPhrase": "OK"
		}
	}]
}
convert_data_output=\
{
	"@context": ["https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.jsonld", {
		"Tempr": "http://example.org/Tempr",
		"tempo": "http://example.org/tempo"
	}],
	"location": {
		"type": "GeoProperty",
		"value": "{\"type\": \"Point\", \"coordinates\": [49.406393, 8.684208]}"
	},
	"tempo": {
		"type": "Property",
		"value": 34
	},
	"id": "urn:ngsi-ld:Temprature702",
	"type": "Tempr"
}
patch_data_output=\
{
	"@context": ["https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.jsonld", {
		"Tempr": "http://example.org/Tempr",
		"tempo": "http://example.org/tempo"
	}],
	"tempo": {
		"type": "Property",
		"value": 34
	},
	"location": {
		"type": "GeoProperty",
		"value": "{\"type\": \"Point\", \"coordinates\": [49.406393, 8.684208]}"
	}
}
orian_notify_data=\
{
	"subscriptionId": "5d09cdeb0016e878cf94e070",
	"data": [{
		"type": "roomie",
		"id": "Room5",
		"temp": {
			"type": "Float",
			"value": 50,
			"metadata": {}
		}
	}]
}

orian_notify_output_data=\
{
	"@context": ["https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.jsonld", {
		"roomie": "http://example.org/roomie",
		"temp": "http://example.org/temp"
	}],
	"type": "roomie",
	"id": "urn:ngsi-ld:Room5",
	"temp": {
		"type": "Float",
		"value": 50
	}
} 
id_value="urn:ngsi-ld:Temprature702"

class TestStringMethods(unittest.TestCase):
    def test_orian_converter(self):
        obj=orian_convert_data(orian_notify_data)
        returndata=obj.get_data()
        self.assertEqual(returndata,orian_notify_output_data)
    def test_get_ngsi_ld(self):
        obj=ngsi_data_creation(ngsi_data)
        result_data=obj.get_ngsi_ld()
        self.assertEqual(result_data,convert_data_output)
    def test_get_entityId(self):
        obj=ngsi_data_creation(ngsi_data)
        entity_id=obj.get_entityId()
        self.assertEqual(entity_id,id_value)
    def test_mock_post(self):
        with patch('common_utilities.rest_client.requests.post') as mock_get:
            mock_get.return_value.status_code = 201
            configobj=config_data()
            entity_url=configobj.get_entity_url()
            url1 =constant.http+entity_url+constant.entity_uri
            payload=convert_data_output
            payload=json.dumps(payload)
            obj=Rest_client(url1,payload)
            response=obj.post_request()
        self.assertEqual(response.status_code, 201)
    def test_mock_patch(self):
        with patch('common_utilities.rest_client.requests.patch') as mock_get:
            mock_get.return_value.status_code = 204
            obj=ngsi_data_creation(ngsi_data)
            entity_id=obj.get_entityId()
            configobj=config_data()
            entity_url=configobj.get_entity_url()
            url=constant.http+entity_url+constant.entity_uri+entity_id+'/attrs'
            payload=patch_data_output
            payload=json.dumps(payload)
            obj=Rest_client(url,payload)
            response=obj.patch_request()
        self.assertEqual(response.status_code, 204)
if __name__ == '__main__':
    unittest.main()


