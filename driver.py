import os

LED_DRIVER_PATH = "/sys/class/leds/aw210xx_led"
NODE_SINGLE_LED_BR = "single_led_br"

def exec_shell(cmd: str):
    os.system(cmd)

def write_to_node(node: str, content: str):
    cmd = "adb shell \"su -c \'echo " + content + " > " + LED_DRIVER_PATH + "/" + node + "\'\""
    exec_shell(cmd)

def single_led_br_set(led_num: int, brightness: int):
    write_to_node(NODE_SINGLE_LED_BR, str(led_num) + " " + str(brightness))

def round_leds_br_set(brightness: int):
    for led_num in range(2, 6):
        single_led_br_set(led_num, brightness)

def horse_race_leds_br_set(start: int, brightness: int):
    led = [16, 13, 11, 9, 12, 10, 14, 15, 8]
    for led_num in range(start, 10):
        single_led_br_set(led[led_num], brightness)

def vline_leds_br_set(brightness: int):
    led = [13, 11, 9, 12, 10, 14, 15, 8]
    for led_num in led:
        single_led_br_set(led_num, brightness)

def all_white_leds_br_set(brightness: int):
    for led_num in range(1, 17):
        if led_num == 6:
            continue
        single_led_br_set(led_num, brightness)

all_white_leds_br_set(1000)