'''
Problem Statement: Run a benchmark program on different system configurations on gem5 and analyse the output statistics of each of these config combinations to 
                   select top 10 combinations.
                   
Subject Name: High Performance Computer Architecture(CS60003)
Semester: Spring 2021
Assignment No. : 01
Submitted By: Group-I (Benchmark program - (towers.c) )

'''

import os
  #output directory where stats.txt will be stores
m5out="/home/user/I_HPCA_ASSIGNMENT_1/m5out/"  

 #gem.opt location                                  
BUILDDIR="/home/user/gem5/build/X86/gem5.opt"    

 #custom config script location
SCRIPT="/home/user/I_HPCA_ASSIGNMENT_1/custom_script/config.py" 

 #executable file location        
CODE="/home/user/I_HPCA_ASSIGNMENT_1/custom_script/towers"                       

top_10 = ['2223211323',
          '2223211313',
          '2113111313',
          '2231111323',
          '1122111323',
          '2231111313',
          '1221211323',
          '1121211313',
          '1121211323',
          '2223211213']

count = 0
for args in top_10:
    count+=1
    command = BUILDDIR + " --outdir=" + m5out +"SIMnum-" + str(count) + "_arg-" + str(args) + " " +SCRIPT+ " " +  "--cmd=" + CODE + " --args=" + args
    os.system(command)

#for running entire simulation 
"""
variables=[3 ,2 ,3 ,3 ,3 ,2 ,3 ,3 ,2 ,2] 
for i in range (0,11664):
    tmp=i
    args=""
    for s in variables:
        rem= int(tmp) % int(s)
        rem= rem + 1 
        tmp= tmp / s  
        args= str(rem)+str(args)
    command = BUILDDIR + " --outdir=" + m5out +"SIMnum-" + str(i) + "_args-" + str(args) + " " +SCRIPT+ " " +  "--cmd=" + CODE + " --args=" + args
    #print(command)
    os.system(command)
    print("Sim Number",i," Done")
"""
