# Bluetooth protocol

Overview of the bluetooth comminucation protocol.

How to read?
- Operation section: `Request: <description> (<UUID>)`
- Request format sub-section `Request (<type>)`
- Response format sub-section `Response`

## Common

Every packet (almost every) is made of the following structure: `<size: 1B><type: 1B><data: 0+B>`.

Here `size` is single-byte value, `type` is single-byte value and `data` is variable length.

Request is sent chunked in 20 bytes. Responses are sent in separate packets.

## Request: Scan WIFI (detailed) (0x000D)

Request detailed WIFI scan.

### Request (0x07)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000D,
    message: 0x 01 07
)
```

### Response

```
notification(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000E,
)
```

#### Structure

Response is made of chunks:
```
<size><type = 0x07><chunk>
```

To get actual result, concatenate chunks. Result is tab-separated string, example:
```
"Home Wifi",3,-44\t"Guests",3,-44\t"Hotspot",3,-44
```

Data can be interpreted as following:
- `"Home Wifi"` - network name
- `3` - channel
- `-44` - rssi

## Request: Scan WIFI (simple) (0x000D)

Request simple WIFI scan.

### Request (0x04)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000D,
    message: 0x 01 04
)
```

### Response

```
notification(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000E,
)
```

#### Structure

Response is made of chunks:
```
<size><type = 0x04><chunk>
```

To get actual result, concatenate chunks. Result is comma-separated string, example:
```
"Home Wifi","Guests","Hotspot"
```

Data can be interpreted as following:
- `"Home Wifi"` - network name

## Request: Get bluetooth MAC (0x000D)

Request bluetooth MAC.

### Request (0x08)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000D,
    message: 0x 01 08
)
```

### Response

```
notification(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000E,
)
```

#### Structure

Response is made of chunks:
```
<size><type = 0x08><mac bytes>
```

mac bytes are little-endian order (raw bytes, not string):
```
AB8967452301
```

Equals to mac address `01:23:45:67:89:AB`

## Request: Get WIFI MAC (0x0017)

Request WIFI MAC.

### Request (0x0B)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0017,
    message: 0x 01 0B
)
```

### Response

```
notification(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0018,
)
```

#### Structure

Response is made of chunks:
```
<size><type = 0x0B><mac bytes>
```

mac bytes are big-endian order (raw bytes, not string):
```
0123456789AB
```

Equals to mac address `01:23:45:67:89:AB`

## Request: Get Bluetooth MAC (0x0017)

Request bluetooth MAC.

### Request (0x0C)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0017,
    message: 0x 01 0C
)
```

### Response

```
notification(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0018,
)
```

#### Structure

Response is made of chunks:
```
<size><type = 0x0C><mac bytes>
```

mac bytes are big-endian order (raw bytes, not string):
```
0123456789AB
```

Equals to mac address `01:23:45:67:89:AB`

## Request: Normal display (0x0017)

Request enable display.

### Request (0x02)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0017,
    message: 0x 01 02
)
```

### Note

The purpose of this code is unknown and has beed discovered during random poking into UUID.

## Request: Black display (0x0017)

Request disable display.

### Note

The purpose of this code is unknown and has beed discovered during random poking into UUID.

### Request (0x03)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0017,
    message: 0x 01 03
)
```

## Request: Set link token (0x0001)

Write account link token.

### Note

Token is acquired from account and possible used to authenticate/sign MQTT connection requests.

Token is 16 bytes. Example: `0123456789ABCDEF0123456789ABCDEF`.

### Request (0x01 + 0x02)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0001,
    message: 0x 11 01 0123456789ABCDEF0123456789ABCDEF
)

write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0001,
    message: 0x 11 02 0123456789ABCDEF0123456789ABCDEF
)
```

## Request: Connect to WIFI (0x000D)

Write WIFI connection info.

### Note

Write WIFI configuration to device.

WIFI configuration is formatted as `"network_name","network_password"`

### Request (0x01)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000D,
    message: 0x 21 01 226e6574776f726b5f6e616d65222c226e6574776f726b5f70617373776f726422
)
```

## Request: Send what? (0x000D)

### Note

Unknown characteristic, sometimes written during setup. Length is 18 bytes.

### Request (0x06)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x000D,
    message: 0x 13 06 0123456789ABCDEF0123456789ABCDEF0123
)
```

## Request: Set MQTT configuration (0x0001)

Write MQTT config.

### Note

Payload is fomatted as space-separated string. Example:
```
"<host> <port> <login> <password>"
```

Example from real-world setup:
```
"mqtt.bj.cleargrass.com 11883 <WIFI_MAC_ADDRESS>&<LOGIN> <VERY_LONG_HEX_PASSWORD>"
```

### Request (0x17)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0001,
    message: 0x 38 17 6d7174742e626a2e636c65617267726173732e636f6d20313138383320303132333435363738394142266c6f67696e2070617373776f7264
)
```

## Request: Set MQTT tpics (0x0001)

Write MQTT topics.

### Note

Payload is fomatted as space-separated string. Example:
```
"<client_id> <read_topic> <write_topic>"
```

Example from real-world setup:
```
"<WIFI_MAC_ADDRESS>|securemode=3,signmethod=hmacsha256,prefix=,random=<SERVER_ID>| /<LOGIN>/<WIFI_MAC_ADDRESS>/user/get /<LOGIN>/<WIFI_MAC_ADDRESS>/user/update"
```

Example `SERVER_ID`: `server464`.

### Request (0x18)

```
write(
    service: 22210000-554a-4546-5542-46534450464d,
    uuid: 0x0001,
    message: 0x 86 18 3031323334353637383941427c7365637572656d6f64653d332c7369676e6d6574686f643d686d61637368613235362c7072656669783d2c72616e646f6d3d7365727665723436347c202f6c6f67696e2f3031323334353637383941422f757365722f676574202f6c6f67696e2f3031323334353637383941422f757365722f757064617465
)
```
