from tango import Tango
import time

def main():
    bot = Tango()
    
def arm_movement1(bot):
    # wave with right arm
    bot.right_shoulder(6400)
    timeAmount = 0.0
    while(timeAmount < 8.0):
        bot.right_bicep(4400)
        time.sleep(1.0)
        bot.right_bicep(7400)
        time.sleep(1.00)
        timeAmount = timeAmount + 2.0
    bot.right_bicep_reset()
    bot.right_shoulder_reset()
    
def arm_movement2(bot):
    # point with right arm
    bot.right_shoulder(6300)
    bot.right_gripper(7900)
    time.sleep(2.0)
    bot.right_gripper_reset()
    bot.right_shoulder_reset()
    
def arm_movement3(bot):
    # double thumbs up
    bot.right_shoulder(6300)
    bot.left_shoulder(6300)
    bot.right_elbow(6000)
    bot.left_elbow(6000)
    bot.right_forearm(6200)
    bot.left_forearm(6200)
    bot.right_gripper(8000)
    bot.left_gripper(8000)
    time.sleep(4.5)
    bot.right_gripper_reset()
    bot.left_gripper_reset()
    bot.right_forearm_reset()
    bot.left_forearm_reset()
    bot.right_elbow_reset()
    bot.left_elbow_reset()
    bot.right_shoulder_reset()
    bot.left_shoulder_reset()
    
def arm_movement4(bot):
    # cross arms
    bot.right_shoulder(6400)
    bot.left_shoulder(6400)
    bot.right_bicep(4000)
    bot.left_bicep(4000)
    
    time.sleep(4.5)
    
    bot.left_bicep_reset()
    bot.right_bicep_reset()
    bot.right_shoulder_reset()
    bot.left_shoulder_reset()
    
def arm_movement5(bot):
    # "beard stroke"
    bot.right_shoulder(7700)
    bot.right_bicep(4400)
    bot.right_elbow(7000)
    timeAmount = 0.0
    while(timeAmount < 10.1):
        bot.right_gripper(8000)
        time.sleep(1.0)
        bot.right_gripper(4000)
        time.sleep(1.0)
        timeAmount = timeAmount + 2.0
    bot.right_gripper_reset()
    bot.right_elbow_reset()
    bot.right_bicep_reset()
    bot.right_shoulder_reset()
    
def arm_movement6(bot):
    # arms slightly jostling side to side
    timeAmount = 0.0
    while(timeAmount < 20.1):
        bot.right_bicep(7200)
        bot.left_bicep(4600)
        time.sleep(2.0)
        bot.right_bicep(4600)
        bot.left_bicep(7200)
        time.sleep(2.0)
        timeAmount = timeAmount + 4.0
    bot.right_bicep_reset()
    bot.left_bicep_reset()
    
def arm_movement7(bot):
    # arms swinging forward and backward
    timeAmount = 0.0
    while(timeAmount < 20.1):
        bot.right_shoulder(6400)
        bot.left_shoulder_reset()
        time.sleep(2.0)
        bot.right_shoulder_reset()
        bot.left_shoulder(6400)
        time.sleep(2.0)
        timeAmount = timeAmount + 4.0
    bot.right_shoulder_reset()
    bot.left_shoulder_reset()
    
def arm_movement8(bot):
    # right arm kind of out, rist rotating nervously
    timeAmount = 0.0
    bot.right_shoulder(6200)
    while(timeAmount < 12.1):
        bot.right_wrist(4400)
        time.sleep(0.5)
        bot.right_wrist(6700)
        time.sleep(0.5)
        timeAmount = timeAmount + 1.0
    bot.right_wrist_reset()
    bot.right_shoulder_reset()
    
def arm_movement9(bot):
    # left arm version of nervous wrist
    timeAmount = 0.0
    bot.left_shoulder(6200)
    while(timeAmount < 12.1):
        bot.left_wrist(4400)
        time.sleep(0.5)
        bot.left_wrist(6700)
        time.sleep(5.0)
    bot.left_wrist_reset()
    bot.left_shoulder_reset()

def arm_movement10(bot):
    # something
    asdf = 2        
        
if __name__ == "__main__":
    main()