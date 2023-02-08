## Experimentální vyhodnocení algoritmu (15/15b)
Experimentálně srovnejte algoritmy GSAT a probSAT. Určete, který algoritmus dospěje rychleji (v menším počtu iterací) k řešení obtížných instancí 3-SAT v rozsahu 20-75 proměnných. Zdůvodněte použité metody a metriky, popište interpretaci dat.

Uvažujte pevné parametry:

* GSAT: p = 0.4
* probSAT: c<sub>m</sub> = 0, c<sub>b</sub> = 2.3
### Algoritmus probSAT
```
Procedure probSAT (formula F)
    for i := 1 to MAX-TRIES
        T := a randomly generated truth assignment
        for j := 1 to MAX-FLIPS
            if T satisfies F then return T
            randomly pick an unsatisfied clause in F
            randomly pick a variable in that clause,
                each variable x  has the probability proportional to f(x,F)
            flip the truth assignment of the chosen variable
        end for
    end for
    return "No satisfying assignment found"

function f (variable x, formula F)
    make := number of clauses which become satisfied after the flip of x
    break := number of clauses which cease to be satisfied after the flip of x

    return make^cm / (eps+break)^cb
```
cm a cb jsou parametry heuristiky. eps je malá hodnota, která zabraňuje dělení nulou. Existuje zjednodušená varianta `f(x,F)`, kde `cm == 0` a tudíž čitatel je 1.

Adrian Balint and Uwe Schöning. 2012. Choosing probability distributions for stochastic local search and the role of make versus break. In Proceedings of the 15th international conference on Theory and Applications of Satisfiability Testing (SAT'12). Springer-Verlag, Berlin, Heidelberg, 16–29. https://doi.org/10.1007/978-3-642-31612-8_3
