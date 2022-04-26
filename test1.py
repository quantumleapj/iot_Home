
from gpiozero import Buzzer
import time
bz=Buzzer(17)



for i in range(5):
  bz.toggle()
  time.sleep(1)