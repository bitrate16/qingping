# qingping client library

Tool for configuring your Qingping Air Monitor Lite without internet or app.

# WARNING

**Carefully check your device model before use. Author is not responsible for possible damage or device bricking.**

In practive device can not be killed by bluetooth packets, but incompatibilities between firmware and/or hardware may cause fatal damage when operating on unknown opcodes. You must understand and accept the risks before using this utility.

# How to use

Install with

```bash
pip install qingping
```

If you want to connect your device to your MQTT server, put it into pairing mode and do

```bash
python3 -m qingping.bluetooth \
    --verbose \
    --mac MAC__ADDRESS__HERE \
    --wifi-ssid "WIFI__SSID__HERE" \
    --wifi-password "WIFI__PASSWORD__HERE" \
    --link-token "00112233445566778899AABBCCDDEEFF" \
    --mqtt-host "MQTT__HOST__HERE" \
    --mqtt-port 1883 \
    --mqtt-login qingping \
    --mqtt-password qingping \
    --mqtt-client "MQTT__CLIENT__HERE" \
    --mqtt-read "MQTT__TOPIC__READ__HERE" \
    --mqtt-write "MQTT__TOPIC__WRITE__HERE"
```

Optionally change `mqtt-login`, `mqtt-pasword` and `link-token`.

# Supported devices

Currently supported devices:
- Qingping Air Monitor Lite (CGDN1)

# Features

* Full offline device setup
* Support of all (known) bluetooth commands with docs and examples
* Support of all (known) MQTT configuration commands with docs and examples
* Library and a standalone script

# Bluetooth

See [bluetooth.md](bluetooth.md)

# Pipeline

Connection pipeline described [pipeline.md](pipeline.md)

# TODO:

- Discover other packet types
- Documentation for MQTT commands
- Support cli configuration over MQTT

# License

```
qingping - python tools for air monitor
Copyright (C) 2025  bitrate16 (bitrate16@gmail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
