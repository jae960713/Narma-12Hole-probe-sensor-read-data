#-*- coding: cp949 -*-
import struct, binascii, requests, time, shutil, csv, requests
from serial import Serial

#linux 
ser = Serial('/dev/ttyUSB0', 230400)
#windows
#ser = Serial('COM4', 230400)
ser.reset_input_buffer()

#webserver url
url = "http://183.107.120.130:65433/get-12hole-data"

#save data in pi
'''
rtime = str(time.strftime("%y-%m-%d-%H-%M-%S"))
path = '/home/pi/'+ rtime +'-data.csv'
with open(path,'w',newline = '') as f:
    writer = csv.writer(f)
    categories = ["P1 ", "P2 ", "P3 ", "P4 ", "P5 ", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "Ps","Temp", "Velocity X", "Velocity Y", "Velocity Z"]
    writer.writerow(categories)
'''

while True:
    data = []
    realdata = []
    hexdata = []
    numofbyte = 1
    numofdata = 1000 
    buf = bytearray(numofdata * numofbyte)
    realdataarray = ['','','','','','','','','','','','','','','','','']
    pressure = []
    csvsave = []

    if ser.readable(): 
        ser.readinto(buf)
        for i in range(numofdata):
            bytedata = buf[(i * numofbyte): (numofbyte + i * numofbyte)] 
            value = bytedata.hex()
            data.append(value) 
               
        for j in range(1, numofdata):
            if data[j-1] == 'fe' and data[j] == 'fe':
                realdata.append(data[j])
                for k in range(j, j + 75):
                    realdata.append(data[k])
                break

        for l in range(6,74):
            if l <=9:
                realdataarray[0] = str(realdataarray[0]) + realdata[l]
            elif l >= 10 and l <=13:
                realdataarray[1] = str(realdataarray[1]) + realdata[l]
            elif l >=14 and l <=17:
                realdataarray[2] = str(realdataarray[2]) + realdata[l]          
            elif l >=18 and l <=21:
                realdataarray[3] = str(realdataarray[3]) + realdata[l]
            elif l >=22 and l <=25:
                realdataarray[4] = str(realdataarray[4]) + realdata[l]
            elif l >=26 and l <=29:
                realdataarray[5] = str(realdataarray[5]) + realdata[l]            
            elif l >=30 and l <=33:
                realdataarray[6] = str(realdataarray[6]) + realdata[l] 
            elif l >=34 and l <=37:
                realdataarray[7] = str(realdataarray[7]) + realdata[l]        
            elif l >=38 and l <=41:
                realdataarray[8] = str(realdataarray[8]) + realdata[l]
            elif l >=42 and l <=45:
                realdataarray[9] = str(realdataarray[9]) + realdata[l]
            elif l >=46 and l <=49:
                realdataarray[10] = str(realdataarray[10]) + realdata[l]
            elif l >=50 and l <=53:
                realdataarray[11] = str(realdataarray[11]) + realdata[l]
            elif l >=54 and l <=57:
                realdataarray[12] = str(realdataarray[12]) + realdata[l]
            elif l >=58 and l <=61:
                realdataarray[13] = str(realdataarray[13]) + realdata[l]
            elif l >=62 and l <=65:
                realdataarray[14] = str(realdataarray[14]) + realdata[l]
            elif l >=66 and l <=69:
                realdataarray[15] = str(realdataarray[15]) + realdata[l]
            elif l >=70 and l <=73:
                realdataarray[16] = str(realdataarray[16]) + realdata[l]

        for num in range(17):
            fdata = struct.unpack('<f',binascii.unhexlify(realdataarray[num]))[0]
            pressure.append(fdata)

        #append data in csv file
        '''csvsave.append(pressure)
        with open(path,'a',newline = '') as f:
            writer = csv.writer(f)
            for row in csvsave:
                writer.writerow(row)
        '''
        pressurejson = {"P1" : pressure[0],
                        "P2" : pressure[1],
                        "P3" : pressure[2],
                        "P4" : pressure[3],
                        "P5" : pressure[4],
                        "P6" : pressure[5],
                        "P7" : pressure[6],
                        "P8" : pressure[7],
                        "P9" : pressure[8],
                        "P10" : pressure[9],
                        "P11" : pressure[10],
                        "P12" : pressure[11],
                        "Ps" : pressure[12],
                        "Temperature" : pressure[13],
                        "Vx" : pressure[14],
                        "Vy" : pressure[15],
                        "Vz" : pressure[16],
                        "Time" : time.time() * 1000
        }
        print(pressurejson)
        try:
            response = requests.post(url, json = pressurejson)
            time.sleep(1)
            
        except requests.exceptions.ConnectionError:
            print("error")
            time.sleep(2)
            continue
        
f.close()