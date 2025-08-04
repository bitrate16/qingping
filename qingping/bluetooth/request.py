# qingping - python tools for air monitor
# Copyright (C) 2025  bitrate16 (bitrate16@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import pygatt

import qingping.bluetooth.types
import qingping.bluetooth.utils
import qingping.bluetooth.uuid


def do_request_connect_wifi(
    state: qingping.bluetooth.types.State,
    name: str,
    password: str,
):
    if state.verbose:
        print(f'Connect to WIFI { name !r} with password { password !r}')

    payload = f'"{ name }","{ password }"'
    if state.verbose:
        print(f'payload: { payload !r}')

    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_1,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x01,
            data=payload.encode(),
        ).make_packet_chunks(),
    )


def do_request_scan_wifi(
    state: qingping.bluetooth.types.State,
):
    if state.verbose:
        print(f'Request WIFI scan')

    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_1,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x07,
            data=None,
        ).make_packet_chunks(),
    )


def do_request_scan_wifi_simple(
    state: qingping.bluetooth.types.State,
):
    if state.verbose:
        print(f'Request WIFI scan (simple)')

    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_1,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x04,
            data=None,
        ).make_packet_chunks(),
    )


def do_request_set_link_token(
    state: qingping.bluetooth.types.State,
    link_token: bytes,
):
    if state.verbose:
        print(f'Set link token to { link_token.hex() }')

    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_2,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x01,
            data=link_token,
        ).make_packet_chunks(),
    )
    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_2,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x02,
            data=link_token,
        ).make_packet_chunks(),
    )


def do_request_set_mqtt_connection(
    state: qingping.bluetooth.types.State,
    host: str,
    port: int,
    login: str,
    password: str,
):
    if state.verbose:
        print(f'Set MQTT conenction ({ host = }, { port = }, { login = }, {password = } )')

    payload = f'{ host } { port } { login } { password }'
    if state.verbose:
        print(f'payload: { payload !r}')

    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_2,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x17,
            data=payload.encode(),
        ).make_packet_chunks(),
    )


def do_request_set_mqtt_topics(
    state: qingping.bluetooth.types.State,
    client_id: str,
    topic_read: str,
    topic_write: str,
):
    if state.verbose:
        print(f'Set MQTT topics ({ client_id = }, { topic_read = }, { topic_write = } )')

    payload = f'{ client_id } { topic_read } { topic_write }'
    if state.verbose:
        print(f'payload: { payload !r}')

    qingping.bluetooth.utils.write_chunks(
        verbose=state.verbose,
        device=state.device,
        uuid=qingping.bluetooth.uuid.WRITE_UUID_2,
        chunks=qingping.bluetooth.types.DataPacket.make(
            type=0x18,
            data=payload.encode(),
        ).make_packet_chunks(),
    )
