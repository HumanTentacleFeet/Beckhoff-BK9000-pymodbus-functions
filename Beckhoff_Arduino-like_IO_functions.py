#! /usr/bin/env python2

#############################################################
#                                                           #
#  Two Arduino-like functions for the Beckhoff BK9000       #
#  and it's KL2612 and KL1002 I/O terminals.                #
#  To use this script, you need pymodbus to be installed.   #
#                                                           #
#  Written by https://www.github.com/HumanTentacleFeet      #
#                                                           #
#############################################################

try:
    # Import pymodbus, os and some items from time
    from pymodbus.client.sync import ModbusTcpClient
    import os
    from time import time, sleep

    # Define the IP-address and port of the client you want to connect to.
    CLIENT_IP_ADDRESS = '192.168.2.100'  #Your client might be connected to a different IP-address, change this if that is true.
    CLIENT_PORT = 502

    # Tell python how to connect to the client.
    client = ModbusTcpClient(CLIENT_IP_ADDRESS, CLIENT_PORT)

    def convert_number_to_binary_input(number):  # This function performs some calculatinputns for digitalRead(). When the BK9000's input registers are read, the BK9000 gives back a number. That number must be converted.
        if(number>65535):  # If someone tries to manually call this function with a number that is too big to calculate, stop the script.
            print('Error: convert_number_to_binary_input() can only calculate numbers up to 65535.\nExiting...')
            exit(1)
        totalNumber = number  # I don't want to touch number here, so let's put that number-variable inside a 'private' variable.
        binary_array = []  # This array will be filled with 16 numbers that are 2^1, 2^2, etc.
        input = []  # This array is going to contain which inputs are connected and which inputs are disconnected. (This is only for one register, so this function will be called eight times per digitalRead() call.)
        for i in range(0, 16):
            binary_array.append(2**i)  # Fill this array with binary numbers.
        binary_array.reverse()  # The array must be reversed before it can be used properly.
        for currentNumber in range(0,16):  # For each number in the binary_array.
            if(totalNumber <= 0):  # Check if the totalNumber is greater or smaller than the current binary number.
                input.append(0)
            else:
                if(totalNumber-binary_array[currentNumber]>=0):  # If this equals True, subtract the current binary number from the totalNumber and add a '1' to the input_array,
                    input.append(1)
                    totalNumber = totalNumber-binary_array[currentNumber]
                else:  # If this equals False, add a '0' to the input_array.
                    input.append(0)
        input.reverse()  # The array is now in reverse, so reverse it before returning it.
        return input

    def digitalRead(input_number, print_input=False):  # This function checks if an input is connected or not. To see a list of all the input readings, run digitalRead(number_you_wish_to_read, print_input=True) instead of digitalRead(number_you_wish_to_read).
        input_master_array = []  # This array is going to contain all the input-readings (which inputs are connected/disconnected).
        # Read all the registers and let convert_number_to_binary_input() convert them into arrays
        register_0 = convert_number_to_binary_input(client.read_input_registers(0).registers[0])
        register_1 = convert_number_to_binary_input(client.read_input_registers(1).registers[0])
        register_2 = convert_number_to_binary_input(client.read_input_registers(2).registers[0])
        register_3 = convert_number_to_binary_input(client.read_input_registers(3).registers[0])
        register_4 = convert_number_to_binary_input(client.read_input_registers(4).registers[0])
        register_5 = convert_number_to_binary_input(client.read_input_registers(5).registers[0])
        register_6 = convert_number_to_binary_input(client.read_input_registers(6).registers[0])
        register_7 = convert_number_to_binary_input(client.read_input_registers(7).registers[0])
        # Add all the arrays to one big array of 128 items. The master array is going to contain all of the input readings.
        for register_item in range(0,16):
            input_master_array.append(register_0[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_1[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_2[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_3[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_4[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_5[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_6[register_item])
        for register_item in range(0,16):
            input_master_array.append(register_7[register_item])
        # This is the part that prints the complete input-table.
        if(print_input==True):
            print(input_master_array)
        # This is the part that checks if the input is connected or not and gives back True or False.
        if(input_master_array[input_number] == True):
            return True
        elif(input_master_array[input_number] == False):
            return False

    def digitalWrite(output_number, status):
        if(status != True and status != False):
            # Humans make mistakes. Make sure not to write invalid statusses to the BK9000.
            print('digitalWrite: Error: Invalid status: A status can only be True or False.\nExiting...')
            exit(1)
        else:
            # This looks a lot like digitalWrite already...
            client.write_coils(output_number, status)

    ####    <Your code here>    ####

except KeyboardInterrupt:
    print('\nCtrl-C has been pressed.\nExiting...')
