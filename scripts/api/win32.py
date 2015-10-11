import Api
from Api import Api
from Api import Function, Typedef, Enum
from Api import Return, Parameter, Input, Output, InputOutput
from Api import Enumerant
from Api import Extension
from Api import StateType, State

win32 = Api()

VOID = Typedef('VOID','void')

PVOID = Typedef('PVOID','void *')
PVOID.default = '0'

HANDLE = Typedef('HANDLE','PVOID')
HANDLE.default = '0'

LPCSTR = Typedef('LPCSTR','const char *')
LPCSTR.default = '0'

INT32 = Typedef('INT32','signed int')
INT32.default = '0'

INT64 = Typedef('INT64','signed __int64')
INT64.default = '0'

LPVOID = Typedef('LPVOID','void *')
LPVOID.default = '0'

BOOL = Typedef('BOOL','int')
BOOL.default = '0'

DWORD = Typedef('DWORD','unsigned long')
DWORD.default = '0'

FLOAT = Typedef('FLOAT','float')
FLOAT.default = '0'

INT = Typedef('INT','int')
INT.default = '0'

UINT = Typedef('UINT','unsigned int')
UINT.default = '0'

USHORT = Typedef('USHORT','unsigned short')
USHORT.default = '0'

PROC = Typedef('PROC','void *')
PROC.default = 'NULL'

COLORREF = Typedef('COLORREF','DWORD')
COLORREF.default = '0'

LONG = Typedef('LONG','long')
LONG.default = '0'

ULONG_PTR = Typedef('ULONG_PTR','unsigned long *')
ULONG_PTR.default = 'NULL'

HDC = Typedef('HDC','HANDLE')
HDC.default = '0'
HDC.regal = False

HGLRC = Typedef('HGLRC','HANDLE')
HGLRC.default = '0'
HGLRC.regal = False

win32.add(VOID)
win32.add(PVOID)
win32.add(HANDLE)
win32.add(LPCSTR)
win32.add(INT32)
win32.add(INT64)
win32.add(LPVOID)
win32.add(BOOL)
win32.add(DWORD)
win32.add(FLOAT)
win32.add(INT)
win32.add(UINT)
win32.add(USHORT)
win32.add(PROC)
win32.add(COLORREF)
win32.add(LONG)
win32.add(ULONG_PTR)
win32.add(HDC)
win32.add(HGLRC)

defines = Enum('defines')
win32.add(defines)
