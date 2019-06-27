from orian_ld_genrate import orian_convert_data
data={u'subscriptionId': u'5d0754540016e878cf94e06c', u'data': [{u'tempo': {u'type': u'Float', u'value': 60, u'metadata': {}}, u'type': u'Room', u'id': u'Room1', u'temperature': {u'type': u'Float', u'value': 50, u'metadata': {}}}]}
obj=orian_convert_data(data)
data1=obj.get_data()
print(data1)

