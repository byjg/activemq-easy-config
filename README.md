# ActiveMQ Easy Config

This project aims a easy way to setup a network of ActiveMQ brokers. You can change easily the topology and this 
script will create the configurations based on your setup. ActiveMQ Easy Config will produce for you:

- An `activemq.xml` file for each broker with the specific configuration for the broker
- A Docker image for each broker to easy adapt in your container orchestrator.
- A script for run the docker image locally in order to test your network locally.
 

# How it works?

Let's take an example of a duplex connection between two ActiveMQ brokers: 

```

   +----------+                    +----------+
   |          |       Duplex       |          |  
   | Broker 1 | ---<-->----<-->--- | Broker 2 |
   |          |                    |          | 
   +----------+                    +----------+

```

First you have to define the `yaml` file with the configuration of your network:

```yaml
brokers:
  node1: "static:(tcp://node1:61616)"
  node2: "static:(tcp://node2:61616)"

networks:
  common_configuration:
    set_broker_name: "false"
    queue:
      conduit_subscriptions: "false"
      consumer_ttl: "1"
      duplex: "true"
      message_ttl: "-1"
      physical_name: ">"
      user_name: "admin"
    topic:
      conduit_subscriptions: "true"
      consumer_ttl: "1"
      duplex: "true"
      message_ttl: "-1"
      physical_name: ">"
      user_name: "admin"

  network_connector:
    node1:
      to:
        - node2
      config:
        queue:
          duplex: "false"
        topic:
          _ignore: "true"
    node2:
      to:
        - node1
``` 

The first topic in the yaml will define the broker and your respective connection. 
If you intend to use docker, the address can be the broker name. 

You can see a lot of examples of network of brokers in the directory `templates`. In the same directory
you have an `activemq.xml` file used as base also.

After create your template you can just run:

```bash
python aec.py \
    --config templates/simple-duplex-config.yaml \
    --activemq templates/activemq.xml \
    --save-to /my/path/project
```

And you'll get the follow files as result:

- node1.xml
- node2.xml

Optionally if you pass a path to a `Dockerfile` and a registry name, the system will create:

- run.sh
- build.sh
- Dockerfile

You can run `build.sh` to build the docker images and `run.sh` to run the containers in your local machine. 

The docker image created can easily adapted to run on Kubernetes, Docker Swarm or ECS.

In the folder `check` you can run a simple producer/consumer to check the communication.

# Installing


## Recommended:

```bash
pip install aec
```

## get from source

Just clone the repository.

```bash
git clone git@github.com:byjg/activemq-easy-config
```  

# To Do

Help here is appreciate :)

- This configuration can be expanded to other features on ActiveMQ.
- K8s implementation
- Docker swarm implementation
- ECS implementation 
