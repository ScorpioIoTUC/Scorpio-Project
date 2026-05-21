# MQTT General parameters
MQTT_HOST = "mqtt"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "scorpio_data_storage"
## Publish packets stored in the db to scorpio server every 15 seconds.
PUBLISH_INTERVAL = 15 # s
# Topics subscribed
TOPIC_PREPROCESS = "scorpio/preprocess/sat"
TOPIC_PREPROCESS_QOS = 1
TOPIC_UPLOADED = "scorpio/uploaded/sat"
TOPIC_UPLOADED_QOS = 1
# Topics to publish
TOPIC_SEND = "scorpio/send/sat"
TOPIC_SEND_QOS = 0
# Sqlite parameters
SQLITE_DB_PATH = "/data/sat_data.db"
