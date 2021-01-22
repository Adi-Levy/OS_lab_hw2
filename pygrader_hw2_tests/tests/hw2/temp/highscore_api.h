#ifndef HIGHSCORE_API_H
#define HIGHSCORE_API_H
#include <linux/stddef.h>
#include <errno.h>
#include <sys/types.h>

int highscore_add(const char *board, unsigned int score)
{
    int res;

    __asm__(
        "pushl %%eax;"
        "pushl %%ebx;"
        "pushl %%ecx;"
        "movl $243, %%eax;"
        "movl %1, %%ebx;"
        "movl %2, %%ecx;"
        "int $0x80;"
        "movl %%eax,%0;"
        "popl %%ecx;"
        "popl %%ebx;"
        "popl %%eax;"
        : "=m"(res)

        : "m"(board), "m"(score));
    if (res >= (unsigned long)(-125))
    {
        errno = -res;
        res = -1;
    }
    return (int)res;
}

ssize_t highscore_list(const char *board, unsigned int *buf, ssize_t size)
{
    int res;

    __asm__(
        "pushl %%eax;"
        "pushl %%ebx;"
        "pushl %%ecx;"
        "pushl %%edx;"
        "movl $244, %%eax;"
        "movl %1, %%ebx;"
        "movl %2, %%ecx;"
        "movl %3, %%edx;"
        "int $0x80;"
        "movl %%eax,%0;"
        "popl %%edx;"
        "popl %%ecx;"
        "popl %%ebx;"
        "popl %%eax;"
        : "=m"(res)

        : "m"(board), "m"(buf), "m"(size));
    if (res >= (unsigned long)(-125))
    {
        errno = -res;
        res = -1;
    }
    return (ssize_t)res;
}

int highscore_chleague(pid_t pid)
{
    int res;

    __asm__(
        "pushl %%eax;"
        "pushl %%ebx;"
        "movl $245, %%eax;"
        "movl %1, %%ebx;"
        "int $0x80;"
        "movl %%eax,%0;"
        "popl %%ebx;"
        "popl %%eax;"
        : "=m"(res)

        : "m"(pid));
    if (res >= (unsigned long)(-125))
    {
        errno = -res;
        res = -1;
    }
    return (int)res;
}

int highscore_leagues()
{
    int res;

    __asm__(
        "pushl %%eax;"
        "movl $246, %%eax;"
        "int $0x80;"
        "movl %%eax,%0;"
        "popl %%eax;"
        : "=m"(res));

    if (res >= (unsigned long)(-125))
    {
        errno = -res;
        res = -1;
    }
    return (int)res;
}

#endif //HIGHSCORE_API_H
