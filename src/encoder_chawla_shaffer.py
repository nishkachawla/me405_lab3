"""!
@file encoder_chawla_shaffer.py
This file contains code used to configure the encoders. 

@details Objects of this class can be used to configure the encoder driver
         to measure motor rotation in units of encoder ticks.
    
@author Nishka Chawla
@author Ronan Shaffer
@date   26-Jan-2022
@copyright (c) Released under GNU Public License
"""
import pyb
import time 


class EncoderDriver:
    """!
    This class implements an encoder driver for an ME405 kit. 
    """
    
    def __init__(self, pinA, pinB, tim_num):
        """!
        Creates an encoder driver by initializing GPIO pins and reading motor 
        rotation in units of encoder ticks.
        @param pinA         Defines the pin for channel 1 of the timer.
        @param pinB         Defines the pin for channel 2 of the timer.
        @param tim_num      Defines the number of the timer object.
        """
        ## Reference counter
        self._ref_count = 0
        
        ## Current encoder position
        self._current_pos = 0
        
        ## Overflow for Encoder timer counter
        self.period = 65535
        
        ## Timer object used for encoder counting.
        self.tim = pyb.Timer(tim_num, prescaler = 0, period = self.period)
        
        ## Encoder Channel 1 for a timer object.
        self.tch1 = self.tim.channel(1, pyb.Timer.ENC_AB, pin=pinA)
        
        ## Encoder Channel 2 for a timer object.
        self.tch2 = self.tim.channel(2, pyb.Timer.ENC_AB, pin=pinB)
        
    def update(self):
        """!
        This method updates encoder position and delta by tracking the current 
        encoder position and correcting for overflow.
        """       
        ## The current tick count.
        self.update_count = self.tim.counter()
        
        ## Ticks between two most recent encoder positions.
        self.delta = self.update_count - self._ref_count
        
        if self.delta > 0 and self.delta > self.period/2:
            self.delta -= self.period
        if self.delta < 0 and abs(self.delta) > self.period/2:
            self.delta += self.period
            
        self._ref_count = self.tim.counter()
        
        self._current_pos += self.delta
                
    def read(self):
        """!
        This method returns the current encoder position.
        @returns    The position of the motor shaft.
        """ 
        return self._current_pos
    
    def zero(self):
        """!
        This method sets the encoder position to zero.
        """
        self._current_pos = int(0)
    
    def step_rsp(self):
        """!
        This method sets the encoder position to zero.
        """
        pass


