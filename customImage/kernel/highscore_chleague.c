#include <linux/kernel.h>
#include <linux/sched.h>

#include "linux/league.h"

int sys_highscore_chleague(pid_t pid){
    printk("sys_highscore_chleague");
    
    if (pid < 0) // leave league
    {
        if(current->task_league == NULL) {
            return 0;
        }
        league tmp = current->task_league;
        current->task_league = NULL;
        tmp->ref_count--;
		if(tmp->ref_count == 0) {
			destroy_league(tmp);
		}
        //current->prio = current->static_prio;
        //league_prio(current);
    }
    else if (pid == 0) // create new league
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
        //league_prio(current);
    }
    else // joid league
    {
        task_t *task = find_task_by_pid(pid);
        if(task == NULL || task->task_league == NULL) {
            return -ESRCH;
        }
        if(current->task_league != NULL) {
            current->task_league->ref_count--;
            if(current->task_league->ref_count == 0) {
                destroy_league(current->task_league);
            }
        }
        current->task_league = task->task_league;
        current->task_league->ref_count++;
        //league_prio(current);
    }

    
    return 0;
}
