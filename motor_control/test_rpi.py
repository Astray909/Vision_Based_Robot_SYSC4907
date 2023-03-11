import RPi.GPIO as GPIO

# set the pin numbering mode to BCM
GPIO.setmode(GPIO.BCM)

# set up the pins
pins = [5, 6, 13, 19]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# set the pins to high
for pin in pins:
    GPIO.output(pin, GPIO.HIGH)

# cleanup the GPIO pins
GPIO.cleanup()
