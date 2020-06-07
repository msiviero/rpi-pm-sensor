from time import sleep, strftime

import serial

DEVICE = "/dev/ttyAMA0"  # '/dev/cu.usbserial-1410' on MAC with USBtoSERIAL device
BAUD_RATE = 9600


def serial_read(resource):
    acc = b''
    bytes_read = resource.read()

    while bytes_read != b'':
        acc += bytes_read
        bytes_read = resource.read()
    return acc


def serial_send(resource, cmd):
    resource.write(cmd)
    sleep(0.001)


def serial_cmd(cmd):
    with serial.Serial(DEVICE, BAUD_RATE, timeout=1) as resource:
        print("Sending command: %s" % str(cmd))
        serial_send(resource, cmd)
        result = serial_read(resource)
        print("device returned: %s" % str(result))
        return result


def init_bt_device():
    serial_cmd(b'AT')
    serial_cmd(b'AT+RENEW')  # this resets to factory
    serial_cmd(b'AT+NAME%s' % b'RPI_BT')  # SET DEVICE NAME FOR DISCOVERY
    serial_cmd(b'AT+NOTI1')  # SET NOTIFICATIONS ON
    serial_cmd(b'AT+RESET')  # restart device


def bt_notify(text):
    serial_cmd(b'AT+CHAR%s' % bytes(text, 'utf8'))


def main():
    init_bt_device()
    while True:
        bt_notify(strftime('%H:%M:%S'))
        sleep(5)


if __name__ == '__main__':
    main()
