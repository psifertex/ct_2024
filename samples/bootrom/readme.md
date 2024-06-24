# Goals

- Create a loader and architecture extension/modification for the following firmware: [https://software.cisco.com/download/home/283019669/type/282463181/release/1.4.1.03](https://software.cisco.com/download/home/283019669/type/282463181/release/1.4.1.03)

```
$ wget https://v35.us/k06l85e (Sx300_FW_Boot_1.4.1.03.zip)
$ unzip Sx300_FW_Boot_1.4.1.03.zip
$ shasum -a 256 Sx300_FW_Boot_1.4.1.03.zip
605d0c71bd76f0af0bf7cba7f98f7a7787b38e61f502f609fa99afd6f053683d
```

- Instructions on building the replacement architecture are in [Outline.md](Outline.md).
- [bootrom_outline.py](bootrom_outline.py) contains instructions for building a BinaryView loader
