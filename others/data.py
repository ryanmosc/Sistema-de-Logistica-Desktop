import datetime
import time
def data():
    while True:
        agora = datetime.datetime.now()
        print(agora.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)  
data()
