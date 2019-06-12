import yaml
from parsexml import ActiveMQConfig


class Yaml:

    def __init__(self, filename, xmlfilename):
        with open(filename, 'r') as content_file:
            self.config_yaml = yaml.load(content_file.read())
        # print(self.config_yaml)
        self.xmlfilename = xmlfilename

    def config(self, broker_config):
        _config = self.config_yaml["networks"]["common_configuration"]
        if broker_config is not None and broker_config:
            _config["queue"] = {**_config["queue"], **broker_config["queue"]}
            _config["topic"] = {**_config["topic"], **broker_config["topic"]}
        return _config

    def create(self, path, docker_prefix):
        script = ["#!/bin/bash", ""]
        script2 = ["#!/bin/bash", "", "docker network create activemq", ""]
        admin_port = 8161
        jsm_port = 61616
        for key, value in self.config_yaml["networks"]["network_connector"].items():
            activemq = ActiveMQConfig(self.xmlfilename)
            print(key)
            activemq.add_network_connector(
                config=self.config(value["config"] if "config" in value else {}),
                broker_map=self.config_yaml["brokers"],
                broker_name=key,
                broker_data=value["to"]
            )
            activemq.save(path + "/" + key + ".xml")
            script.append(f"docker build -t {docker_prefix}/{key} --build-arg ACTIVEMQ_CONFIG={key}.xml -f Dockerfile .")
            script2.append(f"docker run --network activemq --name {key} -p {admin_port}:8161 -p {jsm_port}:61616 --rm -d {docker_prefix}/{key}")
            admin_port += 1
            jsm_port += 1

        return [script, script2]
