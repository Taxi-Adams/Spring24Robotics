#from tango import Tango
#
#bot = Tango()

def find(data: str) -> None:
    try:
        servoVal = int(data['value']) * 40 + 4000
    except: print(data)
    match data['servo']:
        case ['WHEELFORWARDBACKWARD', 'WHEELTURN']: 
        # Foward/ Backward
            if int(data['value'][1]) == 0:
                #bot.stop_wheels_fb()
                print(int(data['value'][1]))
            # Backwards
            elif int(data['value'][1]) > 0:
                servoVal = int(data['value'][1]) * (18.75) + 5900
                print(int(servoVal))
            # Forwards
            elif int(data['value'][1]) < 0:
                servoVal = 5900 - int(data['value'][1]) * (-17)
                print(servoVal)

            #Left/ Right
            if int(data['value'][0]) == 0:
                #bot.stop_wheels_fb()
                print(int(data['value'][0]))
            # Right
            elif int(data['value'][0]) > 0:
                servoVal = int(data['value'][0]) * (18.75) + 5900
                print(int(servoVal)) 
            # Left
            elif int(data['value'][0]) < 0:
                servoVal = 5900 - int(data['value'][0]) * (-17)
                print(servoVal)

        case "WAISTTURN": print(servoVal)
        case "HEADUPDOWN": print(servoVal)
        case "HEADTURN": print(servoVal)

def main() -> None:
    #bot = Tango()
    #bot.stop_wheels_fb()
    #bot.stop_wheels_lr()
    print(1)

if __name__ == "__main__":
    main()