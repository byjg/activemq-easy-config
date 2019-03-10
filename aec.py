import argparse
from parseyml import Yaml


parser = argparse.ArgumentParser(description='ActiveMQ Easy Config (AEC) v1.0')
parser.add_argument('-c', '--config', help='Configuration file in yaml', required=True)
parser.add_argument('-x', '--xml', help='ActiveMQ Configuration file', required=True)

args = parser.parse_args()

y = Yaml(args.config, args.xml)

y.create()


# print(config_dom.toprettyxml(indent="  "))
