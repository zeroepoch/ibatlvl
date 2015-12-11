#!/usr/bin/env python
#
# To prepare the debugserver for the iOS device see:
#   http://iphonedevwiki.net/index.php/Debugserver
#

import sys
import argparse

# lldb python path
LLDB_PYPATH = "/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/A/Resources/Python"

# target parameters
TARGET_PLATFORM = "remote-ios"
REMOTE_URL = "connect://localhost:2159"

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--binary',
    help='set binary being debugged on target')
parser.add_argument('-s', '--symbol',
    help='run until symbol before dumping')
parser.add_argument('-l', '--limit', type=int,
    help='limit number of instructions traced')
parser.add_argument('-t', '--triple', default='arm64',
    help='target architecture for the binary')
args = parser.parse_args()

# format target triple
target_triple = args.triple + "-apple-ios"

# check if symbol is usable
if args.symbol and not args.binary:
    sys.stderr.write(
        "Error: Symbol argument given without binary argument!\n\n")
    parser.print_help()
    sys.exit(1)

# import lldb library
sys.path.append(LLDB_PYPATH)
import lldb

# create new debugger connection
lldb.debugger = lldb.SBDebugger.Create()
lldb.debugger.SetAsync(False)

# get reusable lldb vars
error = lldb.SBError()
listener = lldb.debugger.GetListener()

# setup lldb platform/target
lldb.target = lldb.debugger.CreateTarget(
    args.binary, target_triple, TARGET_PLATFORM, True, error)
if not lldb.target.IsValid() or not error.Success():
    sys.stderr.write(
        "Error: Failed to setup lldb platform/target!\n")
    sys.exit(1)

# connect to remote target
lldb.process = lldb.target.ConnectRemote(listener, REMOTE_URL, None, error)
if not lldb.process.IsValid() or not error.Success():
    sys.stderr.write(
        "Error: Failed to connect to remote target!\n")
    sys.exit(1)

# get active (only) thread
lldb.thread = lldb.process.GetSelectedThread()
if not lldb.thread.IsValid():
    sys.stderr.write(
        "Error: Failed to get currently active thread!\n")
    sys.exit(1)

# run until entry symbol
if args.symbol:
    breakpoint = lldb.target.BreakpointCreateByName(args.symbol)
    lldb.process.Continue()  # avoid dyld loop during first iter
    lldb.process.Continue()

# save start address
start_addr = lldb.thread.GetSelectedFrame().addr

insnCount = 0

while True:

    # disasm next instruction
    lldb.frame = lldb.thread.GetSelectedFrame()
    insn = lldb.target.ReadInstructions(lldb.frame.addr, 1)[0]

    insnCount += 1

    # print instruction trace line
    print "%8d: %s" % (insnCount, insn)

    # step next instruction
    lldb.thread.StepInstruction(False)
    if lldb.thread.stop_reason != lldb.eStopReasonPlanComplete:
        break
    if lldb.thread.GetSelectedFrame().addr == start_addr:  # repeat
        break

    # check if instruction limit reached
    if args.limit and (insnCount == args.limit):
        break

sys.stderr.write("Trace Complete!\n")

# vim: ai et ts=4 sts=4 sw=4
