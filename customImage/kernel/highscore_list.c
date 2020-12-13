#include "include/linux/highscore_list.h"
#include <linux/kernel.h>

ssize_t sys_highscore_list(const char *board, unsigned int *buffer, ssize_t size){
    printk("sys_highscore_list");
    return 0;
}