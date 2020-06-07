import sys
from time import sleep
import smbus

LCD_FUNCTION_SET = 0x20
LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00
LCD_4BIT_MODE = 0x00
LCD_DISPLAY_CONTROL = 0x08
LCD_DISPLAY_ON = 0x04
LCD_CLEAR_DISPLAY = 0x01
LCD_ENTRY_MODE_SET = 0x04
LCD_ENTRY_LEFT = 0x02
LCD_RETURN_HOME = 0x02
LCD_BACK_LIGHT = 0x08

# Low level functions

bus = smbus.SMBus(1)


def write_cmd(cmd):
    bus.write_byte(0x27, cmd)
    sleep(0.0001)


# High level functions

En = 0b00000100  # Enable bit


def lcd_strobe(data):
    write_cmd(data | En | LCD_BACK_LIGHT)
    sleep(.0005)
    write_cmd(((data & ~En) | LCD_BACK_LIGHT))
    sleep(.0001)


def lcd_clear():
    lcd_write(LCD_CLEAR_DISPLAY)
    lcd_write(LCD_RETURN_HOME)


def lcd_write_four_bits(data):
    write_cmd(data | LCD_BACK_LIGHT)
    lcd_strobe(data)


def lcd_write(command, mode=0):
    lcd_write_four_bits(mode | (command & 0xF0))
    lcd_write_four_bits(mode | ((command << 4) & 0xF0))


def lcd_display_string(string, line):
    if line == 1:
        lcd_write(0x80)
    if line == 2:
        lcd_write(0xC0)
    if line == 3:
        lcd_write(0x94)
    if line == 4:
        lcd_write(0xD4)
    for char in string:
        lcd_write(ord(char), 0b00000001)


def init_lcd():
    lcd_write(0x03)
    lcd_write(0x03)
    lcd_write(0x03)
    lcd_write(0x02)
    lcd_write(LCD_FUNCTION_SET | LCD_2LINE | LCD_5x8DOTS | LCD_4BIT_MODE)
    lcd_write(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON)
    lcd_write(LCD_CLEAR_DISPLAY)
    lcd_write(LCD_ENTRY_MODE_SET | LCD_ENTRY_LEFT)
    sleep(0.2)


def main():
    init_lcd()
    lcd_clear()
    lcd_display_string(sys.argv[1], 1)


if __name__ == '__main__':
    main()
