import pytest
from ctypes import *
from pysrt.memory.process import Process, ProcessAccess


@pytest.fixture
def test_process():
    return Process(name='notepad.exe', pid=1234)


def test_read_lp(test_process):
    # Arrange
    test_process.open()  # Open the process
    lp_base_address = 0x123456
    base_offset = 0x5
    # Override the method to read data from fixed address
    test_process._read = lambda *x, **y: c_uint(0x11223344).value
    
    # Act
    result = test_process.read_lp(lp_base_address, base_offset)
    
    # Assert
    assert result == 0x11223344