> We have recovered a binary and a text file. Can you reverse the flag.



We have a binary called `rev` and an encrypted flag file `rev_this`. Running `rev` gives us: 

```bash
jake@computer:~/ctf-dump/picoctf/reverse_cipher$ ./rev
No flag found, please make sure this is run on the server
Segmentation fault (core dumped)
```

So it just crashes and can't find the flag. Let's try to open this up in a decompiler and analyze what the encryption code does

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char ptr[23]; // [rsp+0h] [rbp-50h] BYREF
  char v5; // [rsp+17h] [rbp-39h]
  int v6; // [rsp+2Ch] [rbp-24h]
  FILE *v7; // [rsp+30h] [rbp-20h]
  FILE *stream; // [rsp+38h] [rbp-18h]
  int j; // [rsp+44h] [rbp-Ch]
  int i; // [rsp+48h] [rbp-8h]
  char v11; // [rsp+4Fh] [rbp-1h]

  stream = fopen("flag.txt", "r");
  v7 = fopen("rev_this", "a");
  if ( !stream )
    puts("No flag found, please make sure this is run on the server");
  if ( !v7 )
    puts("please run this on the server");
  v6 = fread(ptr, 0x18uLL, 1uLL, stream);
  if ( v6 <= 0 )
    exit(0);
  for ( i = 0; i <= 7; ++i )
  {
    v11 = ptr[i];
    fputc(v11, v7);
  }
  for ( j = 8; j <= 22; ++j )
  {
    v11 = ptr[j];
    if ( (j & 1) != 0 )
      v11 -= 2;
    else
      v11 += 5;
    fputc(v11, v7);
  }
  v11 = v5;
  fputc(v5, v7);
  fclose(v7);
  return fclose(stream);
}
```

The encoded flag text gives us this: `picoCTF{w1{1wq84fb<1>49}`

Interesting. So we open up a `flag.txt` file in read and `rev_this` in append. Next up, from index 0 to 7 just outputs the first 7 bytes of the flag.txt file. This makes sense since the encrypted flag had the plaintext `picoCTF{`, which matches the indices in the loop.

```c
for ( i = 0; i <= 7; ++i )
  {
    v11 = ptr[i];
    fputc(v11, v7);
  }
```

Next up from index 8 to 22, we do a small encoding algorithm:

```c
for ( j = 8; j <= 22; ++j )
  {
    v11 = ptr[j];
    if ( (j & 1) != 0 )
      v11 -= 2;
    else
      v11 += 5;
    fputc(v11, v7);
  }
```

So if the index & 1 equals zero, the decimal value of the flag gets subtracted by two, and if not, the decimal value of the flag gets added by 5. 

We can easily reverse these operations in python:

```python
enc_flag = open('rev_this').read()
flag = enc_flag[0:8]
for i in range(8, 23):
    if (i & 1) != 0:
        flag += chr(ord(enc_flag[i]) + 2)
    else:
        flag += chr(ord(enc_flag[i]) - 5)

flag += enc_flag[23:]
print(flag)
```

And we get the flag: ```picoCTF{r3v3rs36ad73964}```