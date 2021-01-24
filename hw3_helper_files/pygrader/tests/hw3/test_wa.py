#!/usr/bin/python

import os
import errno
import pyHighscore
import time


def spend_time(n):
    for i in range(n):
        # This spends about 1s
        for j in xrange(15000000):
            pass

"""
Shirili Shelef, Gabi Mannes.
"""

def test1(): # one proccces with league blocks everyone. (father sleeping)
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0:
        pyHighscore.highscore_chleague(0)
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    time.sleep(1) # force de-scheduling of the parent
    e = time.time()
    os.wait()
    elapsed = e - s
    print(elapsed)
    assert (elapsed > 3), "A process with no league cannot run while a playing process is running"
    
def test2(): # one proccces with league blocks everyone .without sleeping. (both proccess are running)
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0:
        pyHighscore.highscore_chleague(0)
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    spend_time(1)
    e = time.time()
    os.wait()
    elapsed = e - s
    print(elapsed)
    assert (elapsed > 3), "A process with no league cannot run while a playing process is running"    
    
def test3(): # both has league, but son has more boards. father sleeping.
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        b = time.time()
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    time.sleep(2) # force de-scheduling of the parent
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed > 3), "A process with league and board should block other process"    

def test4(): # both has league, but son has more boards. father is not sleeping.
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    spend_time(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed > 3), "A sleeping process with league cannot block other process"    
    
def test5():# son with board but high nice. shouldnt block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        os.nice(5)
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    spend_time(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 3), "A process with league and high nice shouldnt block"    
    
def test6():# son without board but low nice. should block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    pyHighscore.highscore_add('/board', 1)
    pyHighscore.highscore_add('/board1', 1)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board1', 1)
        os.nice(-5)
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    time.sleep(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed > 3), "A process with league and high nice shouldnt block"        
    
def test7():# son with -17 nice, 5 boards. father with -20 nice. shouldnt block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        spend_time(1)
        pyHighscore.highscore_chleague(0)
        os.nice(-17)
        pyHighscore.highscore_add('/board', 1)
        pyHighscore.highscore_add('/board2', 1)
        pyHighscore.highscore_add('/board3', 1)
        pyHighscore.highscore_add('/board14', 1)
        pyHighscore.highscore_add('/board5', 1)
        # Spend time, should block the parent for about 5s
        spend_time(7)
        os._exit(0)
    os.nice(-20)
    time.sleep(4)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 5), "A process with league and high nice shouldnt block"        
    
def test8():# son creates league and destroy it. shouldnt block
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        pyHighscore.highscore_chleague(-1)
        # Spend time, should block the parent for about 5s
        spend_time(5)
        os._exit(0)
    time.sleep(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 3), "A process with league and high nice shouldnt block"        

def test9():# son creates league and go to sleep. shouldnt block
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        time.sleep(2)
        # Spend time, should block the parent for about 5s
        spend_time(4)
        os._exit(0)
    time.sleep(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 3), "A process with league and sleep shouldnt block"        
    
def test10():# son has no league. shouldnt block
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        # Spend time, should block the parent for about 5s
        spend_time(4)
        os._exit(0)
    time.sleep(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 3), "A process with league and sleep shouldnt block"        
    
def test11():# son and father has league. shouldnt block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        # Spend time, should block the parent for about 5s
        spend_time(4)
        os._exit(0)
    time.sleep(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 3), "A process with league and sleep shouldnt block"        
    
def test12():# son and father has league and board. shouldnt block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    pyHighscore.highscore_add('/board', 1)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        # Spend time, should block the parent for about 5s
        spend_time(4)
        os._exit(0)
    time.sleep(1)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 3), "A process with league and sleep shouldnt block"        

def test13():# son with 25 boards. father with -20 nice. shouldnt block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        spend_time(1)
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        pyHighscore.highscore_add('/board2', 1)
        pyHighscore.highscore_add('/board3', 1)
        pyHighscore.highscore_add('/board4', 1)
        pyHighscore.highscore_add('/board5', 1)
        pyHighscore.highscore_add('/board6', 1)
        pyHighscore.highscore_add('/board7', 1)
        pyHighscore.highscore_add('/board8', 1)
        pyHighscore.highscore_add('/board9', 1)
        pyHighscore.highscore_add('/board10', 1)
        pyHighscore.highscore_add('/board11', 1)
        pyHighscore.highscore_add('/board12', 1)
        pyHighscore.highscore_add('/board13', 1)
        pyHighscore.highscore_add('/board14', 1)
        pyHighscore.highscore_add('/board15', 1)
        pyHighscore.highscore_add('/board16', 1)
        pyHighscore.highscore_add('/board17', 1)
        pyHighscore.highscore_add('/board18', 1)
        pyHighscore.highscore_add('/board19', 1)
        pyHighscore.highscore_add('/board20', 1)
        pyHighscore.highscore_add('/board21', 1)
        pyHighscore.highscore_add('/board22', 1)
        pyHighscore.highscore_add('/board23', 1)
        pyHighscore.highscore_add('/board24', 1)
        pyHighscore.highscore_add('/board25', 1)
        # Spend time, should block the parent for about 5s
        spend_time(7)
        os._exit(0)
    os.nice(-20)
    time.sleep(4)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed < 5), "A process with league and high nice shouldnt block"        
    
def test14():# son creates a league and has board. Father join the league. son shouldnt block
    """ Verify a process with a league blocks other processes """
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        time.sleep(2)
        # Spend time, should block the parent for about 5s
        spend_time(10)
        b = time.time()
        print('son - ', b - s)
        os._exit(0)
    time.sleep(1)
    pyHighscore.highscore_chleague(cpid)
    spend_time(2)
    e = time.time()
    elapsed = e - s
    print('father - ', elapsed)
    os.wait()
    assert (elapsed < 9), "A process with league and sleep shouldnt block"        
 
def test15():# son with 25 boards +10 nice. father with -13 nice sleeping. should block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        pyHighscore.highscore_add('/board2', 1)
        pyHighscore.highscore_add('/board3', 1)
        pyHighscore.highscore_add('/board4', 1)
        pyHighscore.highscore_add('/board5', 1)
        pyHighscore.highscore_add('/board6', 1)
        pyHighscore.highscore_add('/board7', 1)
        pyHighscore.highscore_add('/board8', 1)
        pyHighscore.highscore_add('/board9', 1)
        pyHighscore.highscore_add('/board10', 1)
        pyHighscore.highscore_add('/board11', 1)
        pyHighscore.highscore_add('/board12', 1)
        pyHighscore.highscore_add('/board13', 1)
        pyHighscore.highscore_add('/board14', 1)
        pyHighscore.highscore_add('/board15', 1)
        pyHighscore.highscore_add('/board16', 1)
        pyHighscore.highscore_add('/board17', 1)
        pyHighscore.highscore_add('/board18', 1)
        pyHighscore.highscore_add('/board19', 1)
        pyHighscore.highscore_add('/board20', 1)
        pyHighscore.highscore_add('/board21', 1)
        pyHighscore.highscore_add('/board22', 1)
        pyHighscore.highscore_add('/board23', 1)
        pyHighscore.highscore_add('/board24', 1)
        pyHighscore.highscore_add('/board25', 1)
        os.nice(10)
        time.sleep(1)
        # Spend time, should block the parent for about 5s
        spend_time(7)
        os._exit(0)
    time.sleep(1)
    os.nice(-13)
    time.sleep(2)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed > 5), "A process with league and high nice shouldnt block"        
    
def test16():# son with 25 boards +10 nice. father with -13 nice spending time. should block
    """ Verify a process with a league blocks other processes """
    pyHighscore.highscore_chleague(0)
    cpid = os.fork()
    s = time.time()
    if cpid == 0: # son
        pyHighscore.highscore_chleague(0)
        pyHighscore.highscore_add('/board', 1)
        pyHighscore.highscore_add('/board2', 1)
        pyHighscore.highscore_add('/board3', 1)
        pyHighscore.highscore_add('/board4', 1)
        pyHighscore.highscore_add('/board5', 1)
        pyHighscore.highscore_add('/board6', 1)
        pyHighscore.highscore_add('/board7', 1)
        pyHighscore.highscore_add('/board8', 1)
        pyHighscore.highscore_add('/board9', 1)
        pyHighscore.highscore_add('/board10', 1)
        pyHighscore.highscore_add('/board11', 1)
        pyHighscore.highscore_add('/board12', 1)
        pyHighscore.highscore_add('/board13', 1)
        pyHighscore.highscore_add('/board14', 1)
        pyHighscore.highscore_add('/board15', 1)
        pyHighscore.highscore_add('/board16', 1)
        pyHighscore.highscore_add('/board17', 1)
        pyHighscore.highscore_add('/board18', 1)
        pyHighscore.highscore_add('/board19', 1)
        pyHighscore.highscore_add('/board20', 1)
        pyHighscore.highscore_add('/board21', 1)
        pyHighscore.highscore_add('/board22', 1)
        pyHighscore.highscore_add('/board23', 1)
        pyHighscore.highscore_add('/board24', 1)
        pyHighscore.highscore_add('/board25', 1)
        os.nice(10)
        time.sleep(3)
        # Spend time, should block the parent for about 5s
        spend_time(7)
        os._exit(0)
    spend_time(1)
    os.nice(-13)
    spend_time(2)
    e = time.time()
    elapsed = e - s
    print(elapsed)
    os.wait()
    assert (elapsed > 8), "A process with league and high nice shouldnt block"        

def test17(): # error finding is only with log.
    """ Verify a process with a league blocks other processes """
    os.nice(-5)
    pyHighscore.highscore_chleague(0)
    pyHighscore.highscore_add('/board', 1)
    os.nice(-5)
    pyHighscore.highscore_chleague(-1)

if __name__ == "__main__":
    test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    # test7()
    # test8()
    # test9()
    # test10()
    # test11()
    # test12()
    # test13()
    # test14()
    # test15()
    # test16()
    # test17()

    