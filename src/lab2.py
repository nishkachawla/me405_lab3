import serial
from matplotlib import pyplot
import time
## Stores time values of step response
time_list = []
## Stores position values of encoder during step response
pos_list = []

# Open serial port for communication between PC and Nucleo
with serial.Serial('COM11', 115200) as s_port:
    
    s_port.write(b'\x03') #ctrl-C
    s_port.write(b'\x04') #runs main -- ctrl-D
    time.sleep(0.5)
    ## Proportional gain value
    Kp = 0.4
    s_port.write(b'0.05\r')
    ## Runs counter controls number of iterations of data reading
    runs = 0
    
    while runs <= 201:
        ## Stores single line of data read from serial port
        raw_data = s_port.readline()
        ## Converts data type and removes non-number characters
        data = str(raw_data)
        data = data[2:]
        data = data[:-5]
        ## Splits string of data into separate time and position values
        l = data.split(',')
        try:
            ## Convert time value to float
            time = float(l[0])
            ## Convert position value to float
            pos = float(l[1])
            
        except:
            pass
        
        else:
            # Add current time and position values to list for ploting
            time_list.append(time-11)
            pos_list.append(pos)
            
        runs += 1
            
    pyplot.plot(time_list, pos_list, color = 'b')
    pyplot.xlabel('Time [ms]')
    pyplot.ylabel('Position [ticks]')
    pyplot.title('Step Response: Kp = 0.05')
    pyplot.show()

        # try:
        #     for char in data:
        #         if char.isdigit() == True:
        #             if char_flag == 1:
        #                 char2.append(char)
        #             elif char.isdigit() == True:
        #                 char1.append(char)
        #         elif char.isdigit() == False:
        #             char_flag = 1
                    
        #     # float(data[0])
        #     # float(data[1])
        # except:
        #     pass
        # else:
        #     # time_list.append()
        #     # pos_list.append()
        #     data.split(',')
        #     print(data)
        # # print(s_port.read().split(b','))
        #     try:
        #         time = float(data[0])
        #         pos = float(data[1])
        #     except ValueError:
        #         pass
        #     else:
        #         pass
        #         # time_list.append()
                # pos_list.append()
    
#pyplot.plot(time_list, pos_list, color = 'b')
#pyplot.xlabel('Time')
#pyplot.ylabel('Position')
#pyplot.title('Step Response')
#pyplot.show()