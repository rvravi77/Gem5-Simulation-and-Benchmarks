Subject Name: High Performance Computer Architecture(CS60003)
Semester: Spring 2021
Assignment No. : 01
Submitted By: Group-I (Benchmark program - (towers.c) )

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

Problem Statement: Run a benchmark program on different system configurations on gem5 and analyse the output statistics of each of these config combinations to 
                   select top 10 combinations.

IMPLEMENTATION :The benchmark program towers.c was run on the Linux System where we have the Gem5 installed. 

How to run? :

Note: Custom scripts(config.py and script.py) are available in 'custom script' folder of submitted file(I_HPCA_ASSIGNMENT_1.tar.gz).

To run scripts on your own system do following:

1. script.py runs top 10 configurations that are hardcoded in it &
   also contains code(commented) for running all possible combinations.
2. Make path changes in line 13-23 in script.py according to the comments given.
3. Run script.py as : ~$ python3 script.py 
4. stats.txt created in 'm5out/SIMnum'directory.

******************************************************************************************************************************************************************
