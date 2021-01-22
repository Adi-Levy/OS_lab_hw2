#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include "highscore_api.h"

// This spends about 5s
void spend_time() {
    int i, j;
    int sum = 0;
    for (i=0; i<5; i++) {
        for (j=0; j<15000000; j++) {
            sum++;
        }
    }
}

int main()
{
	// simple self test
    pid_t cpid = fork();
	int res = -1;
    time_t start_time, end_time;
            
    start_time = time(NULL);
    if (cpid == 0) {
        // In child: Add a league and block the parent.
        highscore_chleague(0);
        res = highscore_add("/board1", 1);
        assert(res == 0);
        spend_time();
        return 0;
    }
    sleep(1);
    end_time = time(NULL);
	// Make sure the process slept for at least 4 because of its child blocking it
	assert(end_time - start_time > 4);
	printf("Test Done\n");
	
	return 0;
}
