iBatLvl
======

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
