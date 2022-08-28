import os
class AW_MULTI_BREATH_DATA:
    time = [0, 0, 0, 0, 0]
    repeat_nums = 0
    fadeh = 4095
    fadel = 0

class ALGO_DATA:
    total_frames = 0
    cur_frame = 0
    data_start = 0
    data_end = 0

LED_DRIVER_PATH = "/sys/class/leds/aw210xx_led"
NODE_SINGLE_LED_BR = "single_led_br"

LEDS_BREATH_DATA = AW_MULTI_BREATH_DATA()
LEDS_BREATH_DATA.time = [0, 500, 50, 500, 50]
LEDS_BREATH_DATA.repeat_nums = 1
LEDS_BREATH_DATA.fadeh = 4095
LEDS_BREATH_DATA.fadel = 0

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

def charging_leds_horse_race(start: int, state: int):
    leds = [16,13,11,9,12,10,14,15,8]
    pass

def round_leds_on(state: int):
    brightness = 0
    if state == 1:
        brightness = LED_BRIGHTNESS
    round_leds_br_set(brightness)

def algorithm_get_correction(algo_data: ALGO_DATA):
    start_idx = 0
    end_idx = 0

    if algo_data.cur_frame == 0:
        start_idx = algo_data.data_start
    elif (algo_data.total_frames - 1) == algo_data.cur_frame:
        start_idx = algo_data.data_end
    elif algo_data.data_end >= algo_data.data_start:
        # get the start index in gamma array
        while start_idx < GAMMA_STEPS:
            if GAMMA_BRIGHTNESS[start_idx] >= algo_data.data_start:
                break
            start_idx += 1
        
        if start_idx >= GAMMA_STEPS:
            start_idx = GAMMA_STEPS - 1
        
        end_idx = GAMMA_STEPS - 1
        while end_idx >= 0:
            if GAMMA_BRIGHTNESS[end_idx] <= algo_data.data_end:
                break
                end_idx -= 1
        
        if end_idx < 0:
            end_idx = 0
        # get current index
        start_idx += (end_idx - start_idx) * algo_data.cur_frame / (algo_data.total_frames - 1)
        start_idx = GAMMA_BRIGHTNESS[start_idx]
    else:
        while start_idx < GAMMA_STEPS:
            if GAMMA_BRIGHTNESS[start_idx] >= algo_data.data_end:
                break
            start_idx += 1
        
        if start_idx >= GAMMA_STEPS:
            start_idx = GAMMA_STEPS - 1
        
        end_idx = GAMMA_STEPS - 1
        while end_idx >= 0:
            if GAMMA_BRIGHTNESS[end_idx] <= algo_data.data_start:
                break
            end_idx -= 1
        
        if end_idx < 0:
            end_idx = 0
        
        end_idx -= (end_idx - start_idx) * algo_data.cur_frame / (algo_data.total_frames - 1)
        start_idx = GAMMA_BRIGHTNESS[end_idx]

    return start_idx

def leds_breath(led_group: int):
    update_frame_idx = 0
    brightness = 0
    algo_data = ALGO_DATA()
    data = AW_MULTI_BREATH_DATA()
    breath_cur_phase = 0
    breath_cur_loop = 0
    breath_phase_nums = 5
    
    breath_loop_end = 0
    data = LEDS_BREATH_DATA

    algo_data.cur_frame = 0
    algo_data.total_frames = (data.time[0] + 19) / 20 + 1
    algo_data.data_start = data.fadel
    data_end = data.fadeh

    if led_group == 0:
        round_leds_br_set(0)
    elif led_group == 1:
        single_led_br_set(1, 0)
    elif led_group == 2:
        all_white_leds_br_set(0)

    while True:
        update_frame_idx = 1
        algo_data.cur_frame += 1
        if algo_data.cur_frame >= algo_data.total_frames:
            algo_data.cur_frame = 0
            breath_cur_phase += 1
            if breath_cur_phase >= breath_phase_nums:
                breath_cur_phase = 1
                if data.repeat_nums == 0:
                    breath_cur_loop = 0
                elif breath_cur_loop >= (data.repeat_nums - 1):
                    update_frame_idx = 0
                else :
                    breath_cur_loop += 1
            
            if update_frame_idx == 1:
                algo_data.total_frames = data.time[breath_cur_phase]/20 + 1
                if breath_cur_phase == 1:
                    algo_data.data_start = data.fadel
                    algo_data.data_end = data.fadeh
                elif breath_cur_phase == 2:
                    algo_data.data_start = data.fadeh
                    algo_data.data_end = data.fadeh
                elif breath_cur_phase == 3:
                    algo_data.data_start = data.fadeh
                    algo_data.data_end = data.fadel
                else:
                    algo_data.data_start = data.fadel
                    algo_data.data_end = data.fadel
            else:
                algo_data.cur_frame = 0
                algo_data.total_frames = 1
                algo_data.data_start = 0
                algo_data.data_end = 0
                algo_data.breath_loop_end = 1

        brightness = algorithm_get_correction(algo_data)

        if breath_cur_phase == 0:
            brightness == 0
        if breath_cur_phase == 2:
            brightness = data.fadeh
        
        if led_group == 0:
            round_leds_br_set(brightness)
        elif led_group == 1:
            single_led_br_set(1, brightness)
        elif led_group == 2:
            all_white_leds_br_set(brightness)
        
        if breath_loop_end == 1:
            break
    
    if led_group == 0:
        round_leds_br_set(0)
    elif led_group == 1:
        single_led_br_set(1, 0)
    elif led_group == 2:
        all_white_leds_br_set(0)

def round_leds_breath():
    leds_breath(0)


round_leds_breath()

# all_white_leds_br_set(0)