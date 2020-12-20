#include <linux/kernel.h>

#include "linux/league.h"

extern int league_count;

int sys_highscore_leagues(void){
    printk("sys_highscore_leagues");
    return league_count;
}