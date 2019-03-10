import argparse
import os
from parseyml import Yaml


parser = argparse.ArgumentParser(description='ActiveMQ Easy Config (AEC) v1.0')
parser.add_argument('-c', '--config', help='Configuration file in yaml', required=True)
parser.add_argument('-x', '--xml', help='ActiveMQ Configuration file', required=True)
parser.add_argument('-s', '--save-to', help='Save the files to the specified folder (defaults to current directory)',
                    required=False, default=os.getcwd())
parser.add_argument('-d', '--use-dockerfile', help='Generate the docker file for build ', required=False,
                    action="store_true")

args = parser.parse_args()

y = Yaml(args.config, args.xml)

os.makedirs(args.save_to, exist_ok=True)

y.create(args.save_to)


# print(config_dom.toprettyxml(indent="  "))
