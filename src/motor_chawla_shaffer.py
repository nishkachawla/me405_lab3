"""!
@file motor_chawla_shaffer.py
This file contains code used to configure the L6206 motor. 

@details Objects of this class can be used to configure the DRV8847
         motor driver to set the motor duty cycle and perform motor control.
    
@author Nishka Chawla
@author Ronan Shaffer
@date   26-Jan-2022
@copyright (c) Released under GNU Public License
"""

import pyb
import time


class MotorDriver:
    """!
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer_num):
        """!
        Creates a motor driver by initializing GPIO pins and turning the motor 
        off for safety. 
        @param en_pin       The enable pin for the motor. 
        @param in1pin       The pin for channel A of the motor.
        @param in2pin       The pin for channel B of the motor.
        @param timer_num    The number of the timer object.  
        """
        ## The enable pin for the motor. 
        self.en_pin = en_pin
        
        ## The pin for channel A of the motor.
        self.in1pin = in1pin
        
        ## The pin for channel B of the motor.
        self.in2pin = in2pin
        
        ## The number of the timer object.  
        self.timer_num = timer_num
        
        # Enable pin set to high
        self.en_pin.high()
        
        ## Instantiation of a timer object. 
        self.tim = pyb.Timer(self.timer_num, freq = 20000)
        
        ## Instantiation of channel A of the motor. 
        self.channel_A = self.tim.channel(1, pyb.Timer.PWM, pin=self.in1pin)
        
        ## Instantiation of channel A of the motor. 
        self.channel_B = self.tim.channel(2, pyb.Timer.PWM, pin=self.in2pin)
        
        
    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent to the motor to the given 
        level. Positive values cause torque in one direction, negative values
        in the opposite direction.
        @param level    A signed integer holding the duty cycle of the voltage 
                        sent to the motor. 
        '"""
        ## The duty cycle of the voltage sent to the motor. 
        self.level = level
        
        if self.level > 0:
            
            if self.level > 100:
                
                self.channel_A.pulse_width_percent(100)
                self.channel_B.pulse_width_percent(0)
            
            self.channel_A.pulse_width_percent(self.level)
            self.channel_B.pulse_width_percent(0)
            
        if self.level < 0:
            
            if self.level < -100:
                
                self.channel_A.pulse_width_percent(0)
                self.channel_B.pulse_width_percent(100)
            
            self.channel_A.pulse_width_percent(0)
            self.channel_B.pulse_width_percent(-self.level)
            
        if self.level == 0:
            
            self.channel_A.pulse_width_percent(0)
            self.channel_B.pulse_width_percent(0)
        
#         print ('Setting duty cycle to ' + str (self.level))
