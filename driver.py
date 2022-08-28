import os

LED_DRIVER_PATH = "/sys/class/leds/aw210xx_led"
NODE_SINGLE_LED_BR = "single_led_br"
LED_BRIGHTNESS = 100

GAMMA_BRIGHTNESS = [
    0,1,3,4,5,7,8,9,11,12,14,15,17,18,20,22,29,31,33,35,38,40,42,44,47,
    49,51,54,56,59,62,64,80,83,87,90,93,97,100,104,108,111,115,119,123,
    127,131,135,139,143,147,152,156,161,165,170,175,179,184,189,194,199,
    205,210,215,221,226,232,238,244,249,255,262,268,274,281,287,294,301,
    307,314,321,329,336,343,351,359,367,374,383,391,399,408,416,425,434,
    443,452,462,471,481,491,501,511,521,531,542,553,564,575,587,598,610,
    622,634,646,659,672,685,698,711,725,739,753,767,782,796,811,827,842,
    858,874,890,907,924,941,958,976,994,1012,1031,1050,1069,1088,1108,
    1128,1149,1169,1191,1212,1234,1256,1279,1302,1325,1349,1373,1397,
    1422,1448,1473,1499,1526,1553,1580,1608,1637,1666,1695,1725,1755,
    1786,1817,1849,1881,1914,1947,1981,2016,2051,2087,2123,2160,2197,
    2235,2274,2313,2353,2394,2435,2477,2520,2563,2607,2652,2697,2744,
    2791,2839,2887,2936,2987,3038,3090,3142,3196,3250,3306,3362,3402,
    3442,3482,3522,3562,3602,3642,3682,3707,3732,3757,3782,3807,3832,
    3857,3872,3887,3902,3917,3932,3947,3962,3977,3985,3993,4001,4009,
    4017,4025,4033,4041,4045,4049,4053,4057,4061,4065,4069,4073,4075,
    4077,4079,4081,4083,4085,4087,4089,4095
]
GAMMA_STEPS = len(GAMMA_BRIGHTNESS)

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

def charging_leds_horse_race(start: int, state: int, brightness: int):
    leds = [16,13,11,9,12,10,14,15,8]
    if state == 1:
        for led in leds:
            single_led_br_set(led, brightness)
    elif state == 2:
        horse_race_leds_br_set(start, brightness)
    elif state == 0:
        horse_race_leds_br_set(start, 0)
    pass

def round_leds_on(state: int):
    brightness = 0
    if state == 1:
        brightness = LED_BRIGHTNESS
    round_leds_br_set(brightness)


for i in range(1, 17):
    for b in GAMMA_BRIGHTNESS:
        single_led_br_set(i, b)
# round_leds_breath()

# all_white_leds_br_set(0)