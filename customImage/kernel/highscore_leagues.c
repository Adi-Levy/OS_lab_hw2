#include "include/linux/highscore_leagues.h"
#include <linux/kernel.h>

int sys_highscore_leagues(void){
    printk("sys_highscore_leagues");
    return 0;
}