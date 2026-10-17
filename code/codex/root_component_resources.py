"""Shared CPU affinity budget for the C1 campaign, below the user's 80% ceiling.

Every worker shares the same affinity mask, so separate threads/processes
cannot turn a worker limit into use of all logical processors.
"""

import os
import sys
import json
from pathlib import Path
import time


def atomic_json_write(path, value, indent=None):
    """Retry Windows sharing conflicts from readers without exposing partial JSON."""
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=indent, separators=None if indent else (',', ':')) + '\n',
                         encoding='utf-8')
    for attempt in range(200):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if attempt == 199:
                raise
            time.sleep(.05)


def limit_research_process(cores=4):
    state = Path(__file__).resolve().parents[2] / "data/codex_line_resonance_20261016/cpu_guard.budget.json"
    while state.exists():
        try:
            budget = json.loads(state.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            time.sleep(.1)
            continue
        if budget.get("paused"):
            time.sleep(1)
            continue
        cores = min(cores, int(budget["logical_cores"]))
        break
    for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[variable] = "1"
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL("kernel32", use_last_error=True)
        api.GetCurrentProcess.restype = wintypes.HANDLE
        api.GetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)]
        api.SetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.c_size_t]
        api.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        handle = api.GetCurrentProcess()
        allowed, system = ctypes.c_size_t(), ctypes.c_size_t()
        if not api.GetProcessAffinityMask(handle, ctypes.byref(allowed), ctypes.byref(system)):
            raise ctypes.WinError(ctypes.get_last_error())
        selected = [i for i in range(8*ctypes.sizeof(ctypes.c_size_t)) if allowed.value & (1<<i)][:cores]
        mask = sum(1<<i for i in selected)
        if not api.SetProcessAffinityMask(handle, mask):
            raise ctypes.WinError(ctypes.get_last_error())
        if not api.SetPriorityClass(handle, 0x00004000):  # BELOW_NORMAL_PRIORITY_CLASS
            raise ctypes.WinError(ctypes.get_last_error())
        return {"logical_cpu_budget": len(selected), "shared_affinity_mask": mask, "priority": "below_normal"}
    if hasattr(os, "sched_getaffinity"):
        selected = sorted(os.sched_getaffinity(0))[:cores]
        os.sched_setaffinity(0, selected)
        return {"logical_cpu_budget": len(selected), "shared_affinity": selected}
    raise RuntimeError("Cannot enforce the requested CPU budget on this platform.")
