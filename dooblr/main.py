import logging
import config
import mqttclient
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting dooblr")
    main_cfg = config.MainConfig()
    default_cfg_path = os.path.join(os.path.expanduser("~"), ".dooblr")
    default_cfg_file = os.path.join(default_cfg_path, "dooblr.ini")
    if not os.path.isdir(default_cfg_path):
        os.makedirs(default_cfg_path)
        os.makedirs(os.path.join(default_cfg_path, "measurements"))

    try:
        main_cfg.load(default_cfg_file)
    except IOError as e:
        logger.error("Can't open config file {file}: {reason}".format(file=default_cfg_file, reason=e))
        raise

    def callback(message):
        logger.info(message)

    client = mqttclient.MqttClient(callback)
    logger.info("Connecting to MQTT broker: {host}:{port}".format(host=main_cfg.mqtt_host, port=main_cfg.mqtt_port))
    client.connect(main_cfg.mqtt_host, port=main_cfg.mqtt_port)

    measurement_cfg = config.MeasurementConfig()
    for (dirpath, _, filenames) in os.walk(main_cfg.config_dir):
        for filename in filenames:
            logger.info("Loading measurements from {file}".format(file=os.path.join(dirpath, filename)))
            measurement_cfg.load(os.path.join(dirpath, filename))

    for m in measurement_cfg.measurements:
        client.register_measurement(m,
                                    topics=measurement_cfg.measurements[m]["topics"],
                                    fields=measurement_cfg.measurements[m]["fields"],
                                    tags=measurement_cfg.measurements[m]["tags"])
    while True:
        client.loop()

if __name__ == "__main__":
    main()
