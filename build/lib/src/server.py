import logging
import sys

from src.util.connection import Server, Communication
from src.slide import Slide

buffer = {
    "move": "None",
    "note": "None",
}


# powerpoint slide control
def __slide_control(_slide):
    global buffer
    try:
        if buffer['move'] == 'next':
            _slide.next()
        elif buffer['move'] == 'prev':
            _slide.prev()
        note = _slide.get_note_shapes()

        buffer['note'] = note
    except (AttributeError, IndexError, EnvironmentError):
        logging.error("error occur in 'slide_control'")
        return -1


def __run(_slide, _serv):
    global buffer
    _serv.accept()
    while True:
        try:
            recv_data = Communication.receive_data(_serv)
            buffer['move'] = recv_data['move']
            if __slide_control(_slide) == -1:
                return -1
            Communication.send_data(_serv, buffer)
        except ConnectionError:
            logging.warning('client connection closed')
            return 0

def run(ip, port, is_enable_show):
    serv = Server()
    slide = Slide()
    if is_enable_show == True:
        slide.show_on()
    # you have to add the argv

    serv.init(ip, port)
    while True:
        if __run(slide, serv) == -1:
            slide.show_off()
            sys.exit()
