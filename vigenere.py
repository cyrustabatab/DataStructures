from string import ascii_lowercase
import math


print(ascii_lowercase)



def encrypt_2(s,key):
    key = key.encode('utf-8')
    
    key = 0xA12F
    key =key.to_bytes(2,'big')
    s = s.encode('utf-8')
    
    frame = bytearray()
    i = 0
    
    number = 0

    while i < len(s):
        c = s[i]

        result = c ^ key[i % len(key)]
        frame.append(result)
        number <<= 8
        number |= result
        print(hex(number))
        i += 1
    
    print(hex(frame[0]))
    return number


def decrypt_2(ciphertext):
    

    num_bytes =(int(math.ceil(ciphertext.bit_length() / 8)))
    key = 0xA12F
    
    key =key.to_bytes(2,'big')

    ciphertext = ciphertext.to_bytes(num_bytes,'big')
    

    plaintext = []
    
    i = 0

    while i < len(ciphertext):
        b = ciphertext[i]

        result = key[i % len(key)] ^ b
        plaintext.append(chr(result))
        i += 1

    return plaintext

    











def decrypt(s,key):
    

    s = s.lower()

    alphabet_length = len(ascii_lowercase)

    key_length = len(key)

    plaintext = []

    i = 0

    while i < len(s):
        c = s[i]
        decrypted_character = ascii_lowercase[((ord(c) - 97) - (ord(key[i % key_length]) - 97)) % alphabet_length]
        plaintext.append(decrypted_character)
        i += 1


    return ''.join(plaintext)


def encrypt(s,key):
    
    s = s.lower()

    alphabet_length = len(ascii_lowercase)
    key_length = len(key)
    
    ciphertext = []
    i = 0

    while i < len(s):
        c = s[i]
        if c == ' ':
            continue
        

        encrypted_character = ascii_lowercase[((ord(c) - 97) + (ord(key[i % key_length]) - 97)) % alphabet_length]
        ciphertext.append(encrypted_character)
        i += 1
    

    return ''.join(ciphertext)


if __name__ == "__main__":
    
    

    #plaintext= "tellhimaboutme"
    #key = "cafe"

    #ciphertext = (encrypt(plaintext,key))
    #print(ciphertext)

    #print(decrypt(ciphertext,key))

    plaintext = 'Hello!'
    encrypted = encrypt_2(plaintext,'hello')

    plaintext = decrypt_2(encrypted)
    print(plaintext)






