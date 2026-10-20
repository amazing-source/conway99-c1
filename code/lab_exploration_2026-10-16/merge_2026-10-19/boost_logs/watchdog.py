"""Boost watchdog (LAB 20/10/2026).  The user allowed more CPU while nobody uses the PC and asked to cut it as soon
as something opens.

Boost processes = processes whose command line contains one of ROOT_MARKS, plus all their descendants.  The jobs
that were already running before the boost (first P3 runner, rank-39 star of seed 1) are not touched.

Loop, forever:
  WATCH  : every 2 s look for (a) any keyboard/mouse input (GetLastInputInfo changes), (b) a visible top-level
           window of an executable that had none at the baseline, (c) a new game/launcher process.  On the first
           hit, suspend every boost process (NtSuspendProcess: CPU at 0, nothing lost) -> WAIT.
  WAIT   : once there has been no input for IDLE_MIN minutes and neither (b) nor (c) holds, resume -> WATCH.
Every 20 s (both states) kill the duplicates of the runner-2 P3 jobs started later by the first runner.
Events go to watchdog.log.  'python watchdog.py release' resumes everything listed in suspended.json at once."""
import ctypes
import ctypes.wintypes as wt
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "watchdog.log")
BASE = os.path.join(HERE, "baseline.json")
SUSP = os.path.join(HERE, "suspended.json")
IDLE_MIN = 30
ROOT_MARKS = ("p3local_runner2.py", "scratchpad/boost/runs", "scratchpad\\boost\\runs")
DUPS = ("idx_core088_b003270_s008_n256.json", "idx_core088_b003270_s024_n256.json")
GAMES = ("fivem", "gta5", "gtav", "playgtav", "valorant", "leagueclient", "league of legends", "riotclientux",
         "steam.exe", "steamwebhelper", "epicgameslauncher", "battle.net", "obs64", "cs2.exe", "fortnite",
         "minecraft", "robloxplayer", "robloxstudio", "eadesktop", "ubisoftconnect", "upc.exe", "rockstar")
WHITE = {"explorer.exe", "shellexperiencehost.exe", "searchhost.exe", "startmenuexperiencehost.exe",
         "textinputhost.exe", "applicationframehost.exe", "lockapp.exe", "conhost.exe", "openconsole.exe",
         "windowsterminal.exe", "powershell.exe", "pwsh.exe", "cmd.exe", "bash.exe", "python.exe", "star39.exe",
         "claude.exe", "wallpaper64.exe", "wallpaper32.exe"}

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll")
dwmapi = ctypes.WinDLL("dwmapi")


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wt.UINT), ("dwTime", wt.DWORD)]


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", wt.DWORD), ("cntUsage", wt.DWORD), ("th32ProcessID", wt.DWORD),
                ("th32DefaultHeapID", ctypes.c_size_t), ("th32ModuleID", wt.DWORD), ("cntThreads", wt.DWORD),
                ("th32ParentProcessID", wt.DWORD), ("pcPriClassBase", ctypes.c_long), ("dwFlags", wt.DWORD),
                ("szExeFile", ctypes.c_wchar * 260)]


WNDENUMPROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
kernel32.CreateToolhelp32Snapshot.restype = wt.HANDLE
kernel32.CreateToolhelp32Snapshot.argtypes = [wt.DWORD, wt.DWORD]
kernel32.Process32FirstW.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
kernel32.Process32NextW.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
kernel32.OpenProcess.restype = wt.HANDLE
kernel32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
kernel32.CloseHandle.argtypes = [wt.HANDLE]
kernel32.TerminateProcess.argtypes = [wt.HANDLE, wt.UINT]
kernel32.GetTickCount.restype = wt.DWORD
ntdll.NtSuspendProcess.argtypes = [wt.HANDLE]
ntdll.NtResumeProcess.argtypes = [wt.HANDLE]
user32.GetLastInputInfo.argtypes = [ctypes.POINTER(LASTINPUTINFO)]
user32.EnumWindows.argtypes = [WNDENUMPROC, wt.LPARAM]
user32.IsWindowVisible.argtypes = [wt.HWND]
user32.GetWindowTextLengthW.argtypes = [wt.HWND]
user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
user32.GetWindow.argtypes = [wt.HWND, wt.UINT]
user32.GetWindow.restype = wt.HWND
user32.GetWindowLongW.argtypes = [wt.HWND, ctypes.c_int]
dwmapi.DwmGetWindowAttribute.argtypes = [wt.HWND, wt.DWORD, ctypes.c_void_p, wt.DWORD]
INVALID = ctypes.c_void_p(-1).value


def log(msg):
    line = "%s %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def last_input():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    user32.GetLastInputInfo(ctypes.byref(lii))
    return lii.dwTime


def idle_s():
    return ((kernel32.GetTickCount() - last_input()) & 0xFFFFFFFF) / 1000.0


def procs():
    out = {}
    snap = kernel32.CreateToolhelp32Snapshot(2, 0)
    if not snap or snap == INVALID:
        return out
    pe = PROCESSENTRY32W()
    pe.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    ok = kernel32.Process32FirstW(snap, ctypes.byref(pe))
    while ok:
        out[pe.th32ProcessID] = (pe.th32ParentProcessID, pe.szExeFile.lower())
        ok = kernel32.Process32NextW(snap, ctypes.byref(pe))
    kernel32.CloseHandle(snap)
    return out


def window_exes(pmap):
    found = set()

    def cb(hwnd, lp):
        try:
            if not user32.IsWindowVisible(hwnd) or user32.GetWindow(hwnd, 4):
                return True
            if user32.GetWindowLongW(hwnd, -20) & 0x80:
                return True
            cl = wt.DWORD(0)
            dwmapi.DwmGetWindowAttribute(hwnd, 14, ctypes.byref(cl), 4)
            if cl.value or user32.GetWindowTextLengthW(hwnd) == 0:
                return True
            pid = wt.DWORD(0)
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            found.add(pmap.get(pid.value, (0, "?"))[1])
        except Exception:
            pass
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return found


def cmdlines():
    ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine } | "
          "ForEach-Object { [string]$_.ProcessId + [char]9 + $_.CommandLine }")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True,
                           timeout=90, creationflags=0x08000000)
    except Exception as e:
        log("command-line query failed: %r" % (e,))
        return None
    out = {}
    for line in r.stdout.decode("utf-8", "replace").splitlines():
        if "\t" in line:
            a, b = line.split("\t", 1)
            if a.strip().isdigit():
                out[int(a)] = b
    return out


def boost_set(cl, pmap):
    me = os.getpid()
    s = {p for p, c in cl.items() if p in pmap and p != me and any(m in c for m in ROOT_MARKS)}
    grew = True
    while grew:
        grew = False
        for p, (pp, _) in pmap.items():
            if pp in s and p not in s and p != me:
                s.add(p)
                grew = True
    return s


def kill_dups(cl):
    for p, c in cl.items():
        if any(d in c for d in DUPS) and "__r2" not in c:
            h = kernel32.OpenProcess(0x0001, False, p)
            if h:
                kernel32.TerminateProcess(h, 1)
                kernel32.CloseHandle(h)
                log("killed a duplicate of a runner-2 job started by the first runner: pid %d ...%s" % (p, c[-70:]))


def new_games(pmap, base_pids):
    return sorted({exe for p, (_, exe) in pmap.items() if p not in base_pids and any(g in exe for g in GAMES)})


def busy_reason(pmap, base_w, base_pids):
    w = window_exes(pmap) - base_w
    if w:
        return "new window: " + ", ".join(sorted(w))
    g = new_games(pmap, base_pids)
    if g:
        return "new game/launcher process: " + ", ".join(g)
    return None


def ntcall(fn, pids):
    n = 0
    for p in pids:
        h = kernel32.OpenProcess(0x0800, False, p)
        if h:
            if fn(h) == 0:
                n += 1
            kernel32.CloseHandle(h)
    return n


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "release":
        susp = json.load(open(SUSP))
        pmap = procs()
        live = [p for p, exe in susp["suspended"] if pmap.get(p, (0, ""))[1] == exe]
        log("manual release: resumed %d processes" % ntcall(ntdll.NtResumeProcess, live))
        os.replace(SUSP, SUSP + ".released")
        return
    pmap = procs()
    if not os.path.exists(BASE):
        json.dump({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "window_exes": sorted(window_exes(pmap)),
                   "pids": sorted(pmap)}, open(BASE, "w"), indent=1)
    base = json.load(open(BASE))
    base_w, base_pids = set(base["window_exes"]) | WHITE, set(base["pids"])
    log("start: idle %.0f s; baseline windows %s" % (idle_s(), base["window_exes"]))
    state = "WAIT" if os.path.exists(SUSP) else "WATCH"
    t_in, next_cl, cl = last_input(), 0.0, {}
    while True:
        if time.time() >= next_cl:
            c = cmdlines()
            if c is not None:
                cl = c
                kill_dups(cl)
            next_cl = time.time() + 20
        pmap = procs()
        if state == "WATCH":
            reason = "keyboard/mouse input" if last_input() != t_in else busy_reason(pmap, base_w, base_pids)
            if reason:
                cl = cmdlines() or cl
                pmap = procs()
                bs = sorted(boost_set(cl, pmap))
                n = ntcall(ntdll.NtSuspendProcess, bs)
                json.dump({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "reason": reason,
                           "suspended": [(p, pmap[p][1]) for p in bs]}, open(SUSP, "w"), indent=1)
                log("CUT (%s): suspended %d/%d boost processes %s" % (reason, n, len(bs),
                                                                       sorted({pmap[p][1] for p in bs})))
                state = "WAIT"
            time.sleep(2)
        else:
            if idle_s() >= 60 * IDLE_MIN and busy_reason(pmap, base_w, base_pids) is None:
                susp = json.load(open(SUSP))
                live = [p for p, exe in susp["suspended"] if pmap.get(p, (0, ""))[1] == exe]
                n = ntcall(ntdll.NtResumeProcess, live)
                os.replace(SUSP, SUSP + ".last")
                log("RESUMED %d processes after %.0f min without input" % (n, idle_s() / 60))
                state, t_in = "WATCH", last_input()
            time.sleep(10)


if __name__ == "__main__":
    main()
