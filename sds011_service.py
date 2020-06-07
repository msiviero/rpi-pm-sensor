from networking import serve
from sds011 import clear_sensor_if_busy, init_sensor, read_sensor, SensorGPIOReadError, close_sensor

update_interval = 5


def main():
    clear_sensor_if_busy()
    pi = init_sensor()

    def update_value():
        # noinspection PyBroadException
        try:
            pm10, pm25 = read_sensor(pi)
            values_as_string = "%s|%s" % (pm10, pm25)  # read_sensor(pi)
            return values_as_string
        except SensorGPIOReadError as e:
            print("Skipping because of exception", repr(e))
        except Exception:
            close_sensor(pi)

    serve(update_value, update_interval)


if __name__ == '__main__':
    main()
