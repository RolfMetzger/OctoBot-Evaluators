# cython: language_level=3
#  Drakkar-Software OctoBot-Evaluators
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
from asyncio import CancelledError

from octobot_channels import CHANNEL_WILDCARD
from octobot_channels.channels.channel import Channel
from octobot_channels.consumer import Consumer
from octobot_channels.producer import Producer
from octobot_commons.logging.logging_util import get_logger
from octobot_evaluators.constants import EVALUATOR_EVAL_DEFAULT_TYPE
from octobot_evaluators.data.matrix import get_tentacle_path, get_tentacle_value_path, Matrix
from octobot_evaluators.matrices.matrices import Matrices

MATRIX_CHANNELS = "MatrixChannels"


class MatrixChannelConsumer(Consumer):
    async def consume(self):
        while not self.should_stop:
            try:
                await self.callback(**(await self.queue.get()))
            except CancelledError:
                self.logger.warning("Cancelled task")
            except Exception as e:
                self.logger.exception(e, True, f"Exception when calling callback : {e}")


class MatrixChannelProducer(Producer):
    async def send(self,
                   matrix_id,
                   evaluator_name,
                   evaluator_type,
                   eval_note,
                   eval_note_type=EVALUATOR_EVAL_DEFAULT_TYPE,
                   exchange_name=None,
                   cryptocurrency=CHANNEL_WILDCARD,
                   symbol=CHANNEL_WILDCARD,
                   time_frame=None):
        for consumer in self.channel.get_filtered_consumers(matrix_id=matrix_id,
                                                            cryptocurrency=cryptocurrency,
                                                            symbol=symbol,
                                                            time_frame=time_frame,
                                                            evaluator_type=evaluator_type,
                                                            evaluator_name=evaluator_name,
                                                            exchange_name=exchange_name):
            await consumer.queue.put({
                "matrix_id": matrix_id,
                "evaluator_name": evaluator_name,
                "evaluator_type": evaluator_type,
                "eval_note": eval_note,
                "eval_note_type": eval_note_type,
                "exchange_name": exchange_name,
                "cryptocurrency": cryptocurrency,
                "symbol": symbol,
                "time_frame": time_frame
            })

    async def send_eval_note(self,
                             matrix_id: str,
                             evaluator_name: str,
                             evaluator_type,
                             eval_note,
                             eval_note_type,
                             exchange_name: str = None,
                             cryptocurrency: str = None,
                             symbol: str = None,
                             time_frame=None):
        Matrices.instance().get_matrix(matrix_id).set_tentacle_value(
            value_type=eval_note_type,
            value=eval_note,
            value_path=get_tentacle_path(exchange_name=exchange_name,
                                         tentacle_type=evaluator_type,
                                         tentacle_name=evaluator_name) + get_tentacle_value_path(
                cryptocurrency=cryptocurrency,
                symbol=symbol,
                time_frame=time_frame)
        )

        await self.send(matrix_id=matrix_id,
                        evaluator_name=evaluator_name,
                        evaluator_type=evaluator_type,
                        eval_note=eval_note,
                        eval_note_type=eval_note_type,
                        exchange_name=exchange_name,
                        cryptocurrency=cryptocurrency,
                        symbol=symbol,
                        time_frame=time_frame)


class MatrixChannel(Channel):
    FILTER_SIZE = 1
    PRODUCER_CLASS = MatrixChannelProducer
    CONSUMER_CLASS = MatrixChannelConsumer

    MATRIX_ID_KEY = "matrix_id"
    CRYPTOCURRENCY_KEY = "cryptocurrency"
    SYMBOL_KEY = "symbol"
    TIME_FRAME_KEY = "time_frame"
    EVALUATOR_TYPE_KEY = "evaluator_type"
    EXCHANGE_NAME_KEY = "exchange_name"
    EVALUATOR_NAME_KEY = "evaluator_name"

    def __init__(self):
        super().__init__()
        self.logger = get_logger(f"{self.__class__.__name__}")

    async def new_consumer(self,
                           callback: object,
                           size=0,
                           matrix_id=CHANNEL_WILDCARD,
                           cryptocurrency=CHANNEL_WILDCARD,
                           symbol=CHANNEL_WILDCARD,
                           evaluator_name=CHANNEL_WILDCARD,
                           evaluator_type=CHANNEL_WILDCARD,
                           exchange_name=CHANNEL_WILDCARD,
                           time_frame=CHANNEL_WILDCARD):
        consumer = MatrixChannelConsumer(callback, size=size)
        await self._add_new_consumer_and_run(consumer,
                                             matrix_id=matrix_id,
                                             cryptocurrency=cryptocurrency,
                                             symbol=symbol,
                                             evaluator_name=evaluator_name,
                                             evaluator_type=evaluator_type,
                                             exchange_name=exchange_name,
                                             time_frame=time_frame)
        return consumer

    def get_filtered_consumers(self,
                               matrix_id=CHANNEL_WILDCARD,
                               cryptocurrency=CHANNEL_WILDCARD,
                               symbol=CHANNEL_WILDCARD,
                               evaluator_type=CHANNEL_WILDCARD,
                               time_frame=CHANNEL_WILDCARD,
                               evaluator_name=CHANNEL_WILDCARD,
                               exchange_name=CHANNEL_WILDCARD):
        return self.get_consumer_from_filters({
            self.MATRIX_ID_KEY: matrix_id,
            self.CRYPTOCURRENCY_KEY: cryptocurrency,
            self.SYMBOL_KEY: symbol,
            self.TIME_FRAME_KEY: time_frame,
            self.EVALUATOR_TYPE_KEY: evaluator_type,
            self.EVALUATOR_NAME_KEY: evaluator_name,
            self.EXCHANGE_NAME_KEY: exchange_name
        })

    async def _add_new_consumer_and_run(self, consumer,
                                        matrix_id=CHANNEL_WILDCARD,
                                        cryptocurrency=CHANNEL_WILDCARD,
                                        symbol=CHANNEL_WILDCARD,
                                        evaluator_name=CHANNEL_WILDCARD,
                                        evaluator_type=CHANNEL_WILDCARD,
                                        exchange_name=CHANNEL_WILDCARD,
                                        time_frame=None):
        consumer_filters: dict = {
            self.MATRIX_ID_KEY: matrix_id,
            self.CRYPTOCURRENCY_KEY: cryptocurrency,
            self.SYMBOL_KEY: symbol,
            self.TIME_FRAME_KEY: time_frame,
            self.EVALUATOR_NAME_KEY: evaluator_name,
            self.EXCHANGE_NAME_KEY: exchange_name,
            self.EVALUATOR_TYPE_KEY: evaluator_type
        }

        self.add_new_consumer(consumer, consumer_filters)
        await consumer.run()
        self.logger.debug(f"Consumer started for : "
                          f"[matrix_id={matrix_id},"
                          f" cryptocurrency={cryptocurrency},"
                          f" symbol={symbol},"
                          f" time_frame={time_frame},"
                          f" evaluator_name={evaluator_name},"
                          f" exchange_name={exchange_name},"
                          f" evaluator_type={evaluator_type}]")
