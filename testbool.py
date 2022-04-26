from concurrent.futures import thread
from AnalogSpi import AnalogSpi
from FireAlert import FireAlert
from ShadesControl import ShadesControl
from FireAlert import FireAlert
import time
def analog_sensors():
    
    analog_spi=AnalogSpi()
    shades_control=ShadesControl() #서보모터의 gpio 핀은 기본 22로 설정되어있음
    fire_alert=FireAlert()

    while True:
        
        pot_value0 = analog_spi.readadc(analog_spi.pot_channel0)
        pot_value1 = analog_spi.readadc(analog_spi.pot_channel1)
        pot_value2 = analog_spi.readadc(analog_spi.pot_channel2)

        # 불꽃감지
        fire_alert.run(pot_value0)
        # fire_thread=
        # 조도센서 블라인드 
        shades_control.run(pot_value1)
        print(pot_value0)
        # 물높이
        print(pot_value2)
        i=0
        if pot_value2>600 and i==0:
            print("hi")
            i+=1
            # time.sleep(295)
            
        time.sleep(2)

analog_sensors()