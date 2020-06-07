from time import sleep

from lcd import init_lcd, lcd_display_string, lcd_clear
from networking import read_socket_value

update_interval = 5


def main():
    init_lcd()

    while True:
        read_value = read_socket_value()
        pm10, pm25 = read_value.decode("utf-8") .split('|')
        lcd_clear()
        lcd_display_string("PM10  : %s" % pm10.rjust(4), 1)
        lcd_display_string("PM2.5 : %s" % pm25.rjust(4), 2)
        sleep(update_interval)


if __name__ == '__main__':
    main()
