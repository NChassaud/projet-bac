import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

int1 = 27
int2 = 22
int3 = 5
BP = 6
ventilo = 20
MP1 = 12
MP2 = 16
Dout = 23
Din = 24
clk = 18
CS = 25


GPIO.setup (int1,  GPIO.IN)
GPIO.setup (int2,  GPIO.IN)
GPIO.setup (int3,  GPIO.IN)
GPIO.setup (BP, GPIO.IN)
GPIO.setup (ventilo, GPIO.OUT)
GPIO.setup (MP1, GPIO.OUT)
GPIO.setup (MP2, GPIO.OUT)
GPIO.setup (Dout, GPIO.IN)
GPIO.setup (Din, GPIO.OUT)
GPIO.setup (clk, GPIO.OUT)
GPIO.setup (CS, GPIO.OUT)


def MP_mode_refroidissement():
    print ("MP mode refroidissement")
    GPIO.output(MP2, GPIO.HIGH)
    GPIO.output(MP1, GPIO.LOW)
    
def MP_mode_chauffage():
    print ("MP mode chauffage")
    GPIO.output(MP1, GPIO.HIGH)
    GPIO.output(MP2, GPIO.LOW)

def MP_arret():
    print ("MP arret")
    GPIO.output(MP1, GPIO.LOW)
    GPIO.output(MP2, GPIO.LOW)
    
def Marche_ventilo():
    print ("Marche ventilo")
    GPIO.output(ventilo, GPIO.HIGH)
    
def Arret_ventilo():
    print ("Arret ventilo")
    GPIO.output(ventilo, GPIO.LOW)

def readspi(commandin):
    GPIO.output (CS, GPIO.HIGH)
    GPIO.output (clk, GPIO.LOW)
    GPIO.output (CS, GPIO.LOW)

    for i in range(5):
        if(commandin & 0x10 != 0):
            GPIO.output(Din,GPIO.HIGH)
        else :
            GPIO.output (Din, GPIO.LOW)
        commandin = commandin << 1
        GPIO.output(clk, GPIO.HIGH)
        GPIO.output(clk, GPIO.LOW)


    GPIO.output(clk, GPIO.HIGH)
    GPIO.output(clk, GPIO.LOW)
    GPIO.output(clk, GPIO.HIGH)


    bitout = 0

    for i in range(10):
        GPIO.output(clk, GPIO.LOW)
        GPIO.output(clk, GPIO.HIGH)
        bitout = bitout << 1
        if (GPIO.input(Dout) != 0):
            bitout = bitout | 0x01

    GPIO.output (CS, GPIO.HIGH)
    return (bitout)

def Mode_auto():
    print('>>> debut')
    commandin = 0x1E
    bitout=readspi(commandin)
    Vanalog = bitout * 3300 / (2**10)
    print ("bitout = ", bitout)
    print ("Vanalog =", Vanalog)
    time.sleep(1)

    if (Vanalog < 720):
        while (Vanalog < 730):
            MP_mode_chauffage()
            Marche_ventilo()
            commandin = 0x1E
            bitout=readspi(commandin)
            Vanalog = bitout * 3300 / (2**10)
            print ("bitout = ", bitout)
            print ("Vanalog =", Vanalog)
            time.sleep(1)
            
    if (Vanalog > 730 and Vanalog < 745):
        MP_arret()
        Arret_ventilo()
                
    if (Vanalog > 760):
        while (Vanalog > 745):
            MP_mode_refroidissement()
            Marche_ventilo()
            commandin = 0x1E
            bitout=readspi(commandin)
            Vanalog = bitout * 3300 / (2**10)
            print ("bitout = ", bitout)
            print ("Vanalog =", Vanalog)
            time.sleep(1)
            

                
def Mode_manuel():
    etatint2 = GPIO.input(int2)
    etatint3 = GPIO.input(int3)
    etatBP = GPIO.input(BP)
    if(etatint2 ==0 and etatint3 ==1):
        MP_mode_refroidissement()
        if (etatBP == 1):
            Marche_ventilo()
        else :
            Arret_ventilo()
    elif (etatint2 ==1 and etatint3 ==0):
        MP_mode_chauffage()
        if (etatBP == 1):
            Marche_ventilo()
        else :
            Arret_ventilo()
    else :
        MP_arret()
        Arret_ventilo()       

while True :             
    etatint1 = GPIO.input(int1)
    if(etatint1 == 0):       
        print ("Mode manuel")     
        Mode_manuel()
    else :                   
       print ("Mode auto")   
       Mode_auto()