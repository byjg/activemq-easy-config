FROM openjdk:8-jre-alpine

ARG ACTIVEMQ_VERSION=5.15.6
ARG ACTIVEMQ_CONFIG

WORKDIR /opt/activemq

RUN wget http://archive.apache.org/dist/activemq/$ACTIVEMQ_VERSION/apache-activemq-$ACTIVEMQ_VERSION-bin.tar.gz -O- \
  | tar -xz -C /opt/activemq --strip-components=1

COPY $ACTIVEMQ_CONFIG /opt/activemq/conf/activemq.xml

CMD ["/opt/activemq/bin/activemq", "console"]
