from time import sleep

import pigpio

rx = 5  # change accordingly to your config (BCM value used)


class SensorGPIOReadError(Exception):
    pass


def clear_sensor_if_busy():
    pi = pigpio.pi()
    try:
        pi.bb_serial_read_open(rx, 9600)
        close_sensor(pi)
        return False
    except pigpio.error:
        close_sensor(pi)


def init_sensor():
    pi = pigpio.pi()
    pi.set_mode(rx, pigpio.INPUT)
    pi.bb_serial_read_open(rx, 9600)
    sleep(1)
    return pi


def read_sensor(pi):
    try:
        bytes_read, bytes_array = pi.bb_serial_read(rx)
        assert bytes_array[0] == ord(b'\xaa')
        assert bytes_array[1] == ord(b'\xc0')
        assert bytes_array[9] == ord(b'\xab')
        pm25 = (bytes_array[3] * 256 + bytes_array[2]) / 10.0
        pm10 = (bytes_array[5] * 256 + bytes_array[4]) / 10.0
        checksum = sum(b for b in bytes_array[2:8]) % 256
        assert checksum == bytes_array[8]
        return str(pm10), str(pm25)
    except Exception as e:
        raise SensorGPIOReadError(e)


def close_sensor(pi):
    pi.bb_serial_read_close(rx)
    pi.stop()


def main():
    clear_sensor_if_busy()
    pi = init_sensor()

    try:
        pm10, pm25 = read_sensor(pi)
        values_as_string = "%s|%s" % (pm10, pm25)  # read_sensor(pi)
        return values_as_string
    except SensorGPIOReadError as e:
        print("Skipping because of exception", repr(e))
    except Exception:
        close_sensor(pi)


if __name__ == '__main__':
    main()
