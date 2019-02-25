import logging
import socket
import time

from udp import myudp
from pwm import mypwm
from i_o import myio
from lightoff import lightoff

if __name__ == "__main__":
    try:
        logging.basicConfig(level = logging.INFO)
        #set lightoff object
        lightoff = lightoff(26)

        myudp = myudp('192.168.137.20', 2000, 10)
        client = myudp.start()

        mypwm = mypwm(60, 26, 1000, 120, 10, 10, 1, 100)
        pwm = mypwm.start()

        myio = myio('192.168.137.20', 2000)
        myio.file_set()
        akku_id = ''

        while True:
            data_struct = myudp.udp_manipulation(client)
            mypwm.pwm_regelung(pwm, data_struct)

            for i in range(1,9):
                akku_id = akku_id + str(hex(data_struct[i]))[2:]
            logging.info("AkkuGruppe_ID: {}".format(akku_id))
            
            myio.io_manipulation(data_struct, client,akku_id)
            akku_id = ''

    except KeyboardInterrupt:
        logging.info('Regelung durch Keyboard abgebrochen!')
        pwm.stop()
        lightoff.start()
##    except socket.timeout:
##        logging.info('Keine Information aus SC mehr, Stoppen!')
##        pwm.stop()
##        lightoff.start()
