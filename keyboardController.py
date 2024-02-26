from tango import Tango

class KeyboardController:
    def __init__(self):
        # self.keyboardController = Tango()
        self.wheel_fb_val1 = 5900
        # self.wheel_lr_val = 5900
        # print("Testing entering into init")
        # self.main(self)

    def main():
        keyboardController = Tango()
        wheel_fb_val = 5900
        wheel_lr_val = 5900
        part_input = input("Command?")

        if(part_input == 'w'):
            # move forward
            while(wheel_fb_val <= 6500):
                wheel_fb_val += 10
                keyboardController.move_fb(wheel_fb_val)
        elif(part_input == 's'):
            # move backward
            while(wheel_fb_val >= 5300):
                wheel_fb_val -= 10
                keyboardController.move_fb(wheel_fb_val)
        elif(part_input == 'a'):
            # turn left
            while(wheel_lr_val >= 5300):
                wheel_lr_val -= 10
                keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == 'd'):
            # turn right
            while(wheel_lr_val >= 6500):
                wheel_lr_val += 10
                keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == 'wa' or part_input == 'aw'):
            # forward left
            while(wheel_fb_val <= 6500 and wheel_lr_val >= 5300):
                if(wheel_fb_val <= 6500):
                    wheel_fb_val += 10
                    keyboardController.move_fb(wheel_fb_val)
                if(wheel_lr_val >= 5300):
                    wheel_lr_val -= 10
                    keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == 'wd' or part_input == 'dw'):
            # forward right
            while(wheel_fb_val <= 6500 and wheel_lr_val <= 6500):
                if(wheel_fb_val <= 6500):
                    wheel_fb_val += 10
                    keyboardController.move_fb(wheel_fb_val)
                if(wheel_lr_val <= 6500):
                    wheel_lr_val += 10
                    keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == 'as' or part_input == 'sa'):
            # backward left
            while(wheel_fb_val >= 5300 and wheel_lr_val >= 5300):
                if(wheel_fb_val >= 5300):
                    wheel_fb_val -= 10
                    keyboardController.move_fb(wheel_fb_val)
                if(wheel_lr_val >= 5300):
                    wheel_lr_val -= 10
                    keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == 'ds' or part_input == 'sd'):
            # backward right
            while(wheel_fb_val >= 5300 and wheel_lr_val <= 6500):
                if(wheel_fb_val >= 5300):
                    wheel_fb_val -= 10
                    keyboardController.move_fb(wheel_fb_val)
                if(wheel_lr_val <= 6500):
                    wheel_lr_val += 10
                    keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == 'g'):
            # waist left
            keyboardController.turn_waist(5100)
        elif(part_input == 'h'):
            # waist right
            keyboardController.turn_waist(6700)
        elif(part_input == 'n'):
            # head left
            keyboardController.head_lr(4800)
        elif(part_input == 'm'):
            # head right
            keyboardController.head_lr(7000)
        elif(part_input == 'j'):
            # head down
            keyboardController.head_up_down(4800)
        elif(part_input == 'k'):
            # head up
            keyboardController.head_up_down(7000)
        elif(part_input == 'p'):
            while(wheel_fb_val != 5900 and wheel_lr_val != 5900):
                if(wheel_fb_val > 5900):
                    wheel_fb_val -= 10
                    if(wheel_fb_val == 5900):
                        keyboardController.stop_wheels_fb()
                    else:
                        keyboardController.move_fb(wheel_fb_val)
                if(wheel_fb_val < 5900):
                    wheel_fb_val += 10
                    if(wheel_fb_val == 5900):
                        keyboardController.stop_wheels_fb()
                    else:
                        keyboardController.move_fb(wheel_fb_val)
                if(wheel_lr_val > 5900):
                    wheel_lr_val -= 10
                    if(wheel_lr_val == 5900):
                        keyboardController.stop_wheels_lr()
                    else:
                        keyboardController.turn_lr(wheel_lr_val)
                if(wheel_lr_val < 5900):
                    wheel_lr_val += 10
                    if(wheel_lr_val == 5900):
                        keyboardController.stop_wheels_lr()
                    else:
                        keyboardController.turn_lr(wheel_lr_val)
        elif(part_input == '1'):
            keyboardController.right_shoulder(4000)
        elif(part_input == '2'):
            keyboardController.right_shoulder(6000)
        elif(part_input == '3'):
            keyboardController.right_shoulder(8000)
        elif(part_input == '4'):
            keyboardController.left_shoulder(4000)
        elif(part_input == '5'):
            keyboardController.left_shoulder(6000)
        elif(part_input == '6'):
            keyboardController.left_shoulder(8000)


        while (part_input > 0):
            if(part_input == 0):
                if(value_input > wheel_fb_val):
                    while(wheel_fb_val < value_input):
                        wheel_fb_val += 10
                        if(value_input == 5900):
                            keyboardController.stop_wheels_fb()
                        else: 
                            keyboardController.move_fb(wheel_fb_val)
                elif(value_input < wheel_fb_val):
                    while(wheel_fb_val > value_input):
                        wheel_fb_val -= 10
                        if(value_input == 5900):
                            keyboardController.stop_wheels_fb()
                        else: 
                            keyboardController.move_fb(wheel_fb_val)
            elif(part_input == 1):
                if(value_input > wheel_lr_val):
                    while(wheel_lr_val < value_input):
                        wheel_lr_val += 10
                        if(value_input == 5900):
                            keyboardController.stop_wheels_lr()
                        else: 
                            keyboardController.turn_lr(wheel_lr_val)
                elif(value_input < wheel_lr_val):
                    while(wheel_lr_val > value_input):
                        wheel_lr_val -= 10
                        if(value_input == 5900):
                            keyboardController.stop_wheels_lr()
                        else: 
                            keyboardController.turn_lr(wheel_lr_val)
            elif(part_input == 2):
                if(value_input == 5900):
                    keyboardController.center_waist()
                else:
                    keyboardController.turn_waist(value_input)
            elif(part_input == 3):
                if(value_input == 6000):
                    keyboardController.head_center_ud()
                else:
                    keyboardController.head_up_down(value_input)
            elif(part_input == 4):
                if(value_input == 5800):
                    keyboardController.head_center_lr()
                else:
                    keyboardController.head_lr(value_input)
            elif(part_input == 5):
                if(value_input == 4000):
                    keyboardController.right_shoulder_reset()
                else:
                    keyboardController.right_shoulder(value_input)
            elif(part_input == 6):
                if(value_input == 4000):
                    keyboardController.right_bicep_reset()
                else:
                    keyboardController.right_bicep(value_input)
            elif(part_input == 7):
                if(value_input == 4000):
                    keyboardController.right_elbow_reset()
                else:
                    keyboardController.right_elbow(value_input)
            elif(part_input == 8):
                if(value_input == 4000):
                    keyboardController.right_forearm_reset()
                else:
                    keyboardController.right_forearm(value_input)
            elif(part_input == 9):
                if(value_input == 4000):
                    keyboardController.right_wrist_reset()
                else:
                    keyboardController.right_wrist(value_input)
            elif(part_input == 10):
                if(value_input == 4000):
                    keyboardController.right_gripper_reset()
                else:
                    keyboardController.right_gripper(value_input)
            elif(part_input == 11):
                if(value_input == 4000):
                    keyboardController.left_shoulder_reset()
                else:
                    keyboardController.left_shoulder(value_input)
            elif(part_input == 12):
                if(value_input == 4000):
                    keyboardController.left_bicep_reset()
                else:
                    keyboardController.left_bicep(value_input)
            elif(part_input == 13):
                if(value_input == 4000):
                    keyboardController.left_elbow_reset()
                else:
                    keyboardController.left_elbow(value_input)
            elif(part_input == 14):
                if(value_input == 4000):
                    keyboardController.left_forearm_reset()
                else:
                    keyboardController.left_forearm(value_input)
            elif(part_input == 15):
                if(value_input == 4000):
                    keyboardController.left_wrist_reset()
                else:
                    keyboardController.left_wrist(value_input)
            elif(part_input == 16):
                if(value_input == 4000):
                    keyboardController.left_gripper_reset()
                else:
                    keyboardController.left_gripper(value_input)

            part_input = int(input("Please enter the part number: "))
            value_input = int(input("Please enter the value: "))

    if __name__ == "__main__":
        main()
