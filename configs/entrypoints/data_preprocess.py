# Station Location
## Latitude
STATION_LAT = -33.21744893774415
## Longitude
STATION_LON = -70.77569384951704
## Altitude (m)
STATION_ALT = 503

# MQTT General parameters
MQTT_HOST = "mqtt"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "scorpio_data_preprocess"
# Topics subscribed
MQTT_SUB_TOPIC_1 = "scorpio/extract/sat"
MQTT_SUB_TOPIC_1_QOS = 1
RETAIN = False
# Topics to publish
MQTT_PUB_TOPIC_1 = "scorpio/preprocess/sat"
MQTT_PUB_TOPIC_1_QOS = 1
