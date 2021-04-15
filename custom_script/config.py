'''
Problem Statement: Run a benchmark program on different system configurations on gem5 and analyse the output statistics of each of these config combinations to 
                   select top 10 combinations.
                   
Subject Name: High Performance Computer Architecture(CS60003)
Semester: Spring 2021
Assignment No. : 01
Submitted By: Group-I (Benchmark program - (towers.c) )

'''



# HEADER FILES
from __future__ import print_function
from __future__ import absolute_import

import optparse, sys, os, m5
import m5

from m5.defines import buildEnv
from m5.objects import *

from common.Benchmarks import *
from common import ObjectList



# Setting variable values as given in assignment point 2
class fixed_variables:
    # FIXED PARAMETERS
    CPU_MODEL = DerivO3CPU
    CLOCK_FREQ = '2GHz'
    MEM_MODE = 'timing'
    MEM_SIZE = '1GB'
    MEM_TYPE = DDR3_1600_8x8
    NUM_ROB = 1
    L1_TAG_LATENCY = 2
    L1_DATA_LATENCY = 2
    L1_RESPONSE_LATENCY = 2
    L1_MSHRS = 4
    L1_TGSTS_PER_MSHR = 20
    L2_TAG_LATENCY = 20
    L2_DATA_LATENCY = 20
    L2_RESPONSE_LATENCY = 20
    L2_MSHRS = 20
    L2_TGSTS_PER_MSHR = 12
    CACHE_LINE = 64

    # Providing VARIBALE parameters
    L1D_SIZE = ['32kB', '64kB']
    L1I_SIZE = ['32kB', '64kB']
    L2_SIZE = ['128kB', '256kB', '512kB']
    L1_ASSOC = [2, 4, 8]
    L2_ASSOC = [4, 8]
    BP_TYPE = [TournamentBP, BiModeBP, LocalBP]
    LQ_ENTRIES = [16, 32, 64]
    SQ_ENTRIES = [16, 32, 64]
    ROB_ENTRIES = [128, 192]
    IQ_ENTRIES = [16, 32, 64]

# variable to store configuration
ct =  fixed_variables()
 
class L1Cache(Cache):
    assoc = 2
    tag_latency = ct.L1_TAG_LATENCY
    data_latency = ct.L1_DATA_LATENCY
    response_latency = ct.L1_RESPONSE_LATENCY
    mshrs = ct.L1_MSHRS
    tgts_per_mshr = ct.L1_TGSTS_PER_MSHR


class L1_ICache(L1Cache):
    is_read_only = True
    writeback_clean = True

class L1_DCache(L1Cache):
    pass

class L2Cache(Cache):
    assoc = 8
    tag_latency = ct.L2_TAG_LATENCY
    data_latency = ct.L2_DATA_LATENCY
    response_latency = ct.L2_RESPONSE_LATENCY
    mshrs = ct.L2_MSHRS
    tgts_per_mshr = ct.L2_TGSTS_PER_MSHR
    write_buffers = 8

class crawl_pt(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 10
    size = '1kB'
    tgts_per_mshr = 12
    is_read_only = False

def configure_cache(system):
    # Set the cache classes    
    dcache_class = L1_DCache
    icache_class = L1_ICache
    l2_cache_class = L2Cache
    walk_cache_class = crawl_pt

    # Set the cache line size of the system
    system.cache_line_size = 64

    #L2 Cache
    system.l2 = l2_cache_class(clk_domain=system.cpu_clk_domain,size=L2_SIZE,assoc=L2_ASSOC)

    system.tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
    system.l2.cpu_side = system.tol2bus.master
    system.l2.mem_side = system.membus.slave

    # L1 Cache
    icache = icache_class(size=L1I_SIZE, assoc=L1_ASSOC)
    dcache = dcache_class(size=L1D_SIZE, assoc=L1_ASSOC)
    iwalkcache = walk_cache_class()
    dwalkcache = walk_cache_class()

    # Connect caches to the cput
    system.cpu.addPrivateSplitL1Caches(icache, dcache, iwalkcache, dwalkcache)
    system.cpu.createInterruptController()
    system.cpu.connectAllPorts(system.tol2bus, system.membus)


def configure_mem(system):
    # Create interface
    r = system.mem_ranges[0]
    dram_intf = ct.MEM_TYPE()
    dram_intf.range = m5.objects.AddrRange(r.start, size = r.size())

    # Memory Controller
    mem_ctrl = m5.objects.MemCtrl()
    mem_ctrl.dram = dram_intf
    mem_ctrl.port = system.membus.master

    system.mem_ctrls = [mem_ctrl]


def run_simulation():
    m5.instantiate()
    print("**** REAL SIMULATION ****")
    exit_event = m5.simulate()
    print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
    if exit_event.getCode() != 0:
        print("Simulated exit code not 0! Exit code is", exit_event.getCode())


# Parse Args
def parse_arg():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--cmd", default="",help="The binary to run in syscall emulation mode.")
    parser.add_option("-a", "--args", default="1111111111",help="Choosing the different args")
    (options, args) = parser.parse_args()

    # Arguments
    global L1D_SIZE
    L1D_SIZE = ct.L1D_SIZE[int(options.args[0]) - 1]
    global L1I_SIZE
    L1I_SIZE = ct.L1I_SIZE[int(options.args[1]) - 1]
    global L2_SIZE
    L2_SIZE = ct.L2_SIZE[int(options.args[2]) - 1]
    global L1_ASSOC
    val = str(options.args)[3]
    L1_ASSOC = ct.L1_ASSOC[int(val) - 1]
    global L2_ASSOC
    L2_ASSOC = ct.L2_ASSOC[int(options.args[4]) - 1]
    global BP_TYPE
    BP_TYPE = ct.BP_TYPE[int(options.args[5]) - 1]
    global LQ_ENTRIES
    LQ_ENTRIES = ct.LQ_ENTRIES[int(options.args[6]) - 1]
    global SQ_ENTRIES
    SQ_ENTRIES = ct.SQ_ENTRIES[int(options.args[7]) - 1]
    global ROB_ENTRIES
    ROB_ENTRIES = ct.ROB_ENTRIES[int(options.args[8]) - 1]
    global IQ_ENTRIES
    IQ_ENTRIES = ct.IQ_ENTRIES[int(options.args[9]) - 1]

    # Process Creation
    if options.cmd:
        process = Process(pid = 101)
        process.executable = options.cmd
        process.cmd = [options.cmd]
        multiprocesses = [process]
    else:
        print("No workload specified. Exiting!\n", file=sys.stderr)
        sys.exit(1)

    return multiprocesses



def input_values():

    #Fixed Parameters
    multiprocesses = parse_arg()         

    system = System(cpu = ct.CPU_MODEL(),mem_mode = ct.MEM_MODE,mem_ranges = [AddrRange(ct.MEM_SIZE)],cache_line_size = ct.CACHE_LINE)

    # Create clock and voltage domains
    system.voltage_domain = VoltageDomain(voltage = '1V')
    system.clk_domain = SrcClockDomain(clock = ct.CLOCK_FREQ, voltage_domain = system.voltage_domain)
    system.cpu_voltage_domain = VoltageDomain()
    system.cpu_clk_domain = SrcClockDomain(clock = '2GHz', voltage_domain = system.cpu_voltage_domain)

    system.cpu.clk_domain = system.cpu_clk_domain   # Assign the domains to the CPU
    system.cpu.workload = multiprocesses[0]         # Create workload
    system.membus = SystemXBar()                    # Configure Memory
    system.system_port = system.membus.slave
    configure_mem(system)
    system.cpu.numRobs = ct.NUM_ROB

    # Variable Parameters
    system.cpu.LQEntries = LQ_ENTRIES
    system.cpu.SQEntries = SQ_ENTRIES
    system.cpu.numROBEntries = ROB_ENTRIES
    system.cpu.numIQEntries = IQ_ENTRIES
    system.cpu.branchPred = BP_TYPE()       # Configure BP and Cache
    system.cpu.createThreads()
    configure_cache(system)

    # Create root and run simulation
    root = Root(full_system = False, system = system)
    run_simulation()
    
input_values()
