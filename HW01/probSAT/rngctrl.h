#ifndef KG_RNGCTRL 
#define KG_RNGCTRL

#include "xoshiro256plus.h"

int rng_options (int opt, char* optarg, char* prog);
int rng_apply_options (char* prog);
int rng_end_options (char* prog);
extern char rng_synopsis[];

#endif
