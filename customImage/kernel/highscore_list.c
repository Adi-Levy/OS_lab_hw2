#include <linux/kernel.h>
#include <asm/uaccess.h>
#include <linux/sched.h>
#include <linux/slab.h>

#include "linux/league.h"

ssize_t sys_highscore_list(const char *board, unsigned int *buffer, ssize_t size){
    printk("sys_highscore_list");
    
    if(size < 0){
        return -EINVAL;
    }
    
    unsigned int* k_buffer = (unsigned int*)kmalloc(sizeof(unsigned int)*size, GFP_KERNEL);
    if(!k_buffer){
        return -ENOMEM;
    }
    
    // check if procces has league (create league if not)
    if (!(current->task_league))
    {
        current->task_league = init_league();
        return 0;
    }

    // check if league has board (return empty if not)
    char* board_name = (char*)kmalloc(sizeof(char)*100, GFP_KERNEL);
    if(!board_name){
        kfree(k_buffer);
        return -ENOMEM;
    }
    int e = strncpy_from_user(board_name, board, 100);
    if(e == -EFAULT){
        kfree(k_buffer);
        kfree(board_name);
        return e;
    }
    Board board_it = current->task_league->board_list;
    while (board_it != NULL)
    {
        if(!strcmp(board_it->name, board_name)){
            break;
        }
        board_it = board_it->next;
    }
    if(!board_it){
        kfree(k_buffer);
        return 0;
    }

    // return leader list of board
    score_node score_it = board_it->score_list;
    int count = 0;
    while (score_it != NULL && count < size)
    {
        k_buffer[count] = score_it->score;
        score_it = score_it->next;
        count++;
    }
    
    if(copy_to_user(buffer, k_buffer, sizeof(unsigned int)*count) != 0) {
        count = -EFAULT;
    }

    kfree(k_buffer);
    kfree(board_name);
    return count;
}
