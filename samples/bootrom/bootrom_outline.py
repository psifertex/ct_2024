import traceback
from binaryninja import *

class CiscoBoot(BinaryView):
    name = "CiscoBoot"
    long_name = "Cisco Boot Rom"

    def __init__(self, data):
        BinaryView.__init__(self, file_metadata=data.file, parent_view=data)
        self.data = data

    @classmethod
    def is_valid_for_data(self, data):
        # we probably want to see if the first say, 12 bytes or so match something that looks like a cisco boot rom!
        return False

    def init(self):
        try:
            self.arch = Architecture['armv7']
            self.platform = Architecture['armv7'].standalone_platform

            # What we know: this binary expects to be mapped at 0x1800000 - we'll use 0x40000 as the size of the mapping
            # the first 0x10 bytes are header, so for the backing segment, we'll use a file_offset of 0x10
            # only 0x2fd00 bytes are actually mapped in from the file -- the rest are implicitly zero filled (.bss)
            # SEE: BinaryView.add_auto_segment

            # sections that we'll want:
            # .text at 0x1800000 (0x2b1c0 bytes) - ReadOnlyCodeSectionSemantics
            # .data at 0x182b1c0 (0x2fd00 - 0x2b1c0 bytes) - ReadWriteDataSectionSemantics
            # .bss at 0x182fd00 (0xf5d0 bytes)
            # SEE: BinaryView.add_auto_section

            # add an entry point, like the one we happen to know exists at 0x1800b4c
        except:
            log_error(traceback.format_exc())
            return False

        return True

    def perform_is_executable(self):
        return True

    def perform_get_entry_point(self):
        return self.entry_addr

    def perform_get_address_size(self):
        return 4

CiscoBoot.register()

