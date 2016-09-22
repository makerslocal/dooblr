import logging
import os
from dooblr import config, mqttclient, influxdbclient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting dooblr")
    main_cfg = config.MainConfig()
    default_cfg_path = os.path.join(os.path.expanduser("~"), ".dooblr")
    default_cfg_file = os.path.join(default_cfg_path, "dooblr.yml")
    if not os.path.isdir(default_cfg_path):
        logger.warning("Config directory not found, creating: {dir}".format(dir=default_cfg_path))
        os.makedirs(default_cfg_path)
        measurement_cfg_path = os.path.join(default_cfg_path, "measurements")
        os.makedirs(measurement_cfg_path)
        config.MeasurementConfig.save_default_config(os.path.join(measurement_cfg_path, "sample.yml"))

    if not os.path.isfile(default_cfg_file):
        logger.warning(("Main config not found, creating: {config}".format(config=default_cfg_file)))
        config.MainConfig.save_default_config(default_cfg_file)

    try:
        main_cfg.load(default_cfg_file)
    except IOError as e:
        logger.error("Can't open config file {file}: {reason}".format(file=default_cfg_file, reason=e))
        raise

    measurement_cfg = config.MeasurementConfig()
    for (dirpath, _, filenames) in os.walk(main_cfg.config_dir):
        filenames = [fi for fi in filenames if fi.endswith(".yml")]
        for filename in filenames:
            logger.info("Loading measurements from {file}".format(file=os.path.join(dirpath, filename)))
            measurement_cfg.load(os.path.join(dirpath, filename))

    influx = influxdbclient.InfluxDBClient(
        host=main_cfg.influx_host,
        port=main_cfg.influx_port,
        username=main_cfg.influx_username,
        password=main_cfg.influx_password,
        database=main_cfg.influx_database
    )

    def callback(message):
        logger.info(message)
        influx.write(message)

    client = mqttclient.MqttClient(callback)
    logger.info("Connecting to MQTT broker: {host}:{port}".format(host=main_cfg.mqtt_host, port=main_cfg.mqtt_port))
    client.connect(main_cfg.mqtt_host, port=main_cfg.mqtt_port)

    print(measurement_cfg.measurements)
    for m in measurement_cfg.measurements:
        client.register_measurement(m,
                                    topics=measurement_cfg.measurements[m]["topics"],
                                    fields=measurement_cfg.measurements[m]["fields"],
                                    tags=measurement_cfg.measurements[m]["tags"])

    while True:
        client.loop()

if __name__ == "__main__":
    main()
