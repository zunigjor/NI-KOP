#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#ifdef _MSC_VER
#undef max
#undef min
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include <stdint.h> // portable: uint64_t   MSVC: __int64 

// MSVC defines this in winsock2.h!?
typedef struct timeval {
    long tv_sec;
    long tv_usec;
} timeval;

int gettimeofday(struct timeval* tp, struct timezone* tzp)
{
    // Note: some broken versions only have 8 trailing zero's, the correct epoch has 9 trailing zero's
    // This magic number is the number of 100 nanosecond intervals since January 1, 1601 (UTC)
    // until 00:00:00 January 1, 1970 
    static const uint64_t EPOCH = ((uint64_t)116444736000000000ULL);

    SYSTEMTIME  system_time;
    FILETIME    file_time;
    uint64_t    time;

    GetSystemTime(&system_time);
    SystemTimeToFileTime(&system_time, &file_time);
    time = ((uint64_t)file_time.dwLowDateTime);
    time += ((uint64_t)file_time.dwHighDateTime) << 32;

    tp->tv_sec = (long)((time - EPOCH) / 10000000L);
    tp->tv_usec = (long)(system_time.wMilliseconds * 1000);
    return 0;
}
#else
#include <sys/time.h>           /* gettimeofday */
#endif

#include "rngctrl.h"

/* options */
char* endsts = NULL;		/* filename to write RNG state at the end */
char* begsts = NULL;		/* filename to write RNG state at the beginning */
rng_seed_t  rng_seed;  int rng_seed_given = 0;
rng_state_t rng_state; int rng_state_given = 0;

void rng_seed_time (rng_seed_t* pseed) {
    struct timeval tv;
    unsigned long long tm;
    gettimeofday (&tv, NULL);
    tm = (long long)tv.tv_sec + 1000000*(long long)tv.tv_usec;
    *pseed = tm & 0xFFFFFFFF;
}

int rng_options (int opt, char* optarg, char* prog) {
    int rtn, err=0;
    FILE* in;

    switch (opt) {

    case 'r': 						            /* RNG seed */
        rtn = rng_seed_deseri (optarg, &rng_seed);	/* can be interpreted as seed */
        if (rtn) {
            rng_seed_given = 1;
            break; 
        }
        if (strcmp ("time", optarg) == 0) { 	/* given the time keyword */
            rng_seed_time(&rng_seed); 
            rng_seed_given = 1;
            break; 
        }
        in = fopen (optarg, "r");               /* must be filename */
        if (!in) { 
            perror (prog); 
            err++; 
            break;
        }
        rtn = rng_seed_read (in, &rng_seed);
        if (!rtn) { 
            fprintf (stderr, "%s: RNG seed in %s incorrect\n", prog, optarg); 
            err++;
            break; 
        }
        fclose (in);
        rng_seed_given = 1;
        break;

    case 'R':                                   /* RNG status given */
        rtn = rng_state_deseri(optarg, &rng_state);     /* is of the correct format */
        if (!rtn) {
            in = fopen (optarg, "r");			/* must be filename */
            if (!in) { 
                perror (prog); 
                err++; 
                break;
	        }
            rtn = rng_state_read (in, &rng_state);
            if (!rtn) { 
                fprintf (stderr, "%s: RNG status in %s incorrect\n", prog, optarg); 
                err++; 
            }
            fclose (in);
        }
        rng_state_given = 1;
        break;
         
    case 's': begsts = optarg;				/* save status at the beginning */
        break;

    case 'S': endsts = optarg;				/* save status at the end */
        break;

    default: break;
    }
    return (err == 0);
}

#define DEFAULT_SEED 0x55AA55AA55AA55AAULL

int rng_apply_options (char* prog) {
    FILE* out; int err=0;
    rng_state_t state;

    if (rng_state_given) {       			/* if given, state has priority */
        rng_set_state (&rng_state);
    } else if (rng_seed_given) {    			/* else seed given */
        rng_set_seed (rng_seed);
    } else {
        rng_set_seed (DEFAULT_SEED);         		/* else a constant seed as usual */ 
    }
    
    if (begsts) {
        out = fopen (begsts, "w");
        if (!out) { 
            perror (prog); err++; 
        } else {
            rng_get_state(&state);
            rng_state_write(out, &state); 
            fclose(out);
        }
    }      
    return (err == 0);
}

int rng_end_options (char* prog) {
    FILE* out; int err=0;
    rng_state_t state;
    
    if (endsts) {
        out = fopen (endsts, "w");
        if (!out) { 
            perror (prog); err++; 
        } else {
            rng_get_state(&state);
            rng_state_write(out, &state); 
            fclose(out);
        }
    }      
    return (err == 0);
}

char rng_synopsis[]=
"\tRNG control\n"
"\t-r <long seed> | time | <file>   seed from a number (64bit), time, file\n"
"\t-R <hex status> | <file>         rng state from string 0xaa,0xbb,0xcc,0xdd\n"
"\t                                 (4 64-bit numbers)\n"
"\t-s <file>                        state to file at the beginning\n"
"\t-S <file>                        state to file at the end\n";


