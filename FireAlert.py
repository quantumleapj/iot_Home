
# 평상시 1015~1020
# 라이터 가져가면 900정도

# 실내온도가 계속 변할텐데 그럼 아날로그값도 변할까? 값을 어떻게 지정해야 할까?
#  = 장비시작후 계속 평균값을 저장하다가 평균값보다 값이 많이 벌어지면 알림띄우기로 하자 

# 0띄워지는 경우도 있는데 이경우는 어쩔까?
# = 0뜨는건 값에서 제외

# 장비시작한지 얼마 안됐을때는 라이터가 꺼질때도 값이 많이 변할수있다
# 평균값보다 센서값이 적은 경우만 조건문에 넣자 

# 불이 계속 나있을 경우 평균값이 점점 낮아져서 장비가 정상작동하는데도 꺼질수있다? 
# = 위험알림때는 평균값 계산에서 제외 

# 고작 불꽃감지에 계산너무많이쓰나..?그치만 정수 계산 몇번인데 괜찮지않을까 아니그래도 while문에넣으니까 계속할텐데.. 음..

import sys
from gpiozero import Buzzer
import time
import requests
import json
# from homeiot import send_talk_alert
# bz=Buzzer(17)

key_path='/home/pi/workspace/iot_Home-2/iot_server/access_token.txt'

def send_talk_alert(text,mobile_web_url,web_url=None):
    if not web_url:
        web_url=mobile_web_url
    with open(key_path,'r') as f:
        token=f.read()

    talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    header={"Authorization":f"Bearer {token}"}

    text_template={
        'object_type':'text',
        'text':text,
        # 'image_url': "http://mud-kage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
        'link':{
            'web_url':web_url,
            'mobile_web_url':mobile_web_url
            }
    }
    print(text_template)
    payload={'template_object':json.dumps(text_template)}
    res=requests.post(talk_url,data=payload,headers=header)
    return res.json()

class FireAlert:
  def __init__(self,buzzer_pin=17):
    
    self.average=0

    self.sum=0
    self.count=0
    self.danger_count =0
    self.bz=Buzzer(buzzer_pin)
    

  def run(self, sensor_value):
    # while문에 넣을것

    # 값이 0이면 값이 튀었다고 판단하고 아무것도 하지 않는다 
    if sensor_value==0:
      return

    difference =self.average - sensor_value 

    # if difference > 3:
    if self.average > 3:
      self.danger_count +=1

    else:
      # 위험값이 아닌거 같으면 부저 끈다
      if self.bz.is_active:
        self.bz.off()
      self.danger_count =0
      
      # 위험값이 아닌거 같으면 평균에 포함
      self.cal_average(sensor_value)

    if self.danger_count >2 : 
      self.send_alert()
    print(f"불꽃감지 평균값:{self.average}, 센서값: {sensor_value}, 위험값 카운트 {self.danger_count} ")


  def cal_average(self,sensor_value):
    #평균값 계산 함수 

    if self.sum +1024 >sys.maxsize:
      # 만약 합의 크기가 정수 제한값을 넘을경우 
      self.sum=self.average*100
      self.count=100

    else:
      self.sum +=sensor_value
      self.count+=1

    self.average = self.sum/self.count

  def send_alert(self):
    print("!!!!!!!불꽃감지 알림작동!!!!!!!!")
    i=0
    if i<3:
      res=send_talk_alert('화재발생!!!!','http://192.168.219.106:8000/mjpeg/?mode=stream')#라파 서버주소
      i+=1
    # 라파 주소
    if res.get('result_code')!=0:
        print("전송 실패",res['msg'],res['code'])
    for i in range(6):
      self.bz.toggle()
      time.sleep(1)
    if not self.bz.is_active:
      self.bz.on()
      
      





