import os
from time import sleep

def check_on():
    os.system('hciconfig>/home/pi/Desktop/check_status.txt')
    with open('/home/pi/Desktop/check_status.txt') as f:
        f = f.readlines()
        try:
            assert f[0].strip().split()[0] == 'hci0:'
        except:
            print(f[0].strip().split()[0], 'Error Message')
            raise AssertionError
        split = f[2].strip().split()
        if split[0] == 'UP':
            return True
        else:
            return False

def find_connections(filename):
    addresses = set()
    with open(filename) as f:
        f = f.readlines()
        for i in range(0, len(f)):
            if (i == 1):
                continue
            split = f[i].strip().split()
            addresses.add(split[0])

    return len(addresses)

def run_scan():
    try:
        if check_on() == False:
            os.system('sudo hciconfig hci0 up')
        print('Running scan..')
        os.system('sudo timeout -s INT 10s hcitool lescan > bluetooth_out.txt')  # prints out output to file
        signals_num = find_connections('bluetooth_out.txt')  # gives number of connections in area
        print("Outfile updated", signals_num)
        sleep(6)
        return signals_num

    except AssertionError:
        print('"hci0:" not found')
	
if __name__ == "__main__":
    run_scan()
