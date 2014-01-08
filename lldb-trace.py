#!/usr/bin/env python

import sys
import argparse

# lldb python path
LLDB_PYPATH = "/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/A/Resources/Python"

# target parameters
TARGET_TRIPLE = "armv7s-apple-ios"
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
args = parser.parse_args()

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
    args.binary, TARGET_TRIPLE, TARGET_PLATFORM, True, error)
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
    lldb.process.Continue()

insnCount = 0

while True:

    # disasm next instruction
    lldb.frame = lldb.thread.GetSelectedFrame()
    insn = lldb.target.ReadInstructions(lldb.frame.addr, 1)[0]

    # step next instruction
    lldb.thread.StepInstruction(False)
    if lldb.thread.stop_reason != lldb.eStopReasonPlanComplete:
        break

    insnCount += 1

    # print instruction trace line
    print "%8d: %s" % (insnCount, insn)

    # check if instruction limit reached
    if args.limit and (insnCount == args.limit):
        break

# vim: ai et ts=4 sts=4 sw=4
