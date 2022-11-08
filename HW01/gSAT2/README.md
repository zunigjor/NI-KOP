## Synapse
`gsat [-p probability] [-T maxtries] [-i maxiter] [-d datafile] [-w width] [-D] [-t tracefile] [PRNG-options] [-e] [cnf-file]`

## Parametry

| Parametr | Povinný | Implicitní hodnota | Typ hodnoty     | Význam                                                                                                                                                                                                 |
|----------|---------|--------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-p`     | ne      | 0.4                | desetinné číslo | Pravděpodobnost, že se v dané iteraci udělá náhodný krok                                                                                                                                               |
| `-T`     | ne      | 1                  | celé číslo      | Max. počet restartů; 0 znamená bez omezení                                                                                                                                                             |
| `-i`     | ne      | 300                | celé číslo      | Max. počet iterací; 0 znamená bez omezení                                                                                                                                                              |
| `-d`     | ne      |                    | jméno souboru   | Pokud je zadán, soubor s řádky tvaru číslo iterace počet splněných klauzulí. Hodnota - znamená standardní chybový výstup. Hodí se pro sledování vývoje řešení. Dá se zobrazit programy, např. gnuplot. |
| `-w`     | ne      | 3                  | celé číslo      | Pokud se instance čte ze standardního vstupu, je třeba dopředu znát max. počet literálů v klauzuli. Používejte vstup ze souboru.                                                                       |
| `-D`     | ne      |                    |                 | Pokud zadán, výstup ladicích informací                                                                                                                                                                 |
| `-t`     | ne      |                    | jméno souboru   | Pokud je zadán, soubor s detailními informacemi o rozhodování algoritmu po jednotlivých iteracích. Hodnota - znamená standardní chybový výstup. Hodí se pro pochopení algoritmu na malých instancích.  |
| `-e`     | ne      |                    |                 | Pokud zadán, výstupní hodnoty jsou odděleny středníkem (na žádost uživatelů, kteří se nechtějí dohadovat s Excelem o oddělovačích)                                                                     |

## Řízení generátoru pseudonáhodných čísel
Program má vlastní PRNG, do kterého jsem dodělal možnosti řízení, aby chod byl opakovatelný, když je to třeba. PRNG nemá kryptografické vlastnosti, je určen pro generování velkého množství dat pro experimenty. Řídí se to následujícími parametry:

| Parametr | Povinný | Implicitní hodnota   | Typ hodnoty                                        | Význam                                                                                                                                                                                                                                                                                                                                            |
|----------|---------|----------------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-r`     | ne      | `0x55AA55AA55AA55AA` | `time` / 64bit-hex / filename                      | Seed generátoru. Pokud je uvedeno klíčové slovo time, bere se seed z fce gettimeofday() nebo ekvivalentu; pokud se argument dá interpretovat jako 64-bitové hexadecimální číslo, bere se číslo; jinak se argument považuje za jméno souboru, ve kterém je zapsáno 64-bitové číslo. Počáteční stav generátoru je ze seedu odvozován pomocným PRNG. |
| `-R`     | ne      |                      | 64bit-hex,64bit-hex,64bit-hex,64bit-hex / filename | Počáteční stav generátoru - nezaměňovat se seedem. Buď čteřice 64-bitových čísel oddělených čárkami, nebo jméno souboru se stejným obsahem.                                                                                                                                                                                                       |
| `-s`     | ne      |                      | filename                                           | Uschovat stav generátoru do souboru na začátku (před generováním prvého čísla).                                                                                                                                                                                                                                                                   |
| `-S`     | ne      |                      | filename                                           | Uschovat stav generátoru do souboru na konci (po generování posledního čísla).                                                                                                                                                                                                                                                                    |
Pokud není zadáno žádné řízení, generátor se spouští s vestavěným konstantním seedem.

## Vstup
Vstupem je formule ve tvaru CNF, ve zjednodušeném standardním formátu DIMACS

## Výstup
Po skončení program vypíše na standardní chybový výstup informace ve tvaru počet-iterací, splněných klauzulí, všech klauzulí, oddělé středníky nebo mezerami. Na standardní výstup se vypíše konečná konfigurace ve standardním formátu. Další informace jsou v souborech datafile a tracefile, poku vyžádány.

## Návratová hodnota
0 (true), pokud proběhl výpočet (i při ukončení signálem SIGINT), 1 (false) při chybě v parametrech nebo vstupním souboru.
