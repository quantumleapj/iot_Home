from AnalogSpi import AnalogSpi
import RPi.GPIO as GPIO
from gpiozero import AngularServo
import time
from datetime import datetime
from FireAlert import FireAlert

# 오전 창문열고 오후면 창문닫는다
# 아침 6시~ 저녁 8시 열고 나중 닫음 

# ============
# 천으로가림 1000
# 어두운 방 800
# 밝은방 440~550
# 손전등 200~100

# ===========
# 낮에는 조도센서 값이 450 이상이 될때까지 
# 시간 딜레이를 줘가면서 도어모터를 여는쪽으로 작동 
# 값이 450가 안되더라도 도어모터 끝이면 그만작동

# 밤에는 if값이 조도센서값 1000 이하인 거, 도어모터가 닫히는 방향인 거 외에 동일한 작동 

angle_blind_test=AngularServo(19, min_angle=-90, max_angle=90, min_pulse_width=0.0004, max_pulse_width=0.0024)
class ShadesControl:
  def __init__(self):
    
    
    angle_blind_test.value=self.dc
    
    self.dc = 7.5
    


  def is_night(self):
    hour=datetime.now().hour
    if hour < 6 or hour>19 :
      return True
    else:
      return False

  def run(self,sensor_value):
    # while문 안에 넣을것
    try:
      if(self.is_night()):
        #밤일때
        if sensor_value<1000:
          print("is_night= true, 조도센서 1000보다 큼")
          try:
            if self.dc < 12.5 :
              
              self.dc += 0.1
              angle_blind_test.value=self.dc
            else:
                self.dc+=0
                angle_blind_test.value-self.dc
          except KeyboardInterrupt:
            self.dc+=0
            angle_blind_test.value-self.dc
        else:
            self.dc+=0
            angle_blind_test.value-self.dc
      else:
        #낮일때
        if sensor_value>450:
          print("is_night= false, 조도센서 450보다 작음")
          try:
            if self.dc > 2.5 :
              
              self.dc -= 0.1
              angle_blind_test.value=self.dc
            else:
                self.dc+=0
                angle_blind_test.value-self.dc

          except KeyboardInterrupt:
            self.dc+=0
            angle_blind_test.value-self.dc    
        else:
            self.dc+=0
            angle_blind_test.value-self.dc

    except KeyboardInterrupt:
        self.dc+=0
        angle_blind_test.value-self.dc
