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
import typing

import qingping.bluetooth.types


def write_chunks(
    device: pygatt.device.BLEDevice,
    uuid: str,
    chunks: typing.Iterable[bytes],
    verbose: bool = False,
):
    for index, chunk in enumerate(chunks):
        if verbose:
            print(f'send chunk [{ index }] to { uuid }: { chunk.hex() }')
        device.char_write(uuid, chunk, wait_for_response=False)
