#ifndef _LEAGUE_H_
#define _LEAGUE_H_

#include <sys/types.h>
#include <linux/slab.h>

typedef struct _score
{
    struct _score *next;
    int score;
} *score_node;

typedef struct _board
{
    char *name;
    struct _board *next;
    score_node score_list;
} *board;

typedef struct _league
{
    board boards_list;
    int ref_count;
} *league;

int league_count = 0;

league init_league(void) {
    league l = (league)kmalloc(sizeof(struct _league));
    if(!l){
        return NULL;
    }
    l->ref_count = 1;
    l->boards_list = NULL;
    
    league_count++;

    return l;
}

void destroy_league(league l) {
    if(!l) {
        board board_it = l->boards_list;
        while (board_it)
        {
            score_node score_it = board_it->score_list;
            while (score_it)
            {
                score_node tmp = score_it;
                score_it = score_it->next;
                kfree(tmp);
            }
            board tmp_b = board_it;
            board_it = board_it->next;
            kfree(tmp_b);
        }
        kfree(l);
    }    
}

#endif
