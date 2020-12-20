#ifndef _LEAGUE_H_
#define _LEAGUE_H_

typedef struct _score
{
    struct _score *next;
    unsigned int score;
} *score_node;

typedef struct _board
{
    char *name;
    struct _board *next;
    score_node score_list;
} *Board;

typedef struct _league
{
    Board board_list;
    int ref_count;
} *league;

league init_league(void);

void destroy_league(league l);

#endif
