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

        while(part_input != '0'):
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
                # stop
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
                # right shoulder
                keyboardController.right_shoulder(4000)
            elif(part_input == '2'):
                keyboardController.right_shoulder(6000)
            elif(part_input == '3'):
                keyboardController.right_shoulder(8000)
            elif(part_input == '4'):
                # left shoulder
                keyboardController.left_shoulder(4000)
            elif(part_input == '5'):
                keyboardController.left_shoulder(6000)
            elif(part_input == '6'):
                keyboardController.left_shoulder(8000)
            elif(part_input == '!'):
                # right bicep
                keyboardController.right_bicep(4000)
            elif(part_input == '@'):
                keyboardController.right_bicep(6000)
            elif(part_input == '#'):
                keyboardController.right_bicep(8000)
            elif(part_input == '$'):
                # left bicep
                keyboardController.left_bicep(4000)
            elif(part_input == '%'):
                keyboardController.left_bicep(6000)
            elif(part_input == '^'):
                keyboardController.left_bicep(8000)
            elif(part_input == '7'):
                # right elbow
                keyboardController.right_elbow(4000)
            elif(part_input == '8'):
                keyboardController.right_elbow(6000)
            elif(part_input == '9'):
                keyboardController.right_elbow(8000)
            elif(part_input == '&'):
                # left elbow
                keyboardController.left_elbow(4000)
            elif(part_input == '*'):
                keyboardController.left_elbow(6000)
            elif(part_input == '('):
                keyboardController.left_elbow(8000)
            elif(part_input == 'c'):
                # right forearm
                keyboardController.right_forearm(4000)
            elif(part_input == 'v'):
                keyboardController.right_forearm(6000)
            elif(part_input == 'b'):
                keyboardController.right_forearm(8000)
            elif(part_input == 'C'):
                # left forearm
                keyboardController.left_forearm(4000)
            elif(part_input == 'V'):
                keyboardController.left_forearm(6000)
            elif(part_input == 'B'):
                keyboardController.left_forearm(8000)
            elif(part_input == 'u'):
                # right wrist
                keyboardController.right_wrist(4000)
            elif(part_input == 'i'):
                keyboardController.right_wrist(6000)
            elif(part_input == 'o'):
                keyboardController.right_wrist(8000)
            elif(part_input == 'U'):
                # left wrist
                keyboardController.left_wrist(4000)
            elif(part_input == 'I'):
                keyboardController.left_wrist(6000)
            elif(part_input == 'O'):
                keyboardController.left_wrist(8000)
            elif(part_input == 'r'):
                # right gripper
                keyboardController.right_gripper(4000)
            elif(part_input == 'r'):
                keyboardController.right_gripper(6000)
            elif(part_input == 'r'):
                keyboardController.right_gripper(8000)
            elif(part_input == 'r'):
                # left gripper
                keyboardController.left_gripper(4000)
            elif(part_input == 'r'):
                keyboardController.left_gripper(6000)
            elif(part_input == 'r'):
                keyboardController.left_gripper(8000)

                part_input = input("Command? ")

    if __name__ == "__main__":
        main()
