#include <linux/slab.h>
#include "linux/league.h"

league_count = 0;

league init_league(void) {
    league l = (league)kmalloc(sizeof(struct _league), GFP_KERNEL);
    if(l){
        return NULL;
    }
    l->ref_count = 1;
    l->board_list = NULL;
    
    league_count++;

    return l;
}

void destroy_league(league l) {
    if(l) {
        Board board_it = l->board_list;
        while (board_it)
        {
            score_node score_it = board_it->score_list;
            while (score_it)
            {
                score_node tmp = score_it;
                score_it = score_it->next;
                kfree(tmp);
            }
            Board tmp_b = board_it;
            board_it = board_it->next;
            kfree(tmp_b);
        }
        kfree(l);
        league_count--;    
    }
}