"""C1, lab session, 2026-10-08. Run a list of independent commands on the lab PC within the user's allowance.
  python guarded_pool.py <file with one command per line> <log file> [max workers, default 12]
Allowance given by the user on 08/10/2026: up to 80% of the processor and of the memory, and back to low performance as
soon as a program showing that someone is at the PC is open (Discord, FiveM, Valorant, ...).
Behaviour: the process list is read every 15 seconds; while a presence program is running at most ONE command runs
(the commands already started are left to finish: each is short); otherwise up to <max workers> (12 = 80% of 16
threads). Children get below-normal priority. If free memory falls below 20% of the total no new command is started.
Each finished command appends one line to the log: index, return code, seconds, last line of its output. Commands whose
index already appears in the log are skipped, so the run can be stopped and resumed."""
import sys, subprocess, time, os, ctypes
cmds = [l.rstrip("\n") for l in open(sys.argv[1], encoding="utf-8") if l.strip()]; logp = sys.argv[2]; MAXW = int(sys.argv[3]) if len(sys.argv) > 3 else 12
PRESENCE = ("discord.exe", "fivem", "gta5.exe", "valorant", "robloxplayer", "leagueclient", "cs2.exe", "fortniteclient")
done = set()
if os.path.exists(logp):
    for l in open(logp, encoding="utf-8"):
        if l.split("\t")[0].isdigit(): done.add(int(l.split("\t")[0]))
class MEM(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
def mem_ok():
    m = MEM(); m.dwLength = ctypes.sizeof(MEM); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)); return m.ullAvailPhys > 0.2 * m.ullTotalPhys
last = [0.0, False]
def presence():
    if time.time() - last[0] > 15:
        out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True).stdout.lower()
        names = {l.split('","')[0].strip('"') for l in out.splitlines() if l}; last[1] = any(any(p in n for p in PRESENCE) for n in names); last[0] = time.time()
    return last[1]
BELOW_NORMAL = 0x00004000; running = {}; todo = [i for i in range(len(cmds)) if i not in done]; t0 = time.time(); log = open(logp, "a", encoding="utf-8"); low_seen = 0
while todo or running:
    for i, (p, ts) in list(running.items()):
        if p.poll() is not None:
            out = (p.stdout.read() or "").strip().splitlines(); log.write("%d\t%d\t%.1f\t%s\n" % (i, p.returncode, time.time() - ts, out[-1][:300] if out else "")); log.flush(); del running[i]
    low = presence(); low_seen += low; cap = 1 if low else MAXW
    while todo and len(running) < cap and mem_ok():
        i = todo.pop(0); running[i] = (subprocess.Popen(cmds[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=BELOW_NORMAL), time.time())
    time.sleep(0.2)
print("commands %d, skipped as already done %d, elapsed %.0f s, presence checks positive %d" % (len(cmds), len(done), time.time() - t0, low_seen))
