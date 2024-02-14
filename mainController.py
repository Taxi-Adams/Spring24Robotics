from tango import tango;

class MainController:
    def __init__self():
        self.mainController = tango()

    def main(self):
        part_input = int(input("Please enter the part number: "))
        value_input = int(input("Please enter the value: "))
        while (part_input is not "stop" or value_input > 0):
            if(part_input == 0):
                if(value_input == 5900):
                    self.mainController.stop_wheels_fb(self.mainController)
                else:
                    self.mainController.move_forward(self.mainController, value_input)
            elif(part_input == 1):
                if(value_input == 5900):
                    self.mainController.stop_wheels_fb(self.mainController)
                else:
                    self.mainController.move_backward(self.mainController, value_input)
            elif(part_input == 2):
                if(self.value_input == 5900):
                    self.mainController.stop_wheels_lr(self.mainController)
                else:
                    self.mainController.turn_wheels_right(self.mainController, value_input)
            elif(part_input == 3):
                if(value_input == 5900):
                    self.mainController.stop_wheels_lr(self.mainController)
                else:
                    self.mainController.turn_wheels_left(self.mainController, value_input)
            part_input = int(input("Please enter the part number: "))
            value_input = int(input("Please enter the value: "))
