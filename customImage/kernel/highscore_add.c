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
    // check if procces has league (create league if not)
    if (!(current->task_league))
    {
        current->task_league = init_league();
        if(!(current->task_league)) {
            kfree(new_score);
            return -ENOMEM;
        }
    }
    // check if league had board (create board if not)
    char* board_name = (char*)kmalloc(sizeof(char)*100, GFP_KERNEL);
    if(!board_name) {
        kfree(new_score);
        return -ENOMEM;
    }
    int e = strncpy_from_user(board_name, board, 100);
    if(e == -EFAULT) {
        kfree(new_score);
        kfree(board_name);
        return e;
    }
    Board board_it = current->task_league->board_list;
    Board new_board = NULL;
    while (board_it != NULL) {
        if(!strcmp(board_it->name, board_name)) {
            new_board = board_it;
            break;
        }
        board_it = board_it->next;
    }
    if(!new_board){
        new_board = (Board)kmalloc(sizeof(struct _board), GFP_KERNEL);
        if (!new_board)
        {
            kfree(board_name);
            kfree(new_score);
            return -ENOMEM;
        }
        new_board->name = board_name;
        new_board->next = current->task_league->board_list;
        new_board->score_list = NULL;
        current->task_league->board_list = new_board;
        current->task_league->board_count++;
    }
    else // board exists
    {
        kfree(board_name);
    }

    // add score to the board
    new_score->score = score;
    
    if(new_board->score_list == NULL){
        new_score->next = NULL;
        new_board->score_list = new_score;
        return 0;
    }
    unsigned int position = 0;
    if(score < new_board->score_list->score) {
        new_score->next = new_board->score_list;
        new_board->score_list = new_score;
        return position;
    }
    position++;
    score_node score_it = new_board->score_list;
    while (score_it->next != NULL && score >= score_it->next->score)
    {
        score_it = score_it->next;
        position++;
    }
    new_score->next = score_it->next;
    score_it->next = new_score;
    return position;
}
