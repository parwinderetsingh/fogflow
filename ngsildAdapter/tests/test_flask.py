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
import test
class TestStringMethods(unittest.TestCase):
    def test_orian_end_point(self):
        data1=json.dumps(test.orian_notify_data)
        url='http://192.168.100.133:8888/notifyContext1'
        header={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = requests.post(url,data=data1,headers=header)
        statusCode=response.status_code
        self.assertEqual(statusCode, 200)
    def test_fogflow_end_point(self):
        data1=json.dumps(test.ngsi_data)
        url='http://192.168.100.133:8888/notifyContext'
        header={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = requests.post(url,data=data1,headers=header)
        statusCode=response.status_code
        self.assertEqual(statusCode, 200)
if __name__ == '__main__':
    unittest.main()

