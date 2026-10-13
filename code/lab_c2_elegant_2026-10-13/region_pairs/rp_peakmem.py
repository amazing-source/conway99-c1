"""Run one scan + one batch pair in-process and print the peak working set (Windows), to declare the memory bound.
<lab python> -B rp_peakmem.py"""
import sys, os, ctypes, ctypes.wintypes as wt, subprocess
class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
def peak():
    pmc = PMC(); pmc.cb = ctypes.sizeof(PMC)
    k32 = ctypes.WinDLL("kernel32", use_last_error=True); ps = ctypes.WinDLL("psapi", use_last_error=True)
    k32.GetCurrentProcess.restype = wt.HANDLE
    ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
    ps.GetProcessMemoryInfo.restype = wt.BOOL
    h = k32.GetCurrentProcess()
    ok = ps.GetProcessMemoryInfo(h, ctypes.byref(pmc), pmc.cb)
    assert ok
    return pmc.PeakWorkingSetSize / 2**20
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, numpy as np
from rp_lib import Lattice, OUT
import rp_search as RS, rp_task2_run as TR
lat = Lattice("044")
print("after lattice load: peak working set %.0f MiB" % peak())
scan = json.load(open(os.path.join(OUT, "scan_044.json")))
p = [q for q in scan["pairs"] if q["region"]][3]
inst = RS.build_instance(lat, np.array(p["y1"]), np.array(p["y2"]), p)
pk = RS.pack_instance(inst)
print("after instance: peak %.0f MiB" % peak())
for md in (0, 1, 4): RS.run(pk, md, node_limit=3_000_000, maxsol=5)
print("after searches: peak %.0f MiB" % peak())
