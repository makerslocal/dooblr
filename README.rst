|Logo|

dooblr - The Data Doubler
=========================

|Build Status|

Utility for duplicating data received over MQTT to InfluxDB.

Installation
------------
In the very near future, **dooblr** will be able to be installed via pypi/pip. Until then, or if you want the latest,
bleeding-edge version, you can install it by cloning or downloading the repo and running ``pip install`` inside the
root directory::

    pip install ./

You should then be able to run **dooblr**::

    dooblr
    
Docker
------
**dooblr** has also been conveniently Dockerized!

You will want to mount or copy your configs into the container at the ```/root/.dooblr``` directory.  An example of how Makers Local 256 uses dooblr can be found in the [makerslocal/dooblr-prod](https://github.com/makerslocal/dooblr-prod) repo.

Example:

    docker run -v $(pwd)/config:/root/.dooblr makerslocal/dooblr:latest

Configuration
-------------
**dooblr** is configured using YAML files, and these files are stored in the user's home directory. On Linux-based
systems they'll need to be in a directory like::

    /home/<username>/.dooblr/

On Windows they're loaded from somewhere like::

    C:\Users\<username>\.dooblr\

After the first run of **dooblr**, this directory will be created, and some default configuration files will be there.
**dooblr** requires a main ``dooblr.yml`` that defines MQTT and InfluxDB connections, and one or more measurement
configs.

A default-settings ``dooblr.yml`` config file will look like::

    # dooblr.yaml
    global:
        config-dir: /home/<username>/.dooblr/measurements  # Directory that contains dooblr's measurement configs

    mqtt:
        host: localhost  # Host, domain name, or IP address of the MQTT broker
        port: 1883       # Port number of the MQTT broker

    influxdb:
        host: localhost   # Host, domain name, or IP address of the InfluxDB instance
        port: 8086        # Port number of the InfluxDB instance
        username: root    # Username for the InfluxDB instance
        password: root    # Password for the InfluxDB instance
        database: dooblr  # Database to use in InfluxDB (will be created if it doesn't exist already)

By default, **dooblr** looks for ``*.yml`` measurement configs in the ``.dooblr/measurements/`` directory. Measurement
configs are used to tell **dooblr** which topics and pieces of data need to be pulled from MQTT and pushed to InfluxDB.
**dooblr** expects the MQTT message to contain simple JSON data in its payload.

Let's say you have a device that publishes to the ``home/kitchen/fridge/temperature`` and
``home/kitchen/freezer/temperature`` topics with the data::

    {"temperature": 40.1, "units":"F", "humidity": 0.12, "label": "blue"}

You would probably want to create a measurement config called ``temperature.yml`` that looks like::

    # temperature.yml
    temperature:
        topics:
        - home/kitchen/fridge/temperature
        - home/kitchen/freezer/temperature
        - home/kitchen/+/temperature  # Standard MQTT wildcards also apply here
        fields:
        - temperature
        - humidity
        tags:
        - units
        optional_tags:
        - label  # Maybe not every message on these topics have a "label" property!

Notice that there can be multiple topics, fields, and tags. Tags and fields refer to the tags and fields used in
InfluxDB. Optional tags will not raise an error if they weren't defined in the MQTT message, while regular tags will.

.. |Build Status| image:: https://travis-ci.org/makerslocal/dooblr.svg?branch=master
   :target: https://travis-ci.org/makerslocal/dooblr

.. |Logo| image:: https://github.com/makerslocal/dooblr/blob/master/logo/text_logo.png?raw=true
   :height: 70px
   :alt: dooblr logo

