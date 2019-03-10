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
        self.broker.setAttribute("brokerName", broker_name)

        if broker_data is None:
            broker_data = []

        for broker in broker_data:
            if broker is None:
                continue
            for cname, connector in {"Q": "queue", "T": "topic"}.items():
                network_connector = self.config_dom.createElement("networkConnector")
                network_connector.setAttribute("conduitSubscriptions", config["conduit_subscriptions"])
                network_connector.setAttribute("consumerTTL", config["consumer_ttl"])
                network_connector.setAttribute("duplex", config["duplex"])
                network_connector.setAttribute("messageTTL", config["message_ttl"])
                network_connector.setAttribute("name", cname + ":" + broker_name + "--" + broker)
                network_connector.setAttribute("uri", broker_map[broker])
                network_connector.setAttribute("userName", config["user_name"])

                excluded_destinations = self.config_dom.createElement("excludedDestinations")
                destination = self.config_dom.createElement("queue" if connector == "topic" else "topic")
                destination.setAttribute("physicalName", ">")

                excluded_destinations.appendChild(destination)
                network_connector.appendChild(excluded_destinations)
                self.network_connectors.appendChild(network_connector)
