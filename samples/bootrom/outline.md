# Dependencies

1. `sudo apt install git cmake build-essential`
1. download/extract binaryninja
1. switch to dev branch/update

# Setting up your enviornment

## Get the binary we'll be working on

To avoid copyright concerns, we do not distribute this bundle with the binary we will be analyzing. Rather, please visit [cisco's website](https://software.cisco.com/download/home/283019669/type/282463181/release/1.4.1.03
And download the first link for: Sx300_FW_Boot_1.4.1.03.zip) to download the file.

```
$ shasum -a 256 Sx300_FW_Boot_1.4.1.03.zip
0382c4c8e328219bbf443fc97a409a978da7f5c8c51ada9b63d2cf818f157892  Sx300_FW_Boot_1.4.1.03.zip
```

Unzip, we'll be using:  `sx300_boot-13506.rfb`

## Get ready to patch the official BinaryNinja ARMv7 Plugin

Now, in a new/empty directory:

```
git clone https://github.com/Vector35/arch-armv7.git
git clone https://github.com/Vector35/binaryninja-api.git
export BN_API_PATH=$PWD/binaryninja-api
cp ~/binaryninja/libbinaryninja* arch-armv7/ #adjust path as appropriate
```

# Writing your patch

This is a two-part problem; first you need to write a BinaryView to load the Cisco Boot image (described in bootrom_outline.py), and second you need to patch the official ARMv7 plugin to lift a unique code pattern found in the image (described below):

This binary uses a rather strange pattern for some calls, and results in constructs equivalent to function calls being treated as block-ending events. Fortunately, it's possible to step in and augment Binary Ninja's existing lifters to cover extremely target specific quirks like this one.

What is the byte pattern we want to intercept and adjust behavior on?

We care about overriding a *very* specific instruction sequence, namely
`mov lr, pc; mov pc, r12` which behaves like a function call.

1. First assemble the snippet above.
1. Set MaxInstructionLength to 8 so we can cheat and check against two instructions
1. Implement `bool is_fake_call(const uint8_t *data)` detecting if it matches that pattern
1. In `Armv7Architecture::GetInstructionInfo`, if the data matches, change the result length to `8`.
1. In `Armv7Architecture::GetInstructionLowLevelIL`, add an instruction to the `il` object including a `Call` to a `Register` (specifically `REG_R12`).


# Building

```
cd arch-armv7
cmake .
make #-j core_count
```

# Installing

1. Launch BinaryNinja
1. Open Settings
1. Disable the ARMv7 Architecture core plugin
1. Tools > Open Plugin Folder
1. sym-link (or copy) the `libarch_armv7.*` you built to here
1. sym-link (or copy) bootrom.py as well
1. Restart BinaryNinja
