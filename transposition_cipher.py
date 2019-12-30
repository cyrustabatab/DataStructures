import pyperclip
import math
from string import ascii_uppercase
import random
from detect_english_programmatically import is_message_english
import pyperclip



def encrypt(m,key):

    encryption = []



    i = 0
    while i < len(m):
        current_row = []
        j = 0
        while i < len(m) and j < key:
            current_row.append(m[i])
            i += 1
            j += 1

        encryption.append(current_row)
    
    ciphertext = []
    for j in range(len(encryption[0])):
        for i in range(len(encryption)):
            if j < len(encryption[i]):
                ciphertext.append(encryption[i][j])
            else:
                break

    return ''.join(ciphertext)
    #print(list(zip(*encryption)))
    #return ''.join(''.join(l) for l in list(zip(*encryption)))


            
def decrypt(m,k):

    n = int(math.ceil(len(m) / k))
    #decrypt ciphertext given key
    boxes = n * k
    boxes_to_shade = boxes - len(m) 
    decryption = []

    shaded_boxes = set()
    for i in range(boxes_to_shade):
        shaded_boxes.add(boxes - 1 - n * i)
    box = 0
    i = 0
    while i < len(m):
        j = 0
        decryption_row = []
        while i < len(m) and j < n:
            if box in shaded_boxes: 
                box += 1
                break
            decryption_row.append(m[i])
            i += 1
            j += 1
            box += 1

        
        decryption.append(decryption_row)
    
    plaintext = []
    for j in range(len(decryption[0])):
        for i in range(len(decryption)):
            if j < len(decryption[i]):
                plaintext.append(decryption[i][j])
            else:
                break

    return ''.join(plaintext)




def transposition_cipher(m):
    

    key_min,key_max = 2,len(m) // 2

    key = int(input(f"Type key from {key_min} to {key_max}: "))


    encrypted = (encrypt(m,key))
    print(encrypted)
    plaintext= decrypt(encrypted,key)
    print(plaintext)


def test_transposition_cipher(num_tests=20):

    
    for i in range(num_tests):

        message = ascii_uppercase * random.randint(4,40)


        message = list(message)
        random.shuffle(message)
        message = ''.join(message)
        
        for key in range(2,len(message)//2):
            encrypted_message= encrypt(message,key)
            decrypted_message = decrypt(encrypted_message,key)

            if message != decrypted_message:
                print("Test Failed")
                print("Mismatch between {message} and {decrypted_message}")
                return


    print("Transposition Cipher Passed")



def break_transposition_cipher(m):


    for key in range(2,len(m)//2):
        decrypted_message = decrypt(m,key)

        if is_message_english(decrypted_message):
            print(decrypted_message)

    


if __name__ == "__main__":
    

    key = 10
    message = "This is the greatest game in the world. Hopefully we will strike TOMORROW"
    print(message)
    encrypted_message = encrypt(message,key)
    print(encrypted_message)

    break_transposition_cipher(encrypted_message)
    



    #test_transposition_cipher()
    #while True:
    #    choice = input("Encrypt or Decrypt(type 'e' or 'd' for decrypt or ENTER to quit): ").lower()
    #    if choice == '':
    #        break
    #    to_encrypt = True if choice == 'e' else  False
    #    
    #    message = input(f"Message to {'encrypt' if to_encrypt else 'decrypt'}: ")
    #    key = int(input(f"Enter key between 2 and {len(message) // 2}: "))
    #    if to_encrypt:
    #        s = encrypt(message,key)
    #        pyperclip.copy(s)
    #    else:
    #        print('here')
    #        s = decrypt(message,key)

    #    print(s)

