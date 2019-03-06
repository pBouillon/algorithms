#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <unistd.h>

#define SOURCE_FILE ""

#define BUFF_SIZE 1024
#define ALPHABET    26

#define SPACES      32

#define BEG_LOWER   97
#define END_LOWER  122

#define BEG_UPPER   65
#define END_UPPER   90


int main(void) {
    char* filename = SOURCE_FILE;

    // file opening
    FILE *file ;
    char  buff[BUFF_SIZE] ;
    int   lines ;

    if (!(file = fopen(filename, "r")))
    {
       fprintf (stderr, "%s\n", "Cannot open file") ; 
       exit (EXIT_FAILURE) ;
    }

    // counters
    int spaces = 0;
    int lower_occurences[ALPHABET];
    int upper_occurences[ALPHABET];
    for(int i = 0; i < ALPHABET; ++i)
    {
        lower_occurences[i] = 0;
        upper_occurences[i] = 0;
    }

    // reading each line
    while (fgets(buff, BUFF_SIZE, file))
    {
        // reading each char
        for (int i = 0; i < (int)strlen(buff); ++i) 
        {
            // handling spaces
            if(buff[i] == 32)
            {
                ++spaces;
                continue;
            }

            // handling lowercase
            if(buff[i] >= BEG_LOWER && buff[i] <= END_LOWER)
            {
                ++lower_occurences[buff[i] - BEG_LOWER];
            }

            // handling uppercase
            if(buff[i] >= BEG_UPPER && buff[i] <= END_UPPER)
            {
                ++upper_occurences[buff[i] - BEG_UPPER];
            }
        }
    }
    fclose (file) ;

    // displaying result
    for (int i = 0; i < ALPHABET; ++i)
    {
        printf(
            "%c: %d\t|\t%c: %d\n", 
            BEG_LOWER + i, 
            lower_occurences[i], 
            BEG_UPPER + i, 
            upper_occurences[i]
        );
    }
    printf("total spaces: %d\n", spaces);

    return 0;
}
