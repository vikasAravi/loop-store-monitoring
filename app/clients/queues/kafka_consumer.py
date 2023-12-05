import json
import os
from typing import List

import kafka
from kafka import OffsetAndMetadata, TopicPartition


class KafkaConsumerClientManager:
    __connection = None

    def __init__(
            self,
            bootstrap_servers,
            auto_offset_reset,
            group_id,
            enable_auto_commit,
            value_deserializer,
            fetch_min_bytes=1
    ):
        self.__connection = kafka.KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=auto_offset_reset,
            group_id=group_id,
            enable_auto_commit=enable_auto_commit,
            value_deserializer=value_deserializer,
            fetch_min_bytes=fetch_min_bytes
        )

    @staticmethod
    def get_kafka_consumer(bootstrap_servers, auto_offset_reset, group_id, enable_auto_commit, value_deserializer,
                           fetch_min_bytes):
        if KafkaConsumerClientManager.__connection is None:
            KafkaConsumerClientManager.__connection = KafkaConsumerClientManager(bootstrap_servers, auto_offset_reset, group_id,
                                                       enable_auto_commit, value_deserializer, fetch_min_bytes)
        return KafkaConsumerClientManager.__connection

    def subscribe(self, topics: List):
        if self.__connection is None:
            raise Exception("Please initialise your consumer before calling subscribe")
        self.__connection.subscribe(topics=topics)

    def consume_messages(self):
        for message in self.__connection:
            yield message

    def poll(self, timeout_ms, max_records):
        return self.__connection.poll(timeout_ms=timeout_ms, max_records=max_records)

    def commit_async(self, message):
        options = {TopicPartition(message.topic, message.partition): OffsetAndMetadata(message.offset + 1, None)}
        self.__connection.commit_async(options)

    def commit_sync(self, message):
        # options = {TopicPartition(message.topic, message.partition): OffsetAndMetadata(message.offset + 1, None)}
        self.__connection.commit(message.offset)
