import argparse
import os
from parseyml import Yaml


parser = argparse.ArgumentParser(description='ActiveMQ Easy Config (AEC) v1.0')
parser.add_argument('-c', '--config', help='Configuration file in yaml', required=True)
parser.add_argument('-x', '--xml', help='ActiveMQ Configuration file', required=True)
parser.add_argument('-s', '--save-to', help='Save the files to the specified folder (defaults to current directory)',
                    required=False, default=os.getcwd())
parser.add_argument('-d', '--docker', help='The name of the registry and the folder. e.g. docker.io/byjg',
                    required=False, default="example")

args = parser.parse_args()

y = Yaml(args.config, args.xml)

os.makedirs(args.save_to, exist_ok=True)

[script, script2] = y.create(args.save_to, args.docker)

handler = open(f"{args.save_to}/build.sh", "w")
handler.write("\n".join(script))
handler.close()

handler = open(f"{args.save_to}/run.sh", "w")
handler.write("\n".join(script2))
handler.close()


# print(config_dom.toprettyxml(indent="  "))
