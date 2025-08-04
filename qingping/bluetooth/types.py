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


import attr
import pygatt
import typing


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@attr.s
class DataPacket:
    # Typical packet structure:
    # <length: byte><type: byte><data: bytes?>

    length: int = attr.ib()
    type: int = attr.ib()
    data: bytes | None = attr.ib()

    @staticmethod
    def make(type: int, data: bytes | bytearray | None) -> "DataPacket":
        if isinstance(data, bytearray):
            data = bytes(data)

        if data is None:
            return DataPacket(
                type=type,
                length=1,
                data=None,
            )
        else:
            return DataPacket(
                type=type,
                length=len(data),
                data=data,
            )

    @staticmethod
    def parse_packet(data: bytes | bytearray) -> "DataPacket":
        if isinstance(data, bytearray):
            data = bytes(data)

        packet = DataPacket(
            length=int(data[0]),
            type=int(data[1]),
            data=data[1:],
        )

        return packet

    @staticmethod
    def parse_packets(data: list[bytes | bytearray]) -> list["DataPacket"]:
        return [
            DataPacket.parse_packet(packet)
            for v in packets
        ]

    def make_packet(self) -> bytes:
        if (self.data is not None) and (len(self.data) > 255):
            raise ValueError(f'data len exceeds 255 (actual: { len(data) })')

        if (self.type < 0) or (self.type > 255):
            raise ValueError(f'type exceeds 255 (actual: { self.type })')

        if self.data is None:
            payload = int.to_bytes(1, 1, 'little')
            payload += int.to_bytes(self.type, 1, 'little')
        else:
            payload = int.to_bytes(len(self.data) + 1, 1, 'little')
            payload += int.to_bytes(self.type, 1, 'little')
            payload += self.data

        return payload

    def make_packet_chunks(self) -> typing.Iterable[bytes]:
        return chunks(self.make_packet(), 20)


@attr.s
class Packet:
    handle: int = attr.ib()
    length: bytes = attr.ib()
    data: bytes = attr.ib()


@attr.s
class State:
    device: pygatt.device.BLEDevice = attr.ib()
    messages: dict[str, list] = attr.ib(factory=dict)
    verbose: bool = attr.ib(default=False)

    def make_notification_handler(self, recv_uuid: str):
        def notification_handler(handle, value):
            print(f"[{ handle }] UUID: { recv_uuid }")
            print(f"[{ handle }] raw: { value }")
            print(f"[{ handle }] bytes: { value.hex() }")

            self.messages[recv_uuid] = self.messages.get(recv_uuid, [])
            self.messages[recv_uuid].append(
                Packet(
                    handle=handle,
                    length=int(value[0]),
                    data=bytes(value[1:]),
                ),
            )

        return notification_handler

    def flush(self, recv_uuid: str) -> list[Packet]:
        if recv_uuid not in self.messages:
            return []

        result = list(self.messages[recv_uuid])
        self.messages[recv_uuid].clear()
        return result
