import yaml
from parsexml import ActiveMQConfig


class Yaml:

    def __init__(self, filename, xmlfilename):
        with open(filename, 'r') as content_file:
            self.config_yaml = yaml.load(content_file.read())
        print(self.config_yaml)
        self.xmlfilename = xmlfilename

    def config(self, broker_config):
        _config = self.config_yaml["networks"]["common_configuration"]
        if broker_config is not None and broker_config:
            _config = {**_config, **broker_config}
        return _config

    def create(self):
        for key, value in self.config_yaml["networks"]["network_connector"].items():
            activemq = ActiveMQConfig(self.xmlfilename)
            print(key)
            activemq.add_network_connector(
                config=self.config(value["config"] if "config" in value else {}),
                broker_map=self.config_yaml["brokers"],
                broker_name=key,
                broker_data=value["to"]
            )
            activemq.save("/tmp/" + key + ".xml")


