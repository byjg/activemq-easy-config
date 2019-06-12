import xml.dom.minidom


class ActiveMQConfig:

    def __init__(self, filename):
        self.config_dom = xml.dom.minidom.parse(filename)

        brokers = self.config_dom.getElementsByTagName("broker")

        if not brokers or len(brokers) > 1:
            print("Seems to be a wrong ActiveMQ file")
            exit(1)

        self.broker = brokers[0]
        network_connectors = self.broker.getElementsByTagName("networkConnectors")

        if not network_connectors:
            network_connectors = self.config_dom.createElement("networkConnectors")
            self.broker.appendChild(network_connectors)

        self.network_connectors = network_connectors[0]

    def save(self, filename):
        file_handle = open(filename, "w")
        self.config_dom. writexml(file_handle)
        file_handle.close()

    def add_network_connector(self, config, broker_map, broker_name, broker_data):
        if "set_broker_name" not in config or ("set_broker_name" in config and config["set_broker_name"] == "true"):
            self.broker.setAttribute("brokerName", broker_name)

        if broker_data is None:
            broker_data = []

        for broker in broker_data:
            if broker is None:
                continue
            for cname, connector in {"Q": "queue", "T": "topic"}.items():
                common_config = (config[connector] if connector in config else {})

                if "_ignore" in common_config and common_config["_ignore"] == "true":
                    continue

                network_connector = self.config_dom.createElement("networkConnector")
                network_connector.setAttribute("name", cname + "_" + broker_name + "_to_" + broker)
                network_connector.setAttribute("uri", broker_map[broker])

                for attribute, value in common_config.items():
                    network_connector.setAttribute(self.to_camel_case(attribute), value)

                excluded_destinations = self.config_dom.createElement("excludedDestinations")
                destination = self.config_dom.createElement("queue" if connector == "topic" else "topic")
                destination.setAttribute("physicalName", ">")

                excluded_destinations.appendChild(destination)
                network_connector.appendChild(excluded_destinations)
                self.network_connectors.appendChild(network_connector)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return components[0] + ''.join(x.title() for x in components[1:]).replace("Ttl", "TTL")
