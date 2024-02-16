from tango import tango;

class MainController:
    def __init__self():
        self.mainController = tango()
        self.wheel_fb_val = 5900
        self.wheel_lr_val = 5900

    def main(self):
        part_input = int(input("Please enter the part number: "))
        value_input = int(input("Please enter the value: "))
        while (part_input is not "stop" or value_input > 0):
            if(part_input == 0):
                if(value_input > self.wheel_fb_val):
                    while(self.wheel_fb_val < value_input):
                        self.wheel_fb_val += 10
                        if(value_input == 5900):
                            self.mainController.stop_wheels_fb(self.mainController)
                        else: 
                            self.mainController.move_fb(self.mainController, self.wheel_fb_val)
                elif(value_input < self.wheel_fb_val):
                    while(self.wheel_fb_val > value_input):
                        self.wheel_fb_val -= 10
                        if(value_input == 5900):
                            self.mainController.stop_wheels_fb(self.mainController)
                        else: 
                            self.mainController.move_fb(self.mainController, self.wheel_fb_val)
            elif(part_input == 1):
                if(value_input > self.wheel_lr_val):
                    while(self.wheel_lr_val < value_input):
                        self.wheel_lr_val += 10
                        if(value_input == 5900):
                            self.mainController.stop_wheels_lr(self.mainController)
                        else: 
                            self.mainController.turn_lr(self.mainController, self.wheel_lr_val)
                elif(value_input < self.wheel_lr_val):
                    while(self.wheel_lr_val > value_input):
                        self.wheel_lr_val -= 10
                        if(value_input == 5900):
                            self.mainController.stop_wheels_lr(self.mainController)
                        else: 
                            self.mainController.turn_lr(self.mainController, self.wheel_lr_val)
            elif(part_input == 2):
                if(self.value_input == 5900):
                    self.mainController.center_waist(self.mainController)
                else:
                    self.mainController.turn_waist(self.mainController, value_input)
            elif(part_input == 3):
                if(value_input == 6000):
                    self.mainController.head_center_ud(self.mainController)
                else:
                    self.mainController.head_up_down(self.mainController, value_input)
            elif(part_input == 4):
                if(value_input == 5800):
                    self.mainController.head_center_lr(self.mainController)
                else:
                    self.mainController.head_lr(self.mainController, value_input)
            elif(part_input == 5):
                if(value_input == 4000):
                    self.mainController.right_shoulder_reset(self.mainController)
                else:
                    self.mainController.right_shoulder(self.mainController, value_input)
            elif(part_input == 6):
                if(value_input == 4000):
                    self.mainController.right_bicep_reset(self.mainController)
                else:
                    self.mainController.right_bicep(self.mainController, value_input)
            elif(part_input == 7):
                if(value_input == 4000):
                    self.mainController.right_elbow_reset(self.mainController)
                else:
                    self.mainController.right_elbow(self.mainController, value_input)
            elif(part_input == 8):
                if(value_input == 4000):
                    self.mainController.right_forearm_reset(self.mainController)
                else:
                    self.mainController.right_forearm(self.mainController, value_input)
            elif(part_input == 9):
                if(value_input == 4000):
                    self.mainController.right_wrist_reset(self.mainController)
                else:
                    self.mainController.right_wrist(self.mainController, value_input)
            elif(part_input == 10):
                if(value_input == 4000):
                    self.mainController.right_gripper_reset(self.mainController)
                else:
                    self.mainController.right_gripper(self.mainController, value_input)
            elif(part_input == 11):
                if(value_input == 4000):
                    self.mainController.left_shoulder_reset(self.mainController)
                else:
                    self.mainController.left_shoulder(self.mainController, value_input)
            elif(part_input == 12):
                if(value_input == 4000):
                    self.mainController.left_bicep_reset(self.mainController)
                else:
                    self.mainController.left_bicep(self.mainController, value_input)
            elif(part_input == 13):
                if(value_input == 4000):
                    self.mainController.left_elbow_reset(self.mainController)
                else:
                    self.mainController.left_elbow(self.mainController, value_input)
            elif(part_input == 14):
                if(value_input == 4000):
                    self.mainController.left_forearm_reset(self.mainController)
                else:
                    self.mainController.left_forearm(self.mainController, value_input)
            elif(part_input == 15):
                if(value_input == 4000):
                    self.mainController.left_wrist_reset(self.mainController)
                else:
                    self.mainController.left_wrist(self.mainController, value_input)
            elif(part_input == 16):
                if(value_input == 4000):
                    self.mainController.left_gripper_reset(self.mainController)
                else:
                    self.mainController.left_gripper(self.mainController, value_input)

            part_input = int(input("Please enter the part number: "))
            value_input = int(input("Please enter the value: "))
