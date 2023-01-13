import ctypes

from . import ReadWriteMemoryError


def _read(handle, lp_base_address:int, offset:int=0) -> bytes:
    """Read memory from a given address
        optionally with an offset from the base address
    """
    # apply offset, default is 0
    address = lp_base_address + offset

    # prepare the read buffer
    read_buffer = ctypes.c_uint()
    lp_buffer = ctypes.byref(read_buffer)
    n_size = ctypes.sizeof(read_buffer)
    lp_n_bytes_read = ctypes.c_ulong(0)

    try:
        # read the memory
        ctypes.windll.kernel32.ReadProcessMemory(
            handle, address, lp_buffer, n_size, ctypes.byref(lp_n_bytes_read)
        )