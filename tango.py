from maestro import Controller;
import time;

WHEELFORWARDBACKWARD = 0
WHEELTURN = 1
WAISTTURN = 2
HEADUPDOWN = 3
HEADTURN = 4
RIGHTARMSHOULDER = 5
RIGHTARMBICEP = 6
RIGHTARMELBOW = 7
RIGHTARMFOREARM = 8
RIGHTARMWRIST = 9
RIGHTARMGRIPPER = 10
LEFTARMSHOULDER = 11
LEFTARMBICEP = 12
LEFTARMELBOW = 13
LEFTARMFOREARM = 14
LEFTARMWRIST = 15
LEFTARMGRIPPER = 16


class Tango:
    def __init__(self):
        #self.turn = int(input("Please enter the value: "))
        self.tango = Controller()
        # Do we need anything else in the init function? I think we should be able to safely call methods by themselves

        #self.tango.setTarget(HEADTURN, self.turn) # example command
        #self.tango = Controller()
        #self.turn = 4500
        #self.tango.setTarget(HEADTURN, self.turn)

    # Potentially add safety checks so that if some command combination can cause issues such as tipping,
    # that combination won't be allowed

    def move_fb(self, val):
        if (val >= 4000 and val <= 8000):
            self.tango.setTarget(WHEELFORWARDBACKWARD, val)

    def stop_wheels_fb(self):
        # Add in a loop to slow down too
        self.tango.setTarget(WHEELFORWARDBACKWARD, 5900)

    def turn_lr(self, val):
        if (val >= 4000 and val <= 8000):
            self.tango.setTarget(WHEELTURN, val)

    def stop_wheels_lr(self):
        self.tango.setTarget(WHEELTURN, 5900)

    def turn_waist(self, val):
        if (val != 5900):
            self.tango.setTarget(WAISTTURN, val)

    def center_waist(self):
        self.tango.setTarget(WAISTTURN, 5900)

    def head_up_down(self, val):
        if(val >= 4000 and val <= 8000):
            self.tango.setTarget(HEADUPDOWN, val)

    def head_center_ud(self):
        self.tango.setTarget(HEADUPDOWN, 6000)

    def head_lr(self, val):
        if(val >= 4000 and val <= 8000):
            self.tango.setTarget(HEADTURN, val)

    def head_center_lr(self):
        self.tango.setTarget(HEADTURN, 5800)

    def right_shoulder(self, val):
        self.tango.setTarget(RIGHTARMSHOULDER, val)

    def right_shoulder_reset(self):
        self.tango.setTarget(RIGHTARMSHOULDER, 4000)

    def right_bicep(self, val):
        self.tango.setTarget(RIGHTARMBICEP, val)

    def right_bicep_reset(self):
        self.tango.setTarget(RIGHTARMBICEP, 4000)

    def right_elbow(self, val):
        self.tango.setTarget(RIGHTARMELBOW, val)

    def right_elbow_reset(self):
        self.tango.setTarget(RIGHTARMELBOW, 4000)

    def right_forearm(self, val):
        self.tango.setTarget(RIGHTARMFOREARM, val)

    def right_forearm_rest(self):
        self.tango.setTarget(RIGHTARMFOREARM, 4000)

    def right_wrist(self, val):
        self.tango.setTarget(RIGHTARMWRIST, val)

    def right_wrist_reset(self):
        self.tango.setTarget(RIGHTARMWRIST, 4000)

    def right_gripper(self, val):
        self.tango.setTarget(RIGHTARMGRIPPER, val)
        # Needs further modification: values closing/opening don't match, and don't want to grip something too hard. Can we get data for this?

    def right_gripper_reset(self):
        self.tango.setTarget(RIGHTARMGRIPPER, 4000)
        # Reset in this case makes more sense for completely open

    def left_shoulder(self, val):
        self.tango.setTarget(LEFTARMSHOULDER, val)

    def left_shoulder_reset(self):
        self.tango.setTarget(LEFTARMSHOULDER, 4000)

    def left_bicep(self, val):
        self.tango.setTarget(LEFTARMBICEP, val)

    def left_bicep_reset(self):
        self.tango.setTarget(LEFTARMBICEP, 4000)

    def left_elbow(self, val):
        self.tango.setTarget(LEFTARMELBOW, val)

    def left_elbow_reset(self):
        self.tango.setTarget(LEFTARMELBOW, 4000)

    def left_forearm(self, val):
        self.tango.setTarget(LEFTARMFOREARM, val)

    def left_forearm_reset(self):
        self.tango.setTarget(LEFTARMFOREARM, 4000)

    def left_wrist(self, val):
        self.tango.setTarget(LEFTARMWRIST, val)

    def left_wrist_reset(self):
        self.tango.setTarget(LEFTARMWRIST, 4000)

    def left_gripper(self, val):
        self.tango.setTarget(LEFTARMGRIPPER, val)
        # Needs further modification: values closing/opening don't match, and don't want to grip something too hard. Can we get data for this?

    def left_gripper_reset(self):
        self.tango.setTarget(LEFTARMGRIPPER, 4000)

    

t = Tango()
