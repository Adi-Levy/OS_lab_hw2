#!/usr/bin/python

import os
import errno
import pyHighscore
import time

def spend_time():
    for i in range(5):
        # This spends about 1s
        for j in xrange(15000000):
            pass

def test1():
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0:
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        # Spend time, should block the parent for about 5s
        spend_time()
        os._exit(0)
    time.sleep(0.1) # force de-scheduling of the parent
    e = time.time()
    os.wait()
    elapsed = e - s
    assert (elapsed > 3), "A process with no league cannot run while a playing process is running"

if __name__ == "__main__":
    test1()
