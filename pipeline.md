# Connection pipeline

By default app uses the following pipeline:
- Connect
- Set link token
- Scan WIFI (0x000D + 07)
- Conenct to WIFI
- Set MQTT config

Then device automatically starts sending data to MQTT queue.

# Activator script

Activator script works as following:
- Connect
- Set pre-defined link token
- Set WIFI
- Set MQTT config
