import json
import sys

service = sys.argv[1]

# The handout's base template, minus "mount" (the APIs never need it)
template = [
    "accept4", "access", "arch_prctl", "bind", "brk", "chdir", "chmod",
    "chown", "clone", "close", "connect", "dup2", "execve", "exit_group",
    "fcntl", "fstat", "futex", "getdents64", "getpid", "getcwd",
    "getsockname", "gettid", "ioctl", "listen", "lseek", "mkdir", "mmap",
    "open", "pipe", "prctl", "read", "rt_sigaction", "rt_sigprocmask",
    "rt_sigreturn", "select", "setgid", "setgroups", "setuid", "socket",
    "stat", "write"
]

# Docker's runtime (runc) needs these to start the container at all
runc_needs = ["newfstatat", "faccessat", "faccessat2", "capget", "capset", "close_range", "fstatfs", "getppid", "statx"]

# Python needs these while it starts up, before strace can attach
startup_needs = ["clone3", "setsockopt", "getsockopt", "getpeername", "uname", "getrandom", "getegid", "geteuid", "getgid", "getuid", "pread64",
                 "prlimit64", "readlinkat", "set_tid_address"]

# Syscalls this service actually made while strace was watching it
with open(service + "-syscalls.txt") as f:
    observed = f.read().split()

allowed = sorted(set(template + runc_needs + startup_needs + observed))

profile = {
    "defaultAction": "SCMP_ACT_ERRNO",
    "architectures": ["SCMP_ARCH_X86_64"],
    "syscalls": [{"names": allowed, "action": "SCMP_ACT_ALLOW"}]
}

with open("seccomp-profiles/seccomp-" + service + ".json", "w") as f:
    json.dump(profile, f, indent=4)

print(service + ": " + str(len(allowed)) + " syscalls allowed")
