iBatLvl
=======

iOS Console Battery Level

This is a console application, meaning no GUI or launch icon. It requires a
jailbroken iPhone to run. When this program is executed it prints the battery
charge level once as a percent then quits.

In order to build this application you must have XCode installed and the
iOS 7.0 SDK, which should be included with XCode. Also see the prerequisites
below. To run the application type `make` then copy the `ibatlvl` executable
to your phone using SSH and run it.

This application was compiled on a MacMini running Mac OS X 10.9.1. The
application was tested on an iPhone 5s GSM running 7.0.4 with the evasi0n7
jailbreak.

Prerequisites
=============

Before you can use IOKit with iOS 7.0 you need to create the symlink below
which allows the compiler to find the IOKit framework during linking.

```
cd /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS7.0.sdk/System/Library/Frameworks/IOKit.framework
sudo ln -s Versions/A/IOKit
```

Headers
=======

The following headers were used to access the private APIs within IOKit on iOS.
These headers were copied from the desktop platform which fortunately uses the
same APIs.

* /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/System/Library/Frameworks/IOKit.framework/Headers/ps/IOPSKeys.h
* /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/System/Library/Frameworks/IOKit.framework/Headers/ps/IOPowerSources.h

Alternatives
============

The same information can actually be found using the `scutil` command.

```
$ scutil
> show State:/IOKit/PowerSources/InternalBattery-0
<dictionary> {
  Battery Provides Time Remaining : TRUE
  BatteryHealth : Good
  Current Capacity : 100
  DesignCycleCount : 300
  Is Charged : TRUE
  Is Charging : FALSE
  Is Present : TRUE
  Max Capacity : 100
  Name : InternalBattery-0
  Power Source State : AC Power
  Time to Empty : 0
  Time to Full Charge : 0
  Transport Type : Internal
  Type : InternalBattery
}
> quit
```

Debugger Script
===============

Mostly for my own reference, `lldb-trace.py` is a python script for instruction
tracing that uses lldb. The lldb client installed on the Mac desktop connects
to a remote debug server running on the iPhone. The steps below describe how to
prepare the `debugserver` for an iPhone 5s, how to start the `debugserver` on
the iPhone, and how to run the instruction tracing script on the Mac. See the
[iPhone Development Wiki](http://iphonedevwiki.net/index.php/Debugserver) for
additional information.

```
mac$ cd ~
mac$ scp mobile@<iphone_ip>:/Developer/usr/bin/debugserver ~/debugserver
mac$ /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/usr/bin/lipo -thin arm64 ~/debugserver -output ~/debugserver.arm64
mac$ scp ~/debugserver.arm64 mobile@<iphone_ip>:~/debugserver

ios$ cd ~
ios$ vim ent.xml  # see file ent.xml below
ios$ ldid -Sent.xml ~/debugserver
ios$ sudo cp ~/debugserver /usr/bin/debugserver
```

File: `ent.xml`

```
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.springboard.debugapplications</key>
    <true/>
    <key>get-task-allow</key>
    <true/>
    <key>task_for_pid-allow</key>
    <true/>
    <key>run-unsigned-code</key>
    <true/>
</dict>
</plist>
```

Start debugserver on the iPhone

```
ios$ debugserver 0.0.0.0:2159 <binary>
```

Run lldb python script on the Mac

```
mac$ ./lldb-trace.py -b <binary> -s main
       1: dyld[0x2be01028]:  mov    r8, sp
       2: dyld[0x2be0102c]:  sub    sp, sp, #16
       3: dyld[0x2be01030]:  bic    sp, sp, #7
       4: dyld[0x2be01034]:  ldr    r3, [pc, #112]
       5: dyld[0x2be01038]:  sub    r0, pc, #8
       6: dyld[0x2be0103c]:  ldr    r3, [r0, r3]
       7: dyld[0x2be01040]:  sub    r3, r0, r3
       8: dyld[0x2be01044]:  ldr    r0, [r8]
       9: dyld[0x2be01048]:  ldr    r1, [r8, #4]
      10: dyld[0x2be0104c]:  add    r2, r8, #8
```

The constants at the top of `lldb-trace.py`, such as the remote hostname, may
need to be modified to fit your environment.
