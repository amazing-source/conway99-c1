"""Run a command at IDLE priority (Windows; children inherit the class).  usage: python idle_run.py <cmd> [args...]"""
import ctypes
import subprocess
import sys

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
sys.exit(subprocess.run(sys.argv[1:]).returncode)
