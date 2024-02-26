from tango import Tango

bot = Tango()

def find(data: str) -> None:
    servoVal = int(data['value']) * 40 + 4000
    match data:
        case ['WHEELFORWARDBACKWARD', 'WHEELTURN']: pass
        case "WAISTTURN": bot.turn_waist(servoVal)
        case "HEADUPDOWN": bot.head_up_down(servoVal)
        case "HEADTURN": bot.head_lr(servoVal)
