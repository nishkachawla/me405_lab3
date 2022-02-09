"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import print_task
import utime
import motor_chawla_shaffer
import encoder_chawla_shaffer
import closedloopcontrol
import array as array

# def task1_fun ():
#     """!
#     Task which puts things into a share and a queue.
#     """
#     counter = 0
#     while True:
#         share0.put (counter)
#         q0.put (counter)
#         counter += 1

#         yield (0)


# def task2_fun ():
#     """!
#     Task which takes things out of a queue and share to display.
#     """
#     while True:
#         # Show everything currently in the queue and the value in the share
#         print ("Share: {:}, Queue: ".format (share0.get ()), end='');
#         while q0.any ():
#             print ("{:} ".format (q0.get ()), end='')
#         print ('')

#         yield (0)

## Input pin configuration
inn = pyb.Pin.IN

## Output with push-pull control pin configuration
out = pyb.Pin.OUT_PP

# Define motor pins
## The enable pin for the motor 1. 
pinENA = pyb.Pin(pyb.Pin.cpu.A10, out)
## The enable pin for the motor 2. 
pinENB = pyb.Pin(pyb.Pin.cpu.C1, out)
## Pin variable for channel A of motor 1.
pinB4 = pyb.Pin(pyb.Pin.cpu.B4, out)
## Pin variable for channel B of motor 1.
pinB5 = pyb.Pin(pyb.Pin.cpu.B5, out)
## Pin variable for channel A of motor 2.
pinA0 = pyb.Pin(pyb.Pin.cpu.A0, out)
## Pin variable for channel B of motor 2.
pinA1 = pyb.Pin(pyb.Pin.cpu.A1, out)

# Define encoder pins
## Pin variable for channel 1 of the encoder A.
pinB6 = pyb.Pin(pyb.Pin.cpu.B6, out)
## Pin variable for channel 2 of the encoder A.
pinB7 = pyb.Pin(pyb.Pin.cpu.B7, out)
## Pin variable for channel 1 of the encoder B.
pinC6 = pyb.Pin(pyb.Pin.cpu.C6, out)
## Pin variable for channel 2 of the encoder B.
pinC7 = pyb.Pin(pyb.Pin.cpu.C7, out)

## Index to iterate through arrays
runs = 0

## Array size
array_size = int((2000/10)+1)

## Array storing time data.
time_list = array.array("f", [0] * array_size)
## Array storing position data.
pos_list = array.array("f", [0] * array_size)

# # # Create a share and a queue to test function and diagnostic printouts
# share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
# q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
#                         name = "Queue 0")

# shares.print_task = print_task.PrintTask (name = 'Printing', 
#         buf_size = 100, thread_protect = True, priority = 0)

## Instantiation of Encoder 2 reading shared variable.
enc2reading = task_share.Queue ('l', 500, thread_protect = False, overwrite = False,
                        name = "enc2reading")

## Instantiation of Motor 1 position setpoint shared variable.
motor1setpoint = task_share.Share ('h', thread_protect = False, name = "motor1setpoint")
## Instantiation of Motor 2 position setpoint shared variable.
motor2setpoint = task_share.Share ('h', thread_protect = False, name = "motor2setpoint")

## Instantiation of Motor 1 proportional gain.
kp1 = task_share.Share ('f', thread_protect = False, name = "kp1")
## Instantiation of Motor 2 proportional gain.
kp2 = task_share.Share ('f', thread_protect = False, name = "kp2")

## Instantiation of motor 1 object.
motor1 = motor_chawla_shaffer.MotorDriver(pinENA, pinB4, pinB5, 3)
## Instantiation of motor 2 object.
motor2 = motor_chawla_shaffer.MotorDriver(pinENB, pinA0, pinA1, 5)

## Instantiation of encoder 1 object.
encoder1 = encoder_chawla_shaffer.EncoderDriver(pinB6, pinB7, 4)
## Instantiation of encoder 2 object.
encoder2 = encoder_chawla_shaffer.EncoderDriver(pinC6, pinC7, 8)

# Zeroing encoder 1.
encoder1.zero()
# Zeroing encoder 2.
encoder2.zero()

## Instantiation of controller object.
#setpoint eventually changed to get() **********
controller1 = closedloopcontrol.ClosedLoop(motor1setpoint.put(int(16384)), kp1.get(), int(100), int(-100))
## Instantiation of controller object.
#setpoint eventually changed to get() **********
controller2 = closedloopcontrol.ClosedLoop(motor2setpoint.put(int(16384)), kp2.get(), int(100), int(-100))
        
def motor1_func ():
    """!
    Task which puts things into a share and a queue.
    """
    while True:
        # Sets motor duty cycle to actuation level
        encoder1.update()
        # enc1reading.put(encoder1.read())
        # encreading.put(encoder1.read())
        # print_task.put(encoder1.read())
        ## Variable storing Encoder 2 position.
        # count_A = encoder1.read()
        motor1.set_duty_cycle(controller1.run(motor1setpoint.get(),encoder1.read()))

        yield (0)
        
def motor2_func ():
    """!
    Task which puts things into a share and a queue.
    """
    while True:
        # Sets motor duty cycle to actuation level
        encoder2.update()
        # enc2reading.put(encoder2.read())
        # encreading.put(encoder2.read())
        print_task.put(str(encoder2.read()))
        ## Variable storing Encoder 2 position.
        # count_B = encoder2.read()
        motor2.set_duty_cycle(controller2.run(motor2setpoint.get(),encoder1.read()))

        yield (0)
        
def print_func ():
    """!
    Task which takes things out of a queue and share to display.
    """
    runs = 0
    while True:   
        print_task.run()
        # while enc2reading.any():
            # encreading.run()
            # pos_list[runs].append(enc2reading.get())
            # print ("{:} ".format(enc2reading.get())) # this works 
            # print ("{:} ".format(pos_list[runs]))    # this doesnt
            
            # print(pos_list[runs])
        runs += 1

        yield (0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    # print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
    #        'Press ENTER to stop and show diagnostics.')

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    # task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
    #                      period = 400, profile = True, trace = False)
    # task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
    #                      period = 1500, profile = True, trace = False)
    motor1_task = cotask.Task (motor1_func, name = 'motor1_task', priority = 2, 
                         period = 10, profile = True, trace = False)
    motor2_task = cotask.Task (motor2_func, name = 'motor2_task', priority = 2, 
                         period = 10, profile = True, trace = False)
    read_task = cotask.Task (print_func, name = 'read_task', priority = 3, 
                         period = 20, profile = True, trace = False)
    
    ## Input for Kp 1
    KP1 = input('Please enter a Kp 1: ')
    controller1.set_Kp(float(KP1))
    kp1.put(float(KP1))
    
    ## Input for Kp 2
    KP2 = input('Please enter a Kp 2: ')
    controller2.set_Kp(float(KP2))
    kp2.put(float(KP2))

    # cotask.task_list.append (task1)
    # cotask.task_list.append (task2)
    cotask.task_list.append(motor1_task)
    cotask.task_list.append(motor2_task)
    cotask.task_list.append(read_task)
    # cotask.task_list.append(encreading)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    vcp.read ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    # print (task1.get_trace ())
    print ('\r\n')
