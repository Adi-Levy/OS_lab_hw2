#!/usr/bin/python

from __future__ import division
from hwgrader.test_utils import memTrack
from hwgrader.test_utils import *
from hwgrader.utils import ParTextTestRunner, ParTestCase, TestError, RebootableTestSuite
import unittest
import shutil
import fcntl
import sys
import os
import time
import errno

EXTENSION_FILES = ('setup.py', 'py_highscore.c')
HEADER_FILE = 'highscore_api.h'
TD_DESC1 = 'Prepare HW2 in time'
TD_DESC_indexed = 'Prepare HW%d in time'
TEMP_FOLDER = 'temp'
EXT_SUCCESSFUL = True


class hw_test(ParTestCase):
    """Basic test"""

    def setUp(self):

        pass
    
    def tearDown(self):

        pass

    def test_header(self):
        """Verify that the header file compiled successfuly."""

        self.assert_(EXT_SUCCESSFUL, 'Failed compilation of %s.' % HEADER_FILE)
        
    def test_add1(self):
        """ Test correct return values of highscore_add: bad args """
        self.errnoCheck(
            cmd=pyHighscore.highscore_add,
            args=(None, 23),
            expected_errno=EFAULT,
            msg='adding a score to NULL board is not allowed');

    def test_add2(self):
        """ Test correct return values of highscore_add: one board """
        place = pyHighscore.highscore_add('/some/board', 4)
        self.assertEqual(place, 0, 'First score in a board should be first')
        place = pyHighscore.highscore_add('/some/board', 2)
        self.assertEqual(place, 0, 'Lower score should be before higher scores')
        place = pyHighscore.highscore_add('/some/board', 3)
        self.assertEqual(place, 1, 'A middle score should be places between higher and lower scores')

    def test_add3(self):
        """ Test correct return values of highscore_add: two boards """
        pyHighscore.highscore_add('/some/board', 4)
        pyHighscore.highscore_add('/some/board', 2)
        pyHighscore.highscore_add('/some/board', 3)
        place = pyHighscore.highscore_add('/some/board2', 3)
        self.assertEqual(place, 0, 'Different boards should have independent tables')

    def test_list1(self):
        """ Test correct return values of highscore_list: bad args """
        self.errnoCheck(
            cmd=pyHighscore.highscore_list,
            args=(None, 3),
            expected_errno=EFAULT,
            msg='Listing a NULL board is not allowed');
        self.errnoCheck(
            cmd=pyHighscore.highscore_list,
            args=("/some/board", -3),
            expected_errno=EINVAL,
            msg='Listing with an invalid buffer size is not allowed');
        pyHighscore.highscore_add('/some/board', 4) # Avoid ambiguity with non-existing board condition
        self.errnoCheck(
            cmd=pyHighscore.highscore_list_NULL,
            args=("/some/board", 3),
            expected_errno=EFAULT,
            msg='Listing to a NULL buffer is not allowed');

    def test_list2(self):
        """ Test correct return values of highscore_list: empty board """
        scores = pyHighscore.highscore_list('/some/board', 5)
        self.assertEqual(scores, (), 'Listing a new board should return an empty list')

    def test_list3(self):
        """ Test correct return values of highscore_list: board with scores """
        pyHighscore.highscore_add('/some/board', 4)
        pyHighscore.highscore_add('/some/board', 0)
        pyHighscore.highscore_add('/some/board', 1)
        scores = pyHighscore.highscore_list('/some/board', 3)
        self.assertEqual(scores, (0, 1, 4), 'Listing a board should return a sorted tuple of scores')

    def test_list4(self):
        """ Test correct return values of highscore_list: partial read """
        pyHighscore.highscore_add('/some/board', 4)
        pyHighscore.highscore_add('/some/board', 0)
        pyHighscore.highscore_add('/some/board', 1)
        scores = pyHighscore.highscore_list('/some/board', 1)
        self.assertEqual(scores, (0,), 'Listing a board should return the requested amount of entries')

    def test_list5(self):
        """ Test correct return values of highscore_list: too big a read """
        pyHighscore.highscore_add('/some/board', 4)
        pyHighscore.highscore_add('/some/board', 0)
        pyHighscore.highscore_add('/some/board', 1)
        scores = pyHighscore.highscore_list('/some/board', 5)
        self.assertEqual(scores, (0, 1, 4), 'Listing a board should not fill the buffer if there are too few entries')

    def test_list6(self):
        """ Test correct return values of highscore_list: empty buffer """
        pyHighscore.highscore_add('/some/board', 4)
        pyHighscore.highscore_add('/some/board', 0)
        pyHighscore.highscore_add('/some/board', 1)
        scores = pyHighscore.highscore_list('/new/board', 0)
        self.assertEqual(scores, (), 'Listing a board with an empty buffer should return an empty result')

    def test_chleague1(self):
        """ Test correct behavior of highscore_chleague (using a single process): process not in a league """
        self.errnoCheck(
            cmd=pyHighscore.highscore_chleague,
            args=(1,),
            expected_errno=ESRCH,
            msg='A process with no league should return ESRCH');

    def test_chleague2(self):
        """ Test correct behavior of highscore_chleague (using a single process): non existing process """
        self.errnoCheck(
            cmd=pyHighscore.highscore_chleague,
            args=(65535,),
            expected_errno=ESRCH,
            msg='Non-existing process should return ESRCH');

    def test_chleague3(self):
        """ Test correct behavior of highscore_chleague (using a single process): correct usage """
        # Test1: All following commands should allocate and then free memory
        mm_track = memTrack()
        mm_track.start_track()
        try:
            pid = os.getpid()
            # Test2: New league should reset tables
            pyHighscore.highscore_add('/some/board', 4)
            pyHighscore.highscore_add('/some/board', 0)
            pyHighscore.highscore_add('/some/board', 1)
            pyHighscore.highscore_chleague(0)
            scores = pyHighscore.highscore_list('/some/board', 5)
            self.assertEqual(scores, (), 'A new league should have empty tables for all boards')
            # Test3: Leaving all leagues should be similar to creating a new league
            pyHighscore.highscore_add('/some/board', 4)
            pyHighscore.highscore_add('/some/board', 0)
            pyHighscore.highscore_add('/some/board', 1)
            pyHighscore.highscore_chleague(-1)
            scores = pyHighscore.highscore_list('/some/board', 5)
            self.assertEqual(scores, (), 'Leaving a league should not keep access to previous tables')
            pyHighscore.highscore_chleague(-1)

  	    mm_track.end_track()
            mm_track.validate([pid], self, debug=True)
        finally:        
            mm_track.close()

    def test_leagues1(self):
        """ Test correct return value of highscore_leagues(): boot empty """
        leagues = pyHighscore.highscore_leagues()
        self.assertEqual(leagues, 0, 'No leagues should be present at system boot')

    def test_leagues2(self):
        """ Test correct return value of highscore_leagues(): create by list """
        pyHighscore.highscore_list('/some/board', 5)
        leagues = pyHighscore.highscore_leagues()
        self.assertEqual(leagues, 1, 'Listing should create a league')

    def test_leagues3(self):
        """ Test correct return value of highscore_leagues(): delete empty """
        pyHighscore.highscore_list('/some/board', 5)
        pyHighscore.highscore_chleague(0)
        leagues = pyHighscore.highscore_leagues()
        self.assertEqual(leagues, 1, 'Leagues with no processes should be deleted')

        pyHighscore.highscore_chleague(-1)
        leagues = pyHighscore.highscore_leagues()
        self.assertEqual(leagues, 0, 'Leagues with no processes should be deleted')

    def test_leagues4(self):
        """ Test correct return value of highscore_leagues(): create by add """
        pyHighscore.highscore_add('/some/board', 1)
        leagues = pyHighscore.highscore_leagues()
        self.assertEqual(leagues, 1, 'Adding should create a league')

    def test_multi_process(self):
        """ Test league behavior with several processes """
        # Test1: All following commands should allocate and then free memory
        mm_track = memTrack()
        mm_track.start_track()
        try:
            ppid = os.getpid()
            pyHighscore.highscore_add('/some/board', 4)

            cpid = os.fork()
            if (cpid == 0):
                # Test2: In child
                # Using same league as parent
                scores = pyHighscore.highscore_list('/some/board', 5)
                self.assertEqual(scores, (4, ), 'Child process should share the league of the parent by default')

                pyHighscore.highscore_add('/some/board', 2) # Parent should later observe this

                # Startin a new league
                pyHighscore.highscore_chleague(0)
                pyHighscore.highscore_add('/some/board', 2)
                scores = pyHighscore.highscore_list('/some/board', 5)
                self.assertEqual(scores, (2, ), 'A new league should be separate than other leagues still existing')
                league_count = pyHighscore.highscore_leagues()
                self.assertEqual(league_count, 2)

                # Returning to previous league
                pyHighscore.highscore_chleague(ppid)
                scores = pyHighscore.highscore_list('/some/board', 5)
                self.assertEqual(scores, (2, 4), 'Previous league should still exist as long as some process is using it')

                league_count = pyHighscore.highscore_leagues()
                self.assertEqual(league_count, 1, 'League with no processes should be terminated')

                os._exit(0)
            # Test3: In parent
            os.wait()
            scores = pyHighscore.highscore_list('/some/board', 5)
            self.assertEqual(scores, (2, 4), 'League data should be shared between all processes using it')

            pyHighscore.highscore_chleague(-1)
            league_count = pyHighscore.highscore_leagues()
            self.assertEqual(league_count, 0)

  	    mm_track.end_track()
            mm_track.validate([cpid, ppid], self, debug=True)
        finally:        
            mm_track.close()


def compile_extension(test_folder, submission_folder):
            
    global EXT_SUCCESSFUL
    
    #
    # Prepare a temporary folder with all necessary files.
    #
    temp_folder = os.path.join(test_folder, TEMP_FOLDER)
    os.chdir(test_folder)
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder, ignore_errors=True)
    os.mkdir(temp_folder)
    
    shutil.copy(os.path.join(submission_folder, HEADER_FILE), temp_folder)
    for file in EXTENSION_FILES:
        shutil.copy(os.path.join(test_folder, file), temp_folder)
    
    #
    # Compile the extension module and import it into the modules namespace
    # Note:
    # I am saving the sys.argv because the run_setup script overwrites them
    # due to a bug
    #
    os.chdir(temp_folder)
    from distutils.core import run_setup
    save_argv = list(sys.argv)
    run_setup('setup.py', script_args=['build_ext', '-b', temp_folder])
    sys.argv = save_argv
    
    if os.path.exists(os.path.join(temp_folder, 'pyHighscore.so')):
        EXT_SUCCESSFUL = True
        #sys.path.append(temp_folder)
    else:
        EXT_SUCCESSFUL = False
        #sys.path.append(test_folder)

    #
    # Note,
    # In any case I use my extension.
    #
    sys.path.append(test_folder)
    os.chdir(test_folder)

    globals().update({'pyHighscore': __import__('pyHighscore')})
    del sys.path[-1]


def suite(**args):
    
    #
    # First, compile the extension
    #
    test_folder = os.path.split(args['test_path'])[0]
    submission_folder = args['submission_path']
    compile_extension(test_folder, submission_folder)

    #
    # Return the test suite
    #
    return unittest.makeSuite(hw_test, prefix='test')


if __name__ == "__main__":


    script_path = os.path.abspath(sys.argv[0])
    test_folder = os.path.split(script_path)[0]
    submission_folder = test_folder
    
    #
    # Compile the extension
    #
    compile_extension(test_folder, submission_folder)

    #
    # Run the tests
    #
    unittest.main(testRunner=ParTextTestRunner())


