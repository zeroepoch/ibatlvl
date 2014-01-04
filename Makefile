#
# iOS Console Battery Level
#

TARGET = ibatlvl
OBJECTS = main.o

CC = clang
LD = $(CC)

ARCH_NAME = armv7s
PLAT_NAME = iPhoneOS.platform
SDK_NAME = iPhoneOS7.0.sdk

# platform/sdk paths
XCODE_BASE = /Applications/Xcode.app/Contents
PLAT_BASE = $(XCODE_BASE)/Developer/Platforms/$(PLAT_NAME)
SDK_BASE = $(PLAT_BASE)/Developer/SDKs/$(SDK_NAME)

# arch specific flags
ARCH_CFLAGS = -arch $(ARCH_NAME) -isysroot $(SDK_BASE)
ARCH_LDFLAGS = $(ARCH_CFLAGS)

CFLAGS = $(ARCH_CFLAGS) -g -Wall -Werror -O3
LDFLAGS = $(ARCH_LDFLAGS) -framework Foundation -framework IOKit

# default target
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

clean:
	rm -f $(OBJECTS) $(TARGET)
