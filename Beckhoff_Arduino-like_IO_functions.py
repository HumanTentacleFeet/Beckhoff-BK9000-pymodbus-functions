#! /usr/bin/env python2

#############################################################
#                                                           #
#  Two Arduino-like functions for the Beckhoff BK9000 PLC   #
#  and it's KL2612 and KL1002 I/O terminals.                #
#  To use this script, you need pymodbus to be installed.   #
#                                                           #
#  Written by https://www.github.com/HumanTentacleFeet      #
#                                                           #
#############################################################

try:
    from pymodbus.client.sync import ModbusTcpClient
    import os
    from time import time, sleep

    PLC_IP_ADDRESS = '192.168.0.1'  #Your PLC might be connected to a different IP-address, change this if that is true
    PLC_PORT = 502

    plc = ModbusTcpClient(PLC_IP_ADDRESS, PLC_PORT)

    def convert_number_to_binary_io(number):
	if(number>680564733841876926926749214863536422911):
		print('convert_number_to_binary_io: Error: Cannot calculate numbers greater than 680564733841876926926749214863536422911.')
		exit(1)
        totalNumber = number
        binary_array = []
        io = []
        for i in range(0, 128+1):
            binary_array.append(2**(128-i))
        for currentNumber in range(0,128+1):
            if(totalNumber <= 0):
                io.append(0)
            else:
                if(totalNumber-binary_array[currentNumber]>=0):
                    io.append(1)
                    totalNumber = totalNumber-binary_array[currentNumber]
                else:
                    io.append(0)
        io.reverse()
        return io

    def digitalRead(input_number):
        io_array = convert_number_to_binary_io(plc.read_input_registers(0).registers[0])
        if(io_array[input_number] == 1):
            return True
        elif(io_array[input_number] == 0):
            return False

    def digitalWrite(output_number, status):
        if(status != True and status != False):
            print('digitalWrite: Error: Invalid status: A status can only be True or False')
            exit(1)
        else:
            plc.write_coils(output_number, status)

    ####    <Your code here>    ####

except ImportError:
    if(os.path.exists("/usr/lib/python2.7/dist-packages/pymodbus") == True):
        print('ImportError: pymodbus has been installed, so the command "import os" seems to be the problem here.')
    else:
        print('ImportError: Package "pymodbus" is missing on this system.')
