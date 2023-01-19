import ctypes

path = 'C:\\Users\\verti\\source\\repos\\TestLibrary\\TestLibrary\\bin\\x64\\Debug\\net6.0\\'
dll_file = 'TestLibrary.dll'

a = ctypes.cdll.LoadLibrary(path + dll_file)
print(a.add(3, 5))