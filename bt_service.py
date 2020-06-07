from time import sleep

from bt import init_bt_device, bt_notify
from networking import read_socket_value

update_interval = 5


def main():
    init_bt_device()

    while True:
        read_value = read_socket_value()
        bt_notify(read_value.decode("utf8"))
        sleep(update_interval)


if __name__ == '__main__':
    main()
