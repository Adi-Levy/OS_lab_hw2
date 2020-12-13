#include "include/linux/highscore_chleague.h"
#include <linux/kernel.h>
#include <linux/sched.h>

int sys_highscore_chleague(pid_t pid){
    printk("sys_highscore_chleague");
    
    if (pid < 0) // leave league
    {
        if(current->task_league == NULL) {
            return -ESRCH;
        }
        current->task_league->ref_count--;
		if(current->task_league->ref_count == 0) {
			destroy_league(current->task_league);
		}
        current->task_league = NULL;
    }
    else if (pid == 0)
    {
        league new_league = init_league();
        if(!new_league) {
            return -ENOMEM;
        }
        if(current->task_league != NULL) {
            current->task_league->ref_count--;
		    if(current->task_league->ref_count == 0) {
			    destroy_league(current->task_league);
		    }
        }
        current->task_league = new_league;
    }
    else
    {
        task_t *task = find_task_by_pid(pid);
        if(task->task_league == NULL) {
            return -ESRCH;
        }
        current->task_league->ref_count--;
		if(current->task_league->ref_count == 0) {
			destroy_league(current->task_league);
		}
        current->task_league = task->task_league;
        current->task_league->ref_count++;
    }
    return 0;
}