import logging
import os, copy
import threading
import tkinter, tkinter.font

from time import sleep
from pynput.keyboard import Key, Listener
from src.util.connection import Client, Communication

__buffer = {
    'clicked': False,
    'accept': True,
    'move': "None",
    'note': "None",
    'page': '',
}
___client = Client()
__prev = {}


def __on_press(key):
    global ___client, __buffer
    logging.info('{} pressed...'.format(key))
    logging.info('clicked ==> {} and accept ==> {}'.format(__buffer['clicked'], __buffer['accept']))
    if key == Key.esc:
        logging.info('close the application')
        os._exit(0)
    if not __buffer['clicked'] and __buffer['accept']:
        if key == Key.right:
            __buffer['move'] = 'next'
            __buffer['clicked'] = True
        elif key == Key.left:
            __buffer['move'] = 'prev'
            __buffer['clicked'] = True
        # valid input then wait the server signal
        if __buffer['clicked']:
            __buffer['accept'] = False
            __run(___client, __buffer)


def __on_release(key):
    global __buffer
    logging.info('{} released...'.format(key))
    __buffer['clicked'] = False


def __run(_client, _buffer):
    try:
        _temp = {
            'clicked': _buffer['clicked'],
            'accept': _buffer['accept'],
            'move': _buffer['move']
        }
        Communication.send_data(_client, _temp)
        recv_data = Communication.receive_data(_client)
        _buffer['note'] = recv_data['note']
        _buffer['note'] = _buffer['note'].replace("\r", "\r\n")
        _buffer['accept'] = True
    except ConnectionError:
        logging.error('server connection closed')
        os._exit(-1)

def __window_destroy():
    logging.info("destroy windows")
    os._exit(0)

def __data_update(_window, _text):
    global __buffer, __prev
    hasNote = __buffer['note'] == "None"
    isChange = __buffer != __prev
    if hasNote or not isChange:
        return -1
    data = "[[ script ]] \n\n"+__buffer['note']
    _text.delete('1.0', tkinter.END)
    _text.insert(tkinter.END, data)
    __prev = copy.deepcopy(__buffer)
    return 0

def __my_window():
    window = tkinter.Tk()
    window.protocol("WM_DELETE_WINDOW", __window_destroy)
    window.title("pptx-client.py")
    window.geometry("1600x900")
    scroll = tkinter.Scrollbar(window)
    # if you want to change the font family then change the font family value
    font = tkinter.font.Font(family="맑은 고딕", size=12)
    text = tkinter.Text(window, height=50, width=75, font=font)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    __data_update(window, text)
    while True:
        sleep(1/24)
        __data_update(window, text)
        window.update()

def run(ip, port):
    try:
        ___client.init(ip, port)
        __run(___client, __buffer)
        wThread = threading.Thread(target=__my_window)
        wThread.start()
        with Listener(on_press=__on_press,
                      on_release=__on_release) as listener:
            listener.join()
    except Exception:
        logging.error("Unexpected ended occur")
        os._exit(-1)
