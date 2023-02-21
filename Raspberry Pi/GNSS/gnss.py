import serial, sys, re
from time import sleep, time
from micropyGPS import MicropyGPS

NMEA_PORT='/dev/ttyUSB1'
AT_PORT='/dev/ttyUSB2'


def ddm2dec(dms_str):
    """Return decimal representation of DDM (degree decimal minutes)
    
    >>> ddm2dec("45° 17,896' N")
    48.8866111111F
    """
    
    dms_str = re.sub(r'\s', '', dms_str)
    
    sign = -1 if re.search('[swSW]', dms_str) else 1
    
    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute_decimal = numbers[1] 
    decimal_val = numbers[2] if len(numbers) > 2 else '0' 
    minute_decimal += "." + decimal_val

    return sign * (int(degree) + float(minute_decimal) / 60)


def initGNSS():
    sys.stdout.write('Init GNSS\n')
    with serial.Serial(AT_PORT, 115200, timeout=5, rtscts=True, dsrdtr=True) as ser:
        ser.write("AT+CGNSCFG=1\r\n".encode())
        sleep(1)
        ser.write("AT+CGNSPWR=1\r\n".encode())
        sleep(1)

try:
    sys.stdout.write('Started GNSS reader\n')
    reader = MicropyGPS(+1)
    initGNSS()
    try:
        last_time = time()
        diff = 0
        count = 1
        with serial.Serial(NMEA_PORT, 115200, timeout=5, rtscts=True, dsrdtr=True) as ser:
            while (diff < float(1) ):
                diff = time() - last_time
                print (f"Diferencia {diff}")
                data = ser.read().decode()
                reader.update(data)
                print(f"***** lectura {count}")
                count += 1 
                # print("UTC_Date={}, UTC_Time={}, lat={}, lng={}".format(reader.date_string(), reader.timestamp, ddm2dec(reader.latitude_string()), reader.longitude_string()))
                print("GNSS in degress lat={}, lng={}".format(format(ddm2dec(reader.latitude_string()),'f'),format(ddm2dec(reader.longitude_string()),'f')))
                # print("altitude={}, course={}, speed={}".format(reader.altitude, reader.course, reader.speed_string('kph')))
            # while True:
            #     # update
            data = ser.read().decode()
            reader.update(data)
            print("UTC_Date={}, UTC_Time={}, lat={}, lng={}".format(reader.date_string(), reader.timestamp, ddm2dec(reader.latitude_string()), reader.longitude_string()))
            print("GNSS in degress lat={}, lng={}".format(format(ddm2dec(reader.latitude_string()),'f'),format(ddm2dec(reader.longitude_string()),'f')))
            print("altitude={}, course={}, speed={}".format(reader.altitude, reader.course, reader.speed_string('kph')))
    except Exception as e:
        print("Error: {}".format(str(e)))
        sleep(1)
                
except KeyboardInterrupt:
    sys.stderr.write('Ctrl-C pressed, exiting GNSS reader\n')
