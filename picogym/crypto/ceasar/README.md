Ceasar is a medium difficulty cryptography challenge that goes over the basics of a ceasar cipher and how to exploit and crack one. I personally found this challenge to be amusing and I learned the basic fundamentals of a ceasar cipher from this challenge. 




Challenge: https://github.com/FaithfulFollowersOfFlaherty/CTFWriteups/blob/picoCTF/picogym/crypto/ceasar/Images/ceasar%20challenge%20image.png

In this challenge, we have to decrypt a ceasar cipher message to find the flag. 

When we open the message file, we get the following string: 

picoCTF{dspttjohuifsvcjdpoabrkttds}

Now, as you can see, we already have the picoCTF part with the curly braces, what we actually have to decrypt is the message inside the curly brackets. 


With ceasar ciphers, a common way to find a vulnerability in encrypted messages is through a frequency attack, how this attack works is you take the string, and you identify what letters show up most frequently in a string, and you try and associate them with the most commonly used letters in the alphabet. In the string above, here are the most commonly appearing letters to least. 

t=4
s=3
d=3
p=2
j=2
o=2
h=1
u=1
i=1
f=1
v=1
c=1
a=1

Now, with the frequency of each letter's appearance identified, we can associate the most common letter, which is t in this instance, to the plaintext letter e. 

now, to change the string to incorporate the letter t to e, we need to figure out how many letters apart the two are. I have a physical thinking process of how I determined this, which is shown here: 


