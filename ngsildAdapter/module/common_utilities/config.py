import ConfigParser
class config_data:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(r'/root/TRANSFORMER/Next_transform/fogflow/ngsildAdapter/module/config/config.ini'))
        logger_obj=Handler()
        self.logger=logger_obj.get_logger()
    def get_entity_url(self):
        self.logger.info("Retriving url of ngsi-ld-broker from config.ini")
        entity_url= self.config.get('My Section', 'ngsi-ld-broker')
        return entity_url
    def get_fogflow_subscription_endpoint(self):
        self.logger.info("Retriving fogflow_subscription_endpoint")
        fogflow_subscription_url=self.config.get('My Section', 'fogflow_subscription_endpoint')
        return fogflow_subscription_url
        
