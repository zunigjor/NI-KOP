#ifndef XOSHIRO256PLUS_H
#define XOSHIRO256PLUS_H

/*  Written in 2018 by David Blackman and Sebastiano Vigna (vigna@acm.org)

To the extent possible under law, the author has dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. This software is distributed without any warranty.

See <http://creativecommons.org/publicdomain/zero/1.0/>. */

/* Hacks to provide better control by Jan Schmidt (schmidt@fit.cvut.cz) */

#include <stdint.h>
#include <stdio.h>

/* State structure, permitting to save and restore RNG state */

typedef struct {
    uint64_t s[4];
} rng_state_t;

typedef uint64_t rng_seed_t;

/* This is xoshiro256+ 1.0, our best and fastest generator for floating-point
   numbers. We suggest to use its upper bits for floating-point
   generation, as it is slightly faster than xoshiro256**. It passes all
   tests we are aware of except for the lowest three bits, which might
   fail linearity tests (and just those), so if low linear complexity is
   not considered an issue (as it is usually the case) it can be used to
   generate 64-bit outputs, too.

   We suggest to use a sign test to extract a random Boolean value, and
   right shifts to extract subsets of bits.

   The state must be seeded so that it is not everywhere zero. If you have
   a 64-bit seed, we suggest to seed a splitmix64 generator and use its
   output to fill s. */


uint64_t rng_next(void);

/* This is the jump function for the generator. It is equivalent
   to 2^128 calls to next(); it can be used to generate 2^128
   non-overlapping subsequences for parallel computations. */

void rng_jump(void);
/* This is the long-jump function for the generator. It is equivalent to
   2^192 calls to next(); it can be used to generate 2^64 starting points,
   from each of which jump() will generate 2^64 non-overlapping
   subsequences for parallel distributed computations. */


void rng_long_jump(void);

double rng_next_double ();
unsigned rng_to_range (unsigned low, unsigned high, double val);
unsigned rng_next_range (unsigned low, unsigned high);
void rng_permute(unsigned permutation[], unsigned n);

typedef double (*rng_density)(double arg, void* par);
double rng_next_dist (rng_density dfunc, void* par);

/* state manipulation functions */
void rng_set_state_uint (uint64_t s0, uint64_t s1, uint64_t s2, uint64_t s3); 
void rng_set_state (rng_state_t* pstate); 
void rng_get_state (rng_state_t* pstate); 
#define RNG_STATE_CHARS 76
int  rng_state_deseri (char*, rng_state_t*);
int  rng_state_seri   (char*, rng_state_t*);
int  rng_state_read   (FILE*, rng_state_t*);
int  rng_state_write  (FILE*, rng_state_t*);

/* seed manipulation functions */
void rng_set_seed(uint64_t seed); 
#define RNG_SEED_CHARS 20
int  rng_seed_deseri (char*, rng_seed_t*);
int  rng_seed_seri   (char*, rng_seed_t*);
int  rng_seed_read   (FILE*, rng_seed_t*);
int  rng_seed_write  (FILE*, rng_seed_t*);

/* the splitmix64 generator, mainly for seeding the main generator */
uint64_t splitmix64_next();
void splitmix64_set_seed (uint64_t seed);

#endif
