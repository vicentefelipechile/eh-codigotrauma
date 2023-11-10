import twilio.rest as Rest

class TwilioClass():
    # ===== Vars =====
    __Client: Rest.Client = None
    __AuthToken: str = "a33402080601e9418050598a40afab7f"
    AccountSid: str = "AC4a7fbac1089722ae0bf1fcff5effbc08"
    Number: str = "+12024107284"
    
    
    # ===== Constructor =====
    def __init__(self) -> None:
        self.__Client = Rest.Client(self.AccountSid, self.__AuthToken)
        
    
    # ===== Methods =====
    def SendMessage(self, number: str = None, message: str = None, method: str = "SMS") -> None:
        if number is None or message is None:
            return
        
        # Expresion regular para detectar si el numero es valido
        if number.find("+") == -1:
            return

        if method == "WSP":
            self.__Client.messages.create(
                body = message,
                from_ = f"whatsapp:+14155238886",
                to = f"whatsapp:{number}"
            )
        else:
            self.__Client.messages.create(
                body = message,
                from_ = self.Number,
                to = number
            )




if __name__ == "__main__":
    Twilio = TwilioClass()
    Twilio.SendMessage("+56990187115", "Hola, soy mrbeast y ando viajando a chile, si no me crees, mira por la ventana a tu derecha", "SMS")