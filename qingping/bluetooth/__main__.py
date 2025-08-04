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


import argparse
import pygatt
import atexit
import time

import qingping.bluetooth.types
import qingping.bluetooth.request


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        'qingping',
        description='qingping bluetooth configuration tool',
    )

    parser.add_argument(
        '--verbose',
        help='Verbose logging',
        action='store_true',
    )

    parser.add_argument(
        '--mac',
        help='Device MAC address',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--link-token',
        help='Link token (must be bytes of length 16)',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--wifi-ssid',
        help='WIFI network name',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--wifi-password',
        help='WIFI network password',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--mqtt-host',
        help='MQTT host',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--mqtt-port',
        help='MQTT port',
        type=int,
        required=True,
    )

    parser.add_argument(
        '--mqtt-login',
        help='MQTT login',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--mqtt-password',
        help='MQTT password',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--mqtt-client',
        help='MQTT client id',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--mqtt-read',
        help='MQTT read topic',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--mqtt-write',
        help='MQTT write topic',
        type=str,
        required=True,
    )

    return parser.parse_args()


def main():
    args = get_args()

    # Validate link token
    try:
        link_token = bytes.fromhex(args.link_token)
        if len(link_token) != 16:
            print(f'Invalid link token length: { len(link_token) } != 16')
            exit(1)

    except:
        print(f'Invalid link token value: { args.link_token }')
        exit(1)

    # Adapter
    adapter = pygatt.GATTToolBackend()
    adapter.start(
        reset_on_start=False,
    )

    # Connect
    device = adapter.connect(args.mac)
    atexit.register(device.disconnect)

    state = qingping.bluetooth.types.State(
        device=device,
        verbose=args.verbose,
    )

    # Write WIFI config
    time.sleep(1)
    qingping.bluetooth.request.do_request_connect_wifi(
        state=state,
        name=args.wifi_ssid,
        password=args.wifi_password,
    )

    # Write link token
    time.sleep(1)
    qingping.bluetooth.request.do_request_set_link_token(
        state=state,
        link_token=link_token,
    )

    # Write MQTT config
    time.sleep(1)
    qingping.bluetooth.request.do_request_set_mqtt_connection(
        state=state,
        host=args.mqtt_host,
        port=args.mqtt_port,
        login=args.mqtt_login,
        password=args.mqtt_password,
    )

    # Write MQTT topics
    time.sleep(1)
    qingping.bluetooth.request.do_request_set_mqtt_topics(
        state=state,
        client_id=args.mqtt_client,
        topic_read=args.mqtt_read,
        topic_write=args.mqtt_write,
    )


if __name__ == '__main__':
    main()
