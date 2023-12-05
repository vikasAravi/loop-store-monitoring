import os

import kafka
import json



class KafkaProducerClientManager:
    __connection = None

    def __init__(self):
        self.__connection = kafka.KafkaProducer(bootstrap_servers="localhost:9093",
                                            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                            retries=2)

    @staticmethod
    def get_kafka_producer():
        if KafkaProducerClientManager.__connection is None:
            KafkaProducerClientManager.__connection = KafkaProducerClientManager()
        return KafkaProducerClientManager.__connection

    def send_message(self, topic, key, data):
        self.__connection.send(topic, key=key, value=data)

