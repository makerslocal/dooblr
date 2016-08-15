import logging
import config
import mqttclient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting dooblr")
    cfg = config.Config()
    cfg.load("config.ini")

    def callback(message):
        logger.info(message)
    client = mqttclient.MqttClient(callback)
    client.connect("test.mosquitto.org", port=1883)
    for m in cfg.measurements:
        client.register_measurement(m,
                                    topics=cfg.measurements[m]["topics"],
                                    fields=cfg.measurements[m]["fields"],
                                    tags=cfg.measurements[m]["tags"])
    while True:
        client.loop()

if __name__ == "__main__":
    main()
