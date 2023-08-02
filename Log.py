import time


def init():
    # noinspection PyGlobalUndefined
    global Log
    Log = open('Assets/Log.txt', 'a')
    Log.writelines(time.ctime() + '\n')


def log(text):
    # noinspection PyGlobalUndefined
    global Log
    Log.write(str(text) + '\n')


def close():
    # noinspection PyGlobalUndefined
    global Log
    Log.close()
