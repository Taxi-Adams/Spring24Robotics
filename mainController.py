from tango import Tango

class MainController:
    def __init__(self):
        # self.mainController = Tango()
        self.wheel_fb_val1 = 5900
        # self.wheel_lr_val = 5900
        # print("Testing entering into init")
        # self.main(self)

    def main():
        mainController = Tango()
        wheel_fb_val = 5900
        wheel_lr_val = 5900
        part_input = int(input("Please enter the part number: "))
        value_input = int(input("Please enter the value: "))
        while (part_input > 0):
            if(part_input == 0):
                if(value_input > wheel_fb_val):
                    while(wheel_fb_val < value_input):
                        wheel_fb_val += 10
                        if(value_input == 5900):
                            mainController.stop_wheels_fb()
                        else: 
                            mainController.move_fb(wheel_fb_val)
                elif(value_input < wheel_fb_val):
                    while(wheel_fb_val > value_input):
                        wheel_fb_val -= 10
                        if(value_input == 5900):
                            mainController.stop_wheels_fb()
                        else: 
                            mainController.move_fb(wheel_fb_val)
            elif(part_input == 1):
                if(value_input > wheel_lr_val):
                    while(wheel_lr_val < value_input):
                        wheel_lr_val += 10
                        if(value_input == 5900):
                            mainController.stop_wheels_lr()
                        else: 
                            mainController.turn_lr(wheel_lr_val)
                elif(value_input < wheel_lr_val):
                    while(wheel_lr_val > value_input):
                        wheel_lr_val -= 10
                        if(value_input == 5900):
                            mainController.stop_wheels_lr()
                        else: 
                            mainController.turn_lr(wheel_lr_val)
            elif(part_input == 2):
                if(value_input == 5900):
                    mainController.center_waist()
                else:
                    mainController.turn_waist(value_input)
            elif(part_input == 3):
                if(value_input == 6000):
                    mainController.head_center_ud()
                else:
                    mainController.head_up_down(value_input)
            elif(part_input == 4):
                if(value_input == 5800):
                    mainController.head_center_lr()
                else:
                    mainController.head_lr(value_input)
            elif(part_input == 5):
                if(value_input == 4000):
                    mainController.right_shoulder_reset()
                else:
                    mainController.right_shoulder(value_input)
            elif(part_input == 6):
                if(value_input == 4000):
                    mainController.right_bicep_reset()
                else:
                    mainController.right_bicep(value_input)
            elif(part_input == 7):
                if(value_input == 4000):
                    mainController.right_elbow_reset()
                else:
                    mainController.right_elbow(value_input)
            elif(part_input == 8):
                if(value_input == 4000):
                    mainController.right_forearm_reset()
                else:
                    mainController.right_forearm(value_input)
            elif(part_input == 9):
                if(value_input == 4000):
                    mainController.right_wrist_reset()
                else:
                    mainController.right_wrist(value_input)
            elif(part_input == 10):
                if(value_input == 4000):
                    mainController.right_gripper_reset()
                else:
                    mainController.right_gripper(value_input)
            elif(part_input == 11):
                if(value_input == 4000):
                    mainController.left_shoulder_reset()
                else:
                    mainController.left_shoulder(value_input)
            elif(part_input == 12):
                if(value_input == 4000):
                    mainController.left_bicep_reset()
                else:
                    mainController.left_bicep(value_input)
            elif(part_input == 13):
                if(value_input == 4000):
                    mainController.left_elbow_reset()
                else:
                    mainController.left_elbow(value_input)
            elif(part_input == 14):
                if(value_input == 4000):
                    mainController.left_forearm_reset()
                else:
                    mainController.left_forearm(value_input)
            elif(part_input == 15):
                if(value_input == 4000):
                    mainController.left_wrist_reset()
                else:
                    mainController.left_wrist(value_input)
            elif(part_input == 16):
                if(value_input == 4000):
                    mainController.left_gripper_reset()
                else:
                    mainController.left_gripper(value_input)

            part_input = int(input("Please enter the part number: "))
            value_input = int(input("Please enter the value: "))

    if __name__ == "__main__":
        main()
