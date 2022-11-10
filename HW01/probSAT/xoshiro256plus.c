/*  Written in 2018 by David Blackman and Sebastiano Vigna (vigna@acm.org)

To the extent possible under law, the author has dedicated all copyright
and related and neighboring rights to this software to the public domain
worldwide. This software is distributed without any warranty.

See <http://creativecommons.org/publicdomain/zero/1.0/>. */
#if defined(__MINGW32__) || defined(__MINGW64__)
#undef __USE_MINGW_ANSI_STDIO
#define __USE_MINGW_ANSI_STDIO 1
#endif

#ifdef _MSC_VER
#pragma warning(disable: 4244)
#endif
#include <inttypes.h>
#include <math.h>
#include "xoshiro256plus.h"

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


static inline uint64_t rotl(const uint64_t x, int k) {
	return (x << k) | (x >> (64 - k));
}

/* static uint64_t s[4]; */
static rng_state_t state;

void rng_set_state_uint (uint64_t s0, uint64_t s1, uint64_t s2, uint64_t s3) {
	state.s[0] = s0;
	state.s[1] = s1;
	state.s[2] = s2;
	state.s[3] = s3;
}

void rng_set_state (rng_state_t* pstate) {
	state.s[0] = pstate->s[0];
	state.s[1] = pstate->s[1];
	state.s[2] = pstate->s[2];
	state.s[3] = pstate->s[3];
}

void rng_get_state (rng_state_t* pstate) {
	pstate->s[0] = state.s[0];
	pstate->s[1] = state.s[1];
	pstate->s[2] = state.s[2];
	pstate->s[3] = state.s[3];
} 

void rng_set_seed(uint64_t seed) {
    /* seeding the aux generator */
    splitmix64_set_seed (seed);

    /* setting the main generator */
    rng_set_state_uint (
	splitmix64_next(), 
	splitmix64_next(), 
	splitmix64_next(), 
	splitmix64_next());
}

#define P64 "%#018" PRIX64

int  rng_state_seri (char* serial, rng_state_t* pstate) {
    snprintf (serial, RNG_STATE_CHARS,
        P64 "," P64 "," P64 "," P64,
	pstate->s[0], pstate->s[1], pstate->s[2], pstate->s[3]);
    return 1;
}
int  rng_state_write  (FILE* out, rng_state_t* pstate) {
    fprintf (out,
        P64 "," P64 "," P64 "," P64 "\n",
	pstate->s[0], pstate->s[1], pstate->s[2], pstate->s[3]);
    return 1;
}

#define S64 "%"  SCNx64

int  rng_state_deseri   (char* serial, rng_state_t* pstate) {
    return (sscanf (serial,
        S64 ", " S64 ", " S64 ", " S64,
	&pstate->s[0], &pstate->s[1], &pstate->s[2], &pstate->s[3]) == 4);
}
int  rng_state_read   (FILE* in,  rng_state_t* pstate) {
    return fscanf (in,
        S64 ", " S64 ", " S64 ", " S64,
	&pstate->s[0], &pstate->s[1], &pstate->s[2], &pstate->s[3]);
} 


uint64_t rng_next(void) {
	const uint64_t result_plus = state.s[0] + state.s[3];

	const uint64_t t = state.s[1] << 17;

	state.s[2] ^= state.s[0];
	state.s[3] ^= state.s[1];
	state.s[1] ^= state.s[2];
	state.s[0] ^= state.s[3];

	state.s[2] ^= t;

	state.s[3] = rotl(state.s[3], 45);

	return result_plus;
}


/* This is the jump function for the generator. It is equivalent
   to 2^128 calls to rng_next(); it can be used to generate 2^128
   non-overlapping subsequences for parallel computations. */

void rng_jump(void) {
	static const uint64_t JUMP[] = { 0x180ec6d33cfd0aba, 0xd5a61266f0c9392c, 0xa9582618e03fc9aa, 0x39abdc4529b1661c };

	uint64_t s0 = 0;
	uint64_t s1 = 0;
	uint64_t s2 = 0;
	uint64_t s3 = 0;
	for(int i = 0; i < sizeof JUMP / sizeof *JUMP; i++)
		for(int b = 0; b < 64; b++) {
			if (JUMP[i] & UINT64_C(1) << b) {
				s0 ^= state.s[0];
				s1 ^= state.s[1];
				s2 ^= state.s[2];
				s3 ^= state.s[3];
			}
			rng_next();	
		}
		
	state.s[0] = s0;
	state.s[1] = s1;
	state.s[2] = s2;
	state.s[3] = s3;
}


/* This is the long-jump function for the generator. It is equivalent to
   2^192 calls to rng_next(); it can be used to generate 2^64 starting points,
   from each of which jump() will generate 2^64 non-overlapping
   subsequences for parallel distributed computations. */

void rng_long_jump(void) {
	static const uint64_t LONG_JUMP[] = { 0x76e15d3efefdcbbf, 0xc5004e441c522fb3, 0x77710069854ee241, 0x39109bb02acbe635 };

	uint64_t s0 = 0;
	uint64_t s1 = 0;
	uint64_t s2 = 0;
	uint64_t s3 = 0;
	for(int i = 0; i < sizeof LONG_JUMP / sizeof *LONG_JUMP; i++)
		for(int b = 0; b < 64; b++) {
			if (LONG_JUMP[i] & UINT64_C(1) << b) {
				s0 ^= state.s[0];
				s1 ^= state.s[1];
				s2 ^= state.s[2];
				s3 ^= state.s[3];
			}
			rng_next();	
		}
		
	state.s[0] = s0;
	state.s[1] = s1;
	state.s[2] = s2;
	state.s[3] = s3;
}

/* This is a fixed-increment version of Java 8's SplittableRandom generator
   See http://dx.doi.org/10.1145/2714064.2660195 and 
   http://docs.oracle.com/javase/8/docs/api/java/util/SplittableRandom.html

   It is a very fast generator passing BigCrush, and it can be useful if
   for some reason you absolutely want 64 bits of state; otherwise, we
   rather suggest to use a xoroshiro128+ (for moderately parallel
   computations) or xorshift1024* (for massively parallel computations)
   generator. */

static uint64_t x; /* The state can be seeded with any value. */

uint64_t splitmix64_next() {
	uint64_t z = (x += 0x9e3779b97f4a7c15);
	z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9;
	z = (z ^ (z >> 27)) * 0x94d049bb133111eb;
	return z ^ (z >> 31);
}
void splitmix64_set_seed (uint64_t seed) {
	x = seed;
}
int  rng_seed_deseri (char* serial, rng_seed_t* pseed) {
    return sscanf (serial, " " S64, pseed);
}
int  rng_seed_seri   (char* serial, rng_seed_t* pseed) {
    snprintf (serial, RNG_SEED_CHARS, P64 "\n", *pseed);
    return 1;
}
int  rng_seed_read   (FILE* in,     rng_seed_t* pseed) {
    return fscanf (in, " " S64, pseed);
}
int  rng_seed_write  (FILE* out,    rng_seed_t* pseed) {
    fprintf (out, P64 "\n", *pseed);
    return 1;
}

double rng_next_double () {
    uint64_t r = rng_next();
    double   h = (r >> 38) << 27;   /* uppermost 26 bits, shifted */
    double   l = (r << 26) >> 37;   /* the following 27 bits */
/*  return (((long)next(26) << 27) + next(27)) / (double)(1LL << 53); */
    return (h + l) / (double)(1LL << 53);
}
/*-----------------------------------------------------------------------------
	transformation from (0,1) to (low .. high) inclusive
-----------------------------------------------------------------------------*/
unsigned rng_to_range (unsigned low, unsigned high, double val) {
    return round (val * (high-low+1) - 0.5 + low);
}

unsigned rng_next_range (unsigned low, unsigned high) {
    return round (rng_next_double() * (high-low+1) - 0.5 + low);
}
/*---------------------------------------------------------------------------*/
/* Fisher-Yates shuffle, aka Knuth shuffle 				     */
/*---------------------------------------------------------------------------*/
static inline unsigned uniform(unsigned m) { /* Returns a random integer 0 <= uniform(m) <= m-1 with uniform distribution */
    return rng_next_range (0, m-1);
}
/*---------------------------------------------------------------------------*/
static inline void swap (unsigned* pa, unsigned* pb) {
    unsigned x = *pa;
    *pa = *pb;
    *pb = x;
}
void rng_permute(unsigned permutation[], unsigned n)
{
    unsigned i, j;
    if (n<2) return;
    for (i = 0; i <= n-2; i++) {
        j = i+uniform(n-i); /* A random integer such that i ? j < n*/
        swap(&permutation[i], &permutation[j]);   /* Swap the randomly picked element with permutation[i] */
    }
}
/*---------------------------------------------------------------------------*/
/* random numbers (0,1) in a given distribution                              */
/* the density function is from (0,1) to (0,1)                               */
/*---------------------------------------------------------------------------*/
double rng_next_dist (rng_density dfunc, void* par) {
    double cand, thr;
    do {
       cand = rng_next_double();
       thr = (*dfunc)(cand, par);
    } while (rng_next_double() > thr);
    return cand;
}
