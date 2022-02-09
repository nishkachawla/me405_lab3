"""!
@file closedloopcontrol.py
This file contains a controller driver used for closed loop control.

@details Objects of this class can be used to configure the controller driver
         to generate a step response for the motor.
    
@author Nishka Chawla
@author Ronan Shaffer
@date   3-Feb-2022
@copyright (c) Released under GNU Public License
"""

class ClosedLoop:
    """!
    This class implements a closed-loop controller class for an ME405 kit, containing
    set_Kp, run, and get_Kp methods to perform speed control for the motor driver.
    """
    def __init__(self, setpoint, Kp, sat_max, sat_min):
        """!
        Creates a controller driver using a proportional gain controller.
        @param setpoint     Defines the reference value for the motor speed.
        @param Kp           Defines the chosen proportional gain.
        @param sat_max      The maximum saturation limit on the PWM level.
        @param sat_min      The minimum saturation limit on the PWM level.
        """
        
        ## Initialisation of error variable
        self.error = 0
        
        ## Initialisation of reference variable in ticks
        self.setpoint = setpoint
        
        ## Initialisation of proportional gain
        self.Kp = Kp
        
        ## Saturation High Limit
        self.sat_max = sat_max
        
        ## Saturation Low Limit
        self.sat_min = sat_min
        
        ## Initialisation of actuation signal variable.
        self.act = 0
        
    def set_Kp(self, Kp):
        """!
        This method sets the proportional gain value.
        @param  Kp  Proportional gain value set by the user.
        """ 
        self.Kp = float(Kp)
        
    def set_setpoint(self, setpoint):
        """!
        This method sets the motor setpoint value. 
        @param  setpoint  Proportional gain value set by the user.
        """ 
        ## Setpoint variable for motor reference speed.
        self.setpoint = setpoint

    def run(self, setpoint, msr):      
        """!
        This method performs proportional control on the motor speed.
        @param  setpoint  Proportional gain value set by the user.
        @param  msr       The measured speed of the motor.
        @returns          The actuation level of the controller.
        """ 
#        add integral stuff if we want
        ## Setpoint variable for motor reference speed.
        self.setpoint = setpoint        
        ## Initialisation of measured variable in ticks
        self.msr = msr
        ## Error between the setpoint value and the measured value
        self.error = self.setpoint - self.msr
#         print(self.msr)
        
        if self.error > 0:
            self.act = int(self.Kp*abs(self.error))
        if self.error < 0:
            self.act = int(self.Kp*abs(self.error)*-1)
        
        if int(self.act) > int(self.sat_max):
            self.act = int(self.sat_max)
        if self.act < int(self.sat_min):
            self.act = int(self.sat_min)
            
#         print('act: ', self.act)
        return self.act
    
    
    def get_Kp(self):
        """!
        This method returns the set proportional gain value.
        @returns    The set proportional gain value.
        """ 
        return self.Kp
    
    def get_stepresponse(self, time_list, pos_list):
        """!
        This method prints step response data for the motor. 
        """ 
        ## Initialisation of the data array size
        array_size = int((3000/10)+1)
        
        ## Index variable
        n = 0
        while n <= int(array_size-1):
            print('{:},{:}'.format(time_list[n], pos_list[n]))
            n +=1
#            print(n)


#if __name__ == '__main__':
#        controller1 = ClosedLoop(50, 0, 0.1, 200, -200)
#        controller2 = ClosedLoop(50, 0, 0.1, 200, -200)
#        controller1.set_setpoint(1)
#        controller1.run()




