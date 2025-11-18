import typing as tp


def encrypt_affine(plaintext: str, a: int, b: int, m: int) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in plaintext:
        if i.isalpha():
            ciphertext += chr((a * ord(i) + b) % m)
    return ciphertext


if __name__ == "__main__":
    print("Affine Encrypter")
    p = int(input("Enter a number: "))
    q = int(input("Enter another number: "))
    message = input("Enter a message to encrypt: ")
    encrypted_msg = encrypt_affine(message, p, q, 26)
    print("Your encrypted message is: ")
    print(encrypted_msg)
