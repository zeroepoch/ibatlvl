/*
 * iOS Console Battery Level
 *
 * Copyright (c) 2014, Eric Work
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 *
 *   Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#import <stdio.h>

#import <Foundation/Foundation.h>

#import "IOPowerSources.h"
#import "IOPSKeys.h"

/*
 * Gets percentage battery remaining
 */
double batteryLevel () {

    double percent = -1.0f;

    CFTypeRef psInfo = IOPSCopyPowerSourcesInfo();
    CFArrayRef psList = IOPSCopyPowerSourcesList(psInfo);

    // check number of sources
    CFIndex numSources = CFArrayGetCount(psList);
    if (numSources == 0)
        fprintf(stderr, "Error: No power sources found!\n");

    // iterate over sources
    for (CFIndex i = 0 ; i < numSources ; i++) {

        // get source description
        CFTypeRef psItem = CFArrayGetValueAtIndex(psList, i);
        CFDictionaryRef psDict = IOPSGetPowerSourceDescription(psInfo, psItem);
        if (psDict == NULL) {
            fprintf(stderr, "Error: Failed to get power source description!\n");
            continue;
        }

        const void *psVal;
        int curCapacity = 0;
        int maxCapacity = 0;

        // get current capacity
        psVal = CFDictionaryGetValue(psDict, CFSTR(kIOPSCurrentCapacityKey));
        CFNumberGetValue((CFNumberRef)psVal, kCFNumberIntType, &curCapacity);

        // get maximum capacity
        psVal = CFDictionaryGetValue(psDict, CFSTR(kIOPSMaxCapacityKey));
        CFNumberGetValue((CFNumberRef)psVal, kCFNumberIntType, &maxCapacity);

        // calc percentage remaining
        percent = ((double)curCapacity / (double)maxCapacity) * 100.0f;

        break;
    }

    // free resources
    CFRelease(psList);
    CFRelease(psInfo);

    return percent;
}

int main (int argc, const char *argv[]) {

    // print battery percentage
    double batLvl = batteryLevel();
    printf("Battery Level = %.0f\n", batLvl);

    return 0;
}
