#include <linux/kernel.h>
#include <asm/uaccess.h>
#include <linux/sched.h>
#include <linux/slab.h>
#include <linux/string.h>

#include "linux/league.h"


int sys_highscore_add(const char *board, unsigned int score){
    printk("sys_highscore_add\n");
    
    score_node new_score = (score_node)kmalloc(sizeof(struct _score), GFP_KERNEL);
    if(!new_score){
        return -ENOMEM;
    }
    printk("in add after score kmalloc\n");
    // check if procces has league (create league if not)
    if (!(current->task_league))
    {
        current->task_league = init_league();
        if(!(current->task_league)) {
            kfree(new_score);
            return -ENOMEM;
        }
    }
    printk("in add after checking league\n");
    // check if league had board (create board if not)
    char* board_name = (char*)kmalloc(sizeof(char)*100, GFP_KERNEL);
    if(!board_name) {
        kfree(new_score);
        return -ENOMEM;
    }
    printk("in add after getting board name\n");
    int e = strncpy_from_user(board_name, board, 100);
    if(e == -EFAULT) {
        kfree(board_name);
        return e;
    }
    printk("in add after copy from user\n");
    Board board_it = current->task_league->board_list;
    printk("1\n");
    Board new_board = NULL;
    printk("2\n");
    while (board_it != NULL) {
        if(!strcmp(board_it->name, board_name)) {
            new_board = board_it;
            break;
        }
        board_it = board_it->next;
    }
    printk("in add after finding board\n");
    if(!new_board){
        new_board = (Board)kmalloc(sizeof(struct _board), GFP_KERNEL);
        if (!new_board)
        {
            kfree(board_name);
            return -ENOMEM;
        }
        new_board->name = board_name;
        new_board->next = current->task_league->board_list;
        new_board->score_list = NULL;
        current->task_league->board_list = new_board;
    }
    else // board exists
    {
        kfree(board_name);
    }
    printk("in add after creating new board\n");

    // add score to the board
    new_score->score = score;
    
    if(new_board->score_list == NULL){
        new_score->next = NULL;
        new_board->score_list = new_score;
        return 0;
    }
    printk("in add after adding first score\n");
    unsigned int position = 0;
    if(score < new_board->score_list->score) {
        new_score->next = new_board->score_list;
        new_board->score_list = new_score;
        return position;
    }
    position++;
    printk("in add after adding score at top of list\n");
    score_node score_it = new_board->score_list;
    while (score_it->next != NULL && score >= score_it->next->score)
    {
        score_it = score_it->next;
        position++;
    }
    new_score->next = score_it->next;
    score_it->next = new_score;
    printk("in add at end of syscall\n");
    return position;
}
