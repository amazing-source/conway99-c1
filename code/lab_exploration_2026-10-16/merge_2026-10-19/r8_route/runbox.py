"""Bounded runner for the R8 route (LAB 20/10/2026).

Rules of the session: one solver process at a time, at most 300 s wall per run, declared memory bound, command line
containing scratchpad/boost/runs (so that the boost watchdog can suspend it), stop if boost/suspended.json exists.

usage: python runbox.py <wall seconds <= 300> <memory MB> <log jsonl under scratchpad/boost/runs> -- cmd args...
The child is put in a Windows job object with a per-process memory limit and KILL_ON_JOB_CLOSE; on timeout the job is
terminated.  One JSON line (command, status, exit code, wall time, peak memory) is appended to the log."""
import ctypes
import ctypes.wintypes as wt
import json
import os
import subprocess
import sys
import time

BOOST = ("C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-"
         "conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/boost")
SUSP = os.path.join(BOOST, "suspended.json")

k32 = ctypes.WinDLL("kernel32", use_last_error=True)


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in ("r", "w", "o", "rb", "wb", "ob")]


class BASIC(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong), ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wt.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wt.DWORD),
                ("Affinity", ctypes.c_size_t), ("PriorityClass", wt.DWORD), ("SchedulingClass", wt.DWORD)]


class EXT(ctypes.Structure):
    _fields_ = [("Basic", BASIC), ("Io", IO_COUNTERS), ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t)]


k32.CreateJobObjectW.restype = wt.HANDLE
k32.OpenProcess.restype = wt.HANDLE
k32.SetInformationJobObject.argtypes = [wt.HANDLE, ctypes.c_int, ctypes.c_void_p, wt.DWORD]
k32.QueryInformationJobObject.argtypes = [wt.HANDLE, ctypes.c_int, ctypes.c_void_p, wt.DWORD, ctypes.c_void_p]
k32.AssignProcessToJobObject.argtypes = [wt.HANDLE, wt.HANDLE]
k32.TerminateJobObject.argtypes = [wt.HANDLE, wt.UINT]


def main():
    wall, mem, log = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    cmd = sys.argv[sys.argv.index("--") + 1:]
    assert wall <= 300 + 1e-9, "wall limit above 5 minutes"
    assert "boost/runs" in log.replace("\\", "/"), "log must live under scratchpad/boost/runs"
    if os.path.exists(SUSP):
        print("REFUSED: suspended.json exists (boost suspended); stop computing", flush=True)
        sys.exit(3)
    job = k32.CreateJobObjectW(None, None)
    info = EXT()
    info.Basic.LimitFlags = 0x100 | 0x2000          # PROCESS_MEMORY | KILL_ON_JOB_CLOSE
    info.ProcessMemoryLimit = mem * 1024 * 1024
    assert k32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))
    t0 = time.time()
    p = subprocess.Popen(cmd, creationflags=0x00004000)     # BELOW_NORMAL_PRIORITY_CLASS
    h = k32.OpenProcess(0x1F0FFF, False, p.pid)
    k32.AssignProcessToJobObject(job, h)
    try:
        rc = p.wait(timeout=wall)
        st = "DONE"
    except subprocess.TimeoutExpired:
        k32.TerminateJobObject(job, 1)
        p.wait()
        rc, st = None, "TIMEOUT"
    q = EXT()
    k32.QueryInformationJobObject(job, 9, ctypes.byref(q), ctypes.sizeof(q), None)
    rec = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "cmd": cmd, "status": st, "rc": rc,
           "wall": round(time.time() - t0, 2), "peak_MB": round(q.PeakProcessMemoryUsed / 2 ** 20, 1),
           "mem_limit_MB": mem}
    with open(log, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
