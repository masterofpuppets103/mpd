#! /bin/bash

echo gpio | sudo tee /sys/class/leds/led0/trigger
echo gpio | sudo tee /sys/class/leds/led1/trigger


echo 0 | sudo tee /sys/class/leds/led0/brightness
echo 0 | sudo tee /sys/class/leds/led1/brightness