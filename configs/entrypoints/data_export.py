from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("SCORPIO_API_URL", "")
CREDENTIALS = {"bearer_token": os.getenv("SCORPIO_STATION_KEY", "")}
# MQTT General parameters
MQTT_HOST = "mqtt"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "scorpio_data_export"
# Topics subscribed
TOPIC_SEND = "scorpio/send/sat"
TOPIC_SEND_QOS = 1
# Topics to publish
TOPIC_UPLOADED = "scorpio/uploaded/sat"
TOPIC_UPLOADED_QOS = 1

# Send pending configuration
## Number of ids to send in each batch to uplaoded topic.
BUFFER_SIZE = 10
MAX_TIME_GAP = 60  # seconds
