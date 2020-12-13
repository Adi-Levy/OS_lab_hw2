#include "include/linux/highscore_add.h"
#include <linux/kernel.h>

int sys_highscore_add(const char *board, unsigned int score){
    printk("sys_highscore_add");
    return 0;
}