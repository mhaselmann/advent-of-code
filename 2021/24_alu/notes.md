*) first try brute force with smaller numbers and check up the frequency of right numbers
*) lookup table for all combinations of inp 1-9 and start values of z --> value: result z
*) 999999999abcjdgf ... try to find shortest tail digits pattern with the at least significant digit z=0, all other leading digits are 9s
--> this approach would also find 
 --> 1st try pattern length 1: 98, 97, 96, 95, 94, 93, 92, 91 
 --> 2nd try pattern length 2: 989, 988, 987, ... 913, 912, 911
 --> 3rd try pattern length 3: 9899, 9898, 9897 ... 9113
*) backward search: of right numbers those entries the show z=0 are possible starting nodes for least significant digit 


* div z 1 --> increases up to factor (for initial_z > 0)
* diz z 26 --> decrases up to factor 26 only if x can be zeroed