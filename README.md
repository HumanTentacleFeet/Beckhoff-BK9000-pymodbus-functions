# Arduino-inspired functions to program Beckhoff's BK9000 PLC (tested on Ubuntu/Linux Mint)

## Short description
A script containing a few functions to make it easier to program the Beckhoff BK9000 and it's KL2612 and KL1002 terminals. The code uses python 2.7 and the package "pymodbus" to speak to the BK9000.

## General information
The script adds two usable functions: digitalRead() and digitalWrite(). These functions are inspired by the commands that the Arduino IDE uses.
You can use these two commands to read input from the KL1002 input-terminal or to control output from the KL2612 output-terminal.

## Examples
### Basic commands
#### digitalWrite()
digitalWrite(0, True) turns the first LED on the first KL2612 output-terminal on, and digitalWrite(0, False) turns it off again.
#### digitalRead()
digitalRead(0): Reads the status of the first LED of the first KL1002 input-terminal, returns True if it's connected and returns False if it's not connected
#### *convert_number_to_binary_io()*
*The script also contains a third function: convert_number_to_binary_io(). This function is used by digitalRead() to convert the BK9000's response into an array which digitalRead() can use to see which inputs are connected or not. You do not need to call this function manually.*
### Arduino's blink for KL2612-terminals
The file blink.py contains code that makes the first LED of the first KL2612 output-terminal blink (turn on and off every second). In the Arduino IDE, there is example-code called "Blink without delay". This example code has been inspired by "Blink without delay"
