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
import pytest
from octobot_channels.channels.channel import del_chan, get_chan

from octobot_evaluators.api.evaluators import create_matrix
from octobot_evaluators.api.initialization import create_matrix_channels
from octobot_evaluators.channels import MATRIX_CHANNEL
from octobot_evaluators.data.matrix import get_tentacle_path
from octobot_evaluators.matrices.matrices import Matrices


async def matrix_callback(matrix_id,
                          evaluator_name,
                          evaluator_type,
                          eval_note,
                          eval_note_type,
                          exchange_name,
                          cryptocurrency,
                          symbol,
                          time_frame):
    pass


@pytest.mark.asyncio
async def test_evaluator_channel_creation():
    del_chan(MATRIX_CHANNEL)
    await create_matrix_channels()
    await get_chan(MATRIX_CHANNEL).new_consumer(matrix_callback)
    await get_chan(MATRIX_CHANNEL).stop()


@pytest.mark.asyncio
async def test_evaluator_channel_send():
    del_chan(MATRIX_CHANNEL)
    matrix_id = create_matrix()
    await create_matrix_channels()
    await get_chan(MATRIX_CHANNEL).new_consumer(matrix_callback)
    await get_chan(MATRIX_CHANNEL).get_internal_producer().send(matrix_id=matrix_id,
                                                                evaluator_name="test",
                                                                evaluator_type="test2",
                                                                eval_note=1)

    # following assert should be None because send() doesn't call set_tentacle_value
    assert Matrices.instance().get_matrix(matrix_id).get_node_at_path(
        get_tentacle_path(tentacle_name="test", tentacle_type="test2")) is None
    await get_chan(MATRIX_CHANNEL).stop()
    Matrices.instance().del_matrix(matrix_id)


@pytest.mark.asyncio
async def test_evaluator_channel_send_eval_note():
    del_chan(MATRIX_CHANNEL)
    matrix_id = create_matrix()
    await create_matrix_channels()
    await get_chan(MATRIX_CHANNEL).new_consumer(matrix_callback)
    await get_chan(MATRIX_CHANNEL).get_internal_producer().send_eval_note(matrix_id=matrix_id,
                                                                          evaluator_name="test",
                                                                          evaluator_type="test2",
                                                                          eval_note=1,
                                                                          eval_note_type=int)

    assert Matrices.instance().get_matrix(matrix_id).get_node_at_path(
        get_tentacle_path(tentacle_name="test", tentacle_type="test2")).node_value == 1
    await get_chan(MATRIX_CHANNEL).stop()
    Matrices.instance().del_matrix(matrix_id)
