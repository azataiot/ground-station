#!/usr/bin/env python3
"""The python3 version of the azt UniSat shell"""
import os
import subprocess
import sys
import time
import struct
import logging
import click
import serial
from binascii import b2a_hex, a2b_hex

writepath = os.path.join(os.getcwd(), 'log.txt')
logging.basicConfig(filename=writepath,
                    level=logging.DEBUG,
                    filemode='a' if os.path.exists(writepath) else 'w',
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

acp = serial.Serial()
acp.baudrate = 38400
new_data = False

TEXT_AZATAI = r""" azt::ver 0.7.9 beta
  _    _       _  _____       _
 | |  | |     (_)/ ____|     | |
 | |  | |_ __  _| (___   __ _| |_
 | |  | | '_ \| |\___ \ / _` | __|
 | |__| | | | | |____) | (_| | |_
  \____/|_| |_|_|_____/ \__,_|\__|
"""


def main():
    logging.info("UniSat Logging Start")
    acp.port = click.prompt("port:", default='/dev/cu.usbserial-0001')
    try:
        acp.open()
    except:
        msg = "Can't open serial. plz check the serial device or the serial port."
        logging.error(msg);
        print(msg)
        sys.exit(1)
    while True:
        try:
            pass
        except:
            pass
        # receiving
        package = []
        while acp.in_waiting > 0:
            c = acp.read()
            hex_byte = b2a_hex(c)
            package.append(hex_byte)
            print(hex_byte, end=' ')
        if len(package) > 5:
            logging.info(package)
            print('\n')
            msg = "Valid Angime:"
            logging.info(msg)
            print(msg)
            # time
            time_now = time.localtime()  # get struct_time
            time_string = time.strftime("%m-%d-%Y-%H-%M-%S", time_now)
            #
            received_time = time_string  # get current time on PC
            content = ''

            if package[0] in [b'2d', b'cd', b'3d']:
                if package[0] == b'2d':
                    sender = 'UniSat->TRX :: Transmission Board'
                elif package[0] == b'cd':
                    sender = "UniSat->GS :: Ground Station"
                else:
                    sender = "UniSat->TOP :: TOP Board"
                length = int(package[2], 16)
                print(f"from: {sender}")
                print(f"received_time: {received_time}")
                print(f"payload length: {length}")
                print(f"payload: {package[2:-2]}")
                logging.info(sender)
                logging.info(received_time)
                logging.info(length)
                logging.info(package[2:-2])
                if package[3] == b'02':
                    print('')
                    msg = f"CMD '02' Таймштамп UTC+0: {package[4:8]}"
                    print(msg)
                    logging.info(msg)
                    tmp_p = package[4:8]
                    tmp_p.reverse()
                    tmp = b''.join(tmp_p)
                    time_stamp = int(tmp, 16)
                    msg = f"UTC Time: {time_stamp}"
                    print(msg)
                    logging.info(msg)

                if package[8] == b'0a':
                    print('')
                    # latitude
                    tmp_p_la = package[9:13]
                    tmp_p_la.reverse()
                    tmp_la = b''.join(tmp_p_la)
                    latitude = struct.unpack('!f', bytes.fromhex(tmp_la.decode()))[0]
                    # longitude
                    tmp_p_lo = package[13:17]
                    tmp_p_lo.reverse()
                    tmp_lo = b''.join(tmp_p_lo)
                    longitude = struct.unpack('!f', bytes.fromhex(tmp_lo.decode()))[0]
                    # height
                    tmp_p_h = package[17:19]
                    tmp_p_h.reverse()
                    tmp_h = b''.join(tmp_p_h)
                    height = int(tmp_h, 16)
                    # speed
                    tmp_p_s = package[19:21]
                    tmp_p_s.reverse()
                    tmp_s = b''.join(tmp_p_s)
                    speed = int(tmp_s, 16)

                    # direction
                    tmp_p_d = package[21:23]
                    tmp_p_d.reverse()
                    tmp_d = b''.join(tmp_p_d)
                    direction = int(tmp_d, 16)

                    print(f"Latitude: {latitude}")
                    print(f"Longitude Value: {longitude}")
                    print(f"Height Value: {height} m")
                    print(f"Speed Value: {speed} m/s")
                    print(f"Direction Value: {direction}")
                    print('')
                    logging.info(f"{latitude}, {longitude}, {height}, {speed}, {direction}")


if __name__ == '__main__':
    print(TEXT_AZATAI)
    print("Type 'exit' or Ctrl+C to quit.")
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        acp.close()
        logging.error("\n\nUniSat: bye~\n")
        print("\n\nUniSat: bye~\n")
        sys.exit(0)
