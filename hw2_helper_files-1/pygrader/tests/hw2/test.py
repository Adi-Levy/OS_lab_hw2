#!/usr/bin/python

import os
import errno
import pyHighscore

def test1():
	"""simple test to invoke the syscalls with no error."""

	pyHighscore.highscore_add("board", 5)
	top10_scores = pyHighscore.highscore_list("board", 10)
    	pyHighscore.highscore_chleague(-1)
	num_of_leagues = pyHighscore.highscore_leagues()


if __name__ == "__main__":
    test1()
