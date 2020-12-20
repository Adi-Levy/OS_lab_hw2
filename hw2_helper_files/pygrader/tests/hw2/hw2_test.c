#include <stdio.h>
#include <assert.h>
#include "highscore_api.h"

int main()
{
	// Get current pid
	int res = -1;
    unsigned int scores[4];

	// Add a new board
	res = highscore_add("/root/map1", 10);
	assert(res == 0);

	// List current scores for map1
	res = highscore_list("/root/map1", scores, 4);
	assert(res == 1);
    assert(scores[0] == 10);

    // Start a new league
    res = highscore_chleague(0);
    assert(res == 0);

    // Check number of leagues
    res = highscore_leagues();
    assert(res == 1);

	return 0;
}
