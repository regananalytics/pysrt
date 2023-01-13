from __future__ import annotations
import ctypes
import ctypes.wintypes
from enum import Enum
import logging
import os
from typing import Any,  List


log = logging.getLogger(__name__)

class ReadWriteMemoryError(Exception):
    pass


MAX_PATH = 260

class ProcessAccess:
    """Process Access Flags"""
    ALL_ACCESS = 0x1F0FFF
    CREATE_PROCESS = 0x0080
    CREATE_THREAD = 0x0002
    DUP_HANDLE = 0x0040
    QUERY_INFORMATION = 0x0400
    QUERY_LIMITED_INFORMATION = 0x1000
    SET_INFORMATION = 0x0200
    SET_QUOTA = 0x0100
    SUSPEND_RESUME = 0x0800
    TERMINATE = 0x0001
    VM_OPERATION = 0x0008
    VM_READ = 0x0010
    VM_WRITE = 0x0020
    SYNCHRONIZE = 0x00100000


## General Process Functions ##

def get_last_error() -> int:
    """Get the last error code"""
    return ctypes.windll.kernel32.GetLastError()


def _list_pids() -> List[int]:
    """List all pids of running processes"""
    buffer_size = 32 # Initial buffer size of 32
    while True:
        process_ids = (ctypes.wintypes.DWORD * buffer_size)()
        cb = ctypes.sizeof(process_ids)
        bytes_returned = ctypes.wintypes.DWORD()
        if ctypes.windll.Psapi.EnumProcesses(
            ctypes.byref(process_ids), cb, ctypes.byref(bytes_returned)
        ):
            if bytes_returned.value < cb:
                # Buffer was large enough to hold all pids
                return list(set(process_ids))
            else:
                # Double the buffer size and try again
                buffer_size *= 2


def _enum_procs(named_only:bool=True) -> dict:
    """Enumerate all running processes
        Returns a dictionary of the form {pid: process_name}
        If named_only is True, only processes with a name will be returned.
    """
    process_ids = _list_pids()
    proc_enum = dict.fromkeys(process_ids)
    for process_id in process_ids:
        proc_handle = ctypes.windll.kernel32.OpenProcess(
            ProcessAccess.QUERY_INFORMATION, False, process_id
        )
        if proc_handle:
            image_file_name = (ctypes.c_char * MAX_PATH)()
            filename = None
            if ctypes.windll.psapi.GetProcessImageFileNameA(
                proc_handle, image_file_name, MAX_PATH
            ) > 0:
                filename = os.path.basename(image_file_name.value).decode('utf-8')
                if not named_only or filename:
                    proc_enum[process_id] = filename
            ctypes.windll.kernel32.CloseHandle(proc_handle)
        if named_only and (not proc_handle or not filename):
            del proc_enum[process_id]
    return proc_enum



class Process(object):
    """Process Class
        This class is used to open a process and read and write to its memory.
    """    

    def __init__(self, name:str='', pid:int=-1, handle:int=-1, error_code:str=None):
        self.name = name
        self.pid = pid
        self.handle = handle
        self.error_code = error_code


    @staticmethod
    def by_name(process_name:str) -> Process:
        """Create a Process object from a process name"""
        proc_enum = _enum_procs()
        for pid, name in proc_enum.items():
            if name.lower().rstrip('.exe') == process_name.lower().rstrip('.exe'):
                return Process(name, pid)


    @staticmethod
    def by_pid(pid:int) -> Process:
        """Create a Process object from a pid"""
        proc_enum = _enum_procs()
        if pid in proc_enum:
            return Process(proc_enum[pid], pid)


    ## Process Attributes ##

    def get_modules(self) -> List[int]:
        """
        Get the process's modules.
        :return: A list of the process's modules adresses in decimal.
        :return: An empty list if the process is not open.
        """
        modules = (ctypes.wintypes.HMODULE * MAX_PATH)()
        ctypes.windll.psapi.EnumProcessModules(
            self.handle, modules, ctypes.sizeof(modules), None
        )
        return [hex(x) for x in tuple(modules) if x is not None]
    

    ## Open Methods ##

    def open(self):
        """Open the process
            with Query, Operation, Read, and Write access flags
        """
        dw_desired_access = (
            ProcessAccess.QUERY_INFORMATION \
            | ProcessAccess.VM_OPERATION \
            | ProcessAccess.VM_READ \
            | ProcessAccess.VM_WRITE
        )
        return self._open(dw_desired_access)


    def open_all_access(self):
        """Open the process with all access flags"""
        return self._open(ProcessAccess.ALL_ACCESS)


    def _open(self, access:ProcessAccess, inherit_handle:bool=True) -> int:
        """Open the process with the given access flags"""
        if not (handle := ctypes.windll.kernel32.OpenProcess(
            access, inherit_handle, self.pid
        )):
            raise ReadWriteMemoryError(f'Unable to open process: [{self.pid}] "{self.name}"')
        self.handle = handle
        return handle


    ## Read Methods ##

    def _read(self, lp_base_address:int, read_buffer, length:int=None, base_offset:int=0) -> bytes:
        """Read memory from a given address
            optionally with an offset from the base address
        """
        # apply offset, default is 0
        address = lp_base_address + base_offset

        # prepare the read buffer
        if length is None:
            length = ctypes.sizeof(read_buffer)
        lp_n_bytes_read = ctypes.c_ulong(0)

        try:
            # read the memory
            ctypes.windll.kernel32.ReadProcessMemory( self.handle,
                address, 
                read_buffer, 
                length, 
                lp_n_bytes_read
            )

        except (BufferError, ValueError, TypeError) as error:
            self._handle_read_error(error)


    def read_byte(self, lp_base_address:int, base_offset:int=0) -> int:
        """Read byte from the process's memory.
            Optionally, use an offset from the base address.
        """
        read_buffer = ctypes.c_ubyte()
        self._read(
            lp_base_address,
            ctypes.byref(read_buffer), 
            base_offset=base_offset
        )
        return read_buffer.value


    def read_lp(self, lp_base_address:int, base_offset:int=0) -> Any:
        """Read data from the process's memory.
            Optionally, use an offset from the base address.
        """
        read_buffer = ctypes.c_uint()
        self._read(
            lp_base_address, 
            ctypes.byref(read_buffer),
            ctypes.sizeof(read_buffer),
            base_offset=base_offset
        )
        return read_buffer.value


    def read_lp_chain(self, lp_base_address:int, lp_chain:List[int]=[], base_offset:int=0) -> int:
        """Follow a pointer chain to get the final value
            Optionally, use an offset from the base address.
            Presumably, the final value is an address, not the data itself.
        """
        if not lp_chain:
            return lp_base_address
        next_address = self.read_lp(lp_base_address, base_offset=base_offset)
        pointer = 0x0
        for offset in lp_chain:
            pointer = int(str(next_address), 0) + int(str(offset), 0)
            next_address = self.read_lp(pointer)
        return pointer


    def read_str(self, lp_base_address:int, length:int, base_offset:int=0) -> str:
        """Read string from the process's memory.
            Optionally, use an offset from the base address.
        """
        read_buffer = ctypes.create_string_buffer(length)
        self._read(
            lp_base_address, 
            read_buffer, 
            length=length,
            base_offset=base_offset
        )
        bufferArray = bytearray(read_buffer)
        if (found_terminator := bufferArray.find(b'\x00')) == -1:
            # No terminator found
            log.warning(f'No terminator found in string at address: {hex(lp_base_address)}')
            return ''
        # Return decoded string
        return bufferArray[:found_terminator].decode('utf-8')


    def _handle_read_error(self, error:Exception):
        """Handle read error"""
        # Close process
        if self.handle:
            self.close()
        # Get error code
        self.error_code = self.get_last_error()
        raise ReadWriteMemoryError({
            'msg': str(error), 
            'Handle': self.handle, 
            'PID': self.pid,
            'Name': self.name, 
            'ErrorCode': self.error_code
        })
        

    ## Write Methods ##

    def write(self, lp_base_address: int, value: int) -> bool:
        """
        Write data to the process's memory.

        :param lp_base_address: The process' pointer.
        :param value: The data to be written to the process's memory

        :return: It returns True if succeed if not it raises an exception.
        """
        try:
            write_buffer = ctypes.c_uint(value)
            lp_buffer = ctypes.byref(write_buffer)
            n_size = ctypes.sizeof(write_buffer)
            lp_number_of_bytes_written = ctypes.c_ulong(0)
            ctypes.windll.kernel32.WriteProcessMemory(
                self.handle, ctypes.c_void_p(lp_base_address), lp_buffer,
                n_size, lp_number_of_bytes_written
            )
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                'msg': str(error), 
                'Handle': self.handle,
                'PID': self.pid,
                'Name': self.name, 
                'ErrorCode': self.error_code
            }
            ReadWriteMemoryError(error)


    def writeString(self, lp_base_address: int, string: str) -> bool:
        """
        Write data to the process's memory.

        :param lp_base_address: The process' pointer.
        :param string: The string to be written to the process's memory

        :return: It returns True if succeed if not it raises an exception.
        """
        try:
            write_buffer = ctypes.create_string_buffer(string.encode())
            lp_buffer = ctypes.byref(write_buffer)
            n_size = ctypes.sizeof(write_buffer)
            lp_number_of_bytes_written = ctypes.c_size_t()
            ctypes.windll.kernel32.WriteProcessMemory(
                self.handle, lp_base_address, lp_buffer,
                n_size, lp_number_of_bytes_written
            )
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                'msg': str(error), 
                'Handle': self.handle, 
                'PID': self.pid,
                'Name': self.name, 
                'ErrorCode': self.error_code
            }
            ReadWriteMemoryError(error)


    def writeByte(self, lp_base_address: int, bytes: List[hex]) -> bool:
        """
        Write data to the process's memory.
        :param lp_base_address: The process' pointer {don't use offsets}.
        :param bytes: The byte(s) to be written to the process's memory
        :return: It returns True if succeed if not it raises an exception.
        """
        try:
            for x in range(len(bytes)):
                write_buffer = ctypes.c_ubyte(bytes[x])
                lp_buffer = ctypes.byref(write_buffer)
                n_size = ctypes.sizeof(write_buffer)
                lp_number_of_bytes_written = ctypes.c_ulong(0)
                ctypes.windll.kernel32.WriteProcessMemory(
                    self.handle, ctypes.c_void_p(lp_base_address + x), lp_buffer,
                    n_size, lp_number_of_bytes_written
                )
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                'msg': str(error), 
                'Handle': self.handle, 
                'PID': self.pid,
                'Name': self.name, 
                'ErrorCode': self.error_code
            }
            ReadWriteMemoryError(error)


    ## Close Method ##

    def close(self) -> int:
        """Closes the process
        Returns the last error code of the process.
        """
        ctypes.windll.kernel32.CloseHandle(self.handle)
        return self.get_last_error()
   
    
    ## Magic Methods ##

    def __repr__(self) -> str:
        return f'Process: [{self.pid}] "{self.name}"'
    
    
    # def thread(self, address: int):
    #     """
    #     Create a remote thread to the address.
    #     If you don't know what you're doing, the process can crash.
    #     """
    #     ctypes.windll.kernel32.CreateRemoteThread(
    #         self.handle, 0, 0, address, 0, 0, 0
    #     )
    #     self.close()    #the thread stays in the process
    #     self.open()     #just for better code understanding



if __name__ == '__main__':
    # Create a Process instance for notepad.exe
    process = Process.by_name('notepad.exe')
    # Open the process
    process.open()
    # Print the process' info
    print(process.__dict__)

    # Print the process
    print(process.get_modules())

    process