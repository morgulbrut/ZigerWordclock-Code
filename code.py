# pyright: reportShadowedImports=false
# pyright: reportMissingImports=false

import words
import wifi
import socketpool
import time
import rtc
import adafruit_dotstar
import settings
import colours
import busio
import supervisor
import adafruit_ntp
import random

# time.localtime indices
HOUR = 3
MINUTE = 4
SECOND = 5
MONTH = 1
DAY = 2

TRACE = True

if settings.LIGHT_SENSOR == True:
    import adafruit_bh1750
    i2c = busio.I2C(settings.I2C_SDA,settings.I2C_SCL)
    light_sensor = adafruit_bh1750.BH1750(i2c)

strip = adafruit_dotstar.DotStar(settings.LED_PIN_CI, settings.LED_PIN_DI, settings.LED_NUMBER, brightness=settings.LED_DEFAULT_BRIGHTNESS, auto_write=False)
realtc = rtc.RTC()

def error(e,colour,word):
    clear_clockface()
    strip[words.WIFI] = colour
    for i in word:
        strip[i] = colour
    strip.show()
    print(e)
    time.sleep(1)
    supervisor.reload()

def set_time():
    if TRACE:
        print("[function]: set_time()")
    print(f"[set_time]: Stopping station")
    radio = wifi.radio
    radio.stop_station()

    strip[words.WIFI] = colours.BLUE
    strip.show()

    radio.start_station()
    print(f"[set_time]:Trying to connect to {settings.SSID} using {settings.PWD}")
    
    try:
        radio.connect(settings.SSID, settings.PWD,timeout=settings.TIMEOUT)
        strip[words.WIFI] = colours.GREEN
        strip.show()
    except ConnectionError as e:
        error(e,colours.RED,words.CON_ERROR)

    print("[set_time]: connected")
    time.sleep(1)

    pool = socketpool.SocketPool(wifi.radio)

    print("[set_time]: Getting time from NTP")
    ntp = adafruit_ntp.NTP(pool, tz_offset=1)
    try:
        realtc.datetime = ntp.datetime
    except Exception as e:
        error(e,colours.ORANGE,words.NTP_ERROR)

    print("[set_time]: Switching off WiFi")
    radio.stop_station()

def get_simple_time():
    if TRACE:
        print("[function]: get_simple_time()")
    hour = realtc.datetime[HOUR]
    minute = realtc.datetime[MINUTE]
    second = realtc.datetime[SECOND]
    print(f"[get_simple_time]: {hour}:{minute}:{second}")
    return hour, minute, second

def clear_clockface():
    if TRACE:
        print("[function]: clear_clockface()")
    for i in range(settings.LED_NUMBER):
        strip[i] = (0, 0, 0)

def test_strip():
    if TRACE:
        print("[function]: test_strip()")
    for i in range(settings.LED_NUMBER):
        if i%10 == 0:
            strip[i] = settings.PALLETE[0]
        elif i%5 == 0:
            strip[i] = settings.PALLETE[1]
        else:
            strip[i] = colours.rainbow(i)
    time.sleep(1)
    strip.show()

def set_normal(h,m):
    if TRACE:
        print(f"[function]: set_normal({h},{m})")
    for i in words.HOURS[h]:
        strip[i] = settings.PALLETE[2]

    # Minuten (Worte)
    mins = int((m) / 5)
    for i in words.MINUTES[mins]:
        strip[i] = settings.PALLETE[1]

    # Minuten (Punkte)
    mins = m % 5
    for i in words.FIVE_MINUTES[mins]:
        strip[i] = settings.PALLETE[1]

    for i in words.IT:
        strip[i] = settings.PALLETE[0]
    for i in words.IS:
        strip[i] = settings.PALLETE[0]

def set_random(h,m):
    if TRACE:
        print(f"[function]: set_random({h},{m})")
    for i in words.HOURS[h]:
        strip[i] = colours.rnd(i)
    mins = int((m) / 5)
    for i in words.MINUTES[mins]:
        strip[i] = colours.rnd(i)
    mins = m % 5
    for i in words.FIVE_MINUTES[mins]:
        strip[i] = colours.rnd(i)
    for i in words.IT:
        strip[i] = colours.rnd(i)
    for i in words.IS:
        strip[i] = colours.rnd(i)

def set_fancy(h,m):
    if TRACE:
        print(f"[function]: set_fancy({h},{m})")
    for i in words.HOURS[h]:
        strip[i] = colours.fancy(i)
    mins = int((m) / 5)
    for i in words.MINUTES[mins]:
        strip[i] = colours.fancy(i)
    mins = m % 5
    for i in words.FIVE_MINUTES[mins]:
        strip[i] = colours.fancy(i)
    for i in words.IT:
        strip[i] = colours.fancy(i)
    for i in words.IS:
        strip[i] = colours.fancy(i)

def set_all_the_colours(h,m):
    if TRACE:
        print(f"[function]: set_all_the_colours({h},{m})")
    for i in words.HOURS[h]:
        strip[i] = colours.all_the_colours(i)
    mins = int((m) / 5)
    for i in words.MINUTES[mins]:
        strip[i] = colours.all_the_colours(i)
    mins = m % 5
    for i in words.FIVE_MINUTES[mins]:
        strip[i] = colours.all_the_colours(i)
    for i in words.IT:
        strip[i] = colours.all_the_colours(i)
    for i in words.IS:
        strip[i] = colours.all_the_colours(i)

def set_rainbow(h,m):
    if TRACE:
        print(f"[function]: set_rainbow({h},{m})")
    for i in words.HOURS[h]:
        strip[i] = colours.rainbow(i)
    mins = int((m) / 5)
    for i in words.MINUTES[mins]:
        strip[i] = colours.rainbow(i)
    mins = m % 5
    for i in words.FIVE_MINUTES[mins]:
        strip[i] = colours.rainbow(i)
    for i in words.IT:
        strip[i] = colours.rainbow(i)
    for i in words.IS:
        strip[i] = colours.rainbow(i)

def set_clockface(h, m, mode):
    if TRACE:
        print(f"[function]: set_clockface({h},{m},{mode})")
    clear_clockface()
    # Stunden
    if m >= 25:
        h += 1
    h = h % 12
    if mode == 'normal':
        set_normal(h,m)
    if mode == 'random':
        set_random(h,m)
    if mode == 'fancy':
        set_fancy(h,m)
    if mode == 'all_the_colours':
        set_all_the_colours(h,m)
    if mode == 'rainbow':
        set_rainbow(h,m)

    if settings.LIGHT_SENSOR == True:
        brightness = light_sensor.lux / 100
        if brightness <= settings.LED_MIN_BRIGHTNESS:
            brightness = settings.LED_MIN_BRIGHTNESS
        strip.brightness = brightness
        if TRACE:
            print(f"[brightness]: {strip.brightness}")
    strip.show()


def wordclock():
    if TRACE:
        print("[function]: wordclock()")
    print(settings.BANNER)
    print(f'[wordclock]: Running in mode: {settings.MODE}')
    print(f'[wordclock]: Displaymode: {settings.DISPLAY_MODE}')
   
    print(f"[wordclock]: Clearing clockface")
    clear_clockface()
    strip[words.MIZ[0]]=settings.PALLETE[0]
    strip[words.MIZ[1]]=settings.PALLETE[1]
    strip[words.MIZ[2]]=settings.PALLETE[2]
    strip.show()
    set_time()

    while True:
        try:
            hour, minute, second = get_simple_time()
            set_clockface(hour, minute,settings.DISPLAY_MODE)
            time.sleep(10)

            if hour == 3 and minute == 0 and second <= 10:
                set_time()

            if hour == 14 and minute == 40 and second <= 10:
                settings.PALLETE = colours.PALLETE_AURORA

            if hour == 16 and minute == 0 and second <= 10:
                settings.PALLETE = colours.PALLETE_AUTUMN

            if settings.MODE == 'demo':
                if second <=10:
                    ch = random.randint(0,3)
                    if ch  == 0:
                        colours.PALLETE_RANDOM = colours.rand_pallete()
                        settings.PALLETE = colours.PALLETE_RANDOM
                        print('[Demomode]: New random pallete')
                    if ch  == 1:
                        settings.PALLETE = random.choice(colours.PALS)
                        print('[Demomode]: Changed pallete')
                    if ch == 2:
                        settings.DISPLAY_MODE = random.choice(['normal','random', 'fancy','all_the_colours'])
                        print(f'[Demomode]: New displaymode: {settings.DISPLAY_MODE}')
                    if ch == 3:
                        colours.rand_setup()
                        print('[Demomode]: Changed random colours')
        except Exception as e:
            error(e,colours.MAGENTA,words.GEN_ERROR)

if __name__ == "__main__":
    if settings.MODE == 'demo':
        test_strip()
        time.sleep(10)
        wordclock()
    if settings.MODE == 'wordclock':
        wordclock()
    if settings.MODE == 'testing':
        settings.PALLETE = colours.PALLETE_AURORA
        print("selftest...")
        test_strip()
        time.sleep(0.75)
