# from fabric import *
import sys

from fabric2 import Connection


def train(c):
    with c.cd('/home/ubuntu/handwriting/form_ai'):
        with c.prefix('source ~/anaconda3/bin/activate pytorch_p36'):
            c.run('python form_ai.py')


def uptime(c):
    c.run('uptime', pty=True)


def wakeup(c):
    c.run('caffeinate -u -t 1')
    # import time
    # time.sleep(10)


def inputWord(c, word):
    print(f"typing {word}")
    c.run(f'osascript -e \'tell application "system events" to keystroke "{word}"\' ', )


if __name__ == '__main__':
    with Connection(host=sys.argv[1], user='ubuntu',
                    connect_kwargs={"key_filename": ['/home/lxq/tensorflow.pem']}) as c:
        train(c)
    # with Connection(host=sys.argv[1]) as c:
    #     c.run('uptime')
    #     wakeup(c)
    #     inputWord(c, "passw0rd")
