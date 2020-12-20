#!/usr/bin/python

#from __future__ import division
from hwgrader.module_utils import *
from hwgrader.test_utils import *
from hwgrader.utils import ParTextTestRunner, ParTestCase, RebootableTestSuite
import fcntl
import unittest
import os
import sys
import time
import math
import errno
import struct
import pyHighscore


class hw_test(ParTestCase):
    """Basic test"""

    _TEST_TIMEOUT = 10

    def test_1(self):
    	"""test 1"""

        pyHighscore.highscore_add("board", 5)
    	top10_scores = pyHighscore.highscore_list("board", 10)
        pyHighscore.highscore_chleague(0)
        num_of_leagues = pyHighscore.highscore_leagues()

    def test_2(self):
    	"""test 2"""

    	num_of_leagues = pyHighscore.highscore_leagues()
    	assert num_of_leagues == 0

    	ret = pyHighscore.highscore_chleague(0)
        assert ret == None

    	num_of_leagues = pyHighscore.highscore_leagues()
    	assert num_of_leagues == 1

    	pyHighscore.highscore_chleague(-1)
    	num_of_leagues = pyHighscore.highscore_leagues()
    	assert num_of_leagues == 0

    	top10_scores = pyHighscore.highscore_list("a1", 10)
        assert top10_scores == ()

    	num_of_leagues = pyHighscore.highscore_leagues()
    	assert num_of_leagues == 1

    	res = pyHighscore.highscore_chleague(0)
        assert res == None

    	res = pyHighscore.highscore_add("a2", 5)
        assert res == 0

        top10_scores = pyHighscore.highscore_list("a2", 10)
        assert top10_scores == (5,)

        top10_scores = pyHighscore.highscore_list("a2", 1)
        assert top10_scores == (5,)

        top10_scores = pyHighscore.highscore_list("a2", 0)
        assert top10_scores == ()

    	num_of_leagues = pyHighscore.highscore_leagues()
    	assert num_of_leagues == 1

    def test_3(self):
    	"""test 3 - fork"""

        pid = os.fork()
        if pid > 0 : #father
            time.sleep(1);
            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 1

    	    res = pyHighscore.highscore_add("two", 5)
            assert res == 0

            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 2

            top_scores = pyHighscore.highscore_list("two", 3)
            assert top_scores == (5,)

            res = pyHighscore.highscore_chleague(pid)
            assert res == None

            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 1

            res = pyHighscore.highscore_add("one", 6)
            assert res == 1

            top_scores = pyHighscore.highscore_list("two", 3)
            assert top_scores == ()

            top_scores = pyHighscore.highscore_list("one", 3)
            assert top_scores == (3,6)

            time.sleep(5)

            pyHighscore.highscore_chleague(-1)
            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 0

        else : #son
            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 0

            pyHighscore.highscore_chleague(0)
            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 1

            res = pyHighscore.highscore_add("one", 3)
            assert res == 0

            time.sleep(3)

            res = pyHighscore.highscore_add("one", 1)
            assert res == 0

            top_scores = pyHighscore.highscore_list("one", 3)
            assert top_scores == (1,3,6)

    def test_4(self):
        '''test 4 '''
        ret = pyHighscore.highscore_chleague(-1)
        assert ret == None

    def test_5(self):
        '''test 5 - exceptions'''
        try:
            pyHighscore.highscore_chleague(11)
            self.assertEqual(1, 0, "Expected error to be thrown")
        except OSError, e:
            self.assertEqual(e.strerror, 'No such process')

    def test_6(self):
        '''test 6 - exceptions'''
        try:
            pyHighscore.highscore_list("one", -1)
            self.assertEqual(1, 0, "Expected error to be thrown")
        except OSError, e:
            self.assertEqual(e.strerror, 'Invalid argument')


    def test_7(self):
        '''test 7 - board NULL'''
        try:
            pyHighscore.highscore_add(None, 1)
            self.assertEqual(1, 0, "Expected error to be thrown")
        except OSError, e:
            self.assertEqual(e.strerror, 'Bad address')

        try:
            pyHighscore.highscore_list(None, 1)
            self.assertEqual(1, 0, "Expected error to be thrown")
        except OSError, e:
            self.assertEqual(e.strerror, 'Bad address')

    def test_8(self):
        '''test 8 - list'''

        top_scores = pyHighscore.highscore_list("two", 3)
        assert top_scores == ()

        res = pyHighscore.highscore_add("one", 1)
        assert res == 0

        res = pyHighscore.highscore_add("one", 6)
        assert res == 1

        res = pyHighscore.highscore_add("one", 2)
        assert res == 1

        res = pyHighscore.highscore_add("one", 7)
        assert res == 3

        top_scores = pyHighscore.highscore_list("two", 3)
        assert top_scores == ()

        top_scores = pyHighscore.highscore_list("one", 0)
        assert top_scores == ()

        top_scores = pyHighscore.highscore_list("one", 1)
        assert top_scores == (1,)

        top_scores = pyHighscore.highscore_list("one", 3)
        assert top_scores == (1,2,6)

        top_scores = pyHighscore.highscore_list("one", 50)
        assert top_scores == (1,2,6,7)

    def test_9(self):
        '''test 9- fork2'''
        pid = os.fork()
        if pid > 0 : #father
            time.sleep(1)
            try:
                pyHighscore.highscore_chleague(pid)
                self.assertEqual(1, 0, "Expected error to be thrown")
            except OSError, e:
                self.assertEqual(e.strerror, 'No such process')

        else : #son
            ret = pyHighscore.highscore_chleague(-1)
            assert ret == None
            time.sleep(3)

    def test_10(self):
        '''test 10- fork3'''
        pid = os.fork()
        if pid > 0 : #father
            time.sleep(1)

            ret = pyHighscore.highscore_chleague(pid)
            assert ret == None

            top_scores = pyHighscore.highscore_list("one", 6)
            assert top_scores == (1,)

            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 1

        else : #son
            res = pyHighscore.highscore_add("one", 1)
            assert res == 0

            time.sleep(3)

            num_of_leagues = pyHighscore.highscore_leagues()
            assert num_of_leagues == 1

def suite(**args):
    global SUBMISSION_PATH

    SUBMISSION_PATH = args['submission_path']
    return unittest.makeSuite(hw_test, 'test')


if __name__ == "__main__":
   unittest.main(testRunner=ParTextTestRunner())
