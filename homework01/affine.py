def encrypt_affine(plaintext: str, a: int, b: int) -> str:
    ciphertext = ""
    for i in plaintext:
        if i.isalpha():
            if i.isupper():
                t = ord("A")
            else:
                t = ord("a")
            ciphertext += chr(t + (a * ord(i) + b) % 26)
        else:
            ciphertext += i
    return ciphertext


if __name__ == "__main__":
    print("Affine Encrypter")
    p = int(input("Enter a number: "))
    q = int(input("Enter another number: "))
    message = input("Enter a message to encrypt: ")
    encrypted_msg = encrypt_affine(message, p, q)
    print("Your encrypted message is: ")
    print(encrypted_msg)
