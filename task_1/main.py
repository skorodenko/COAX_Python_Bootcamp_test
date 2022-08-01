import hashlib


def hash_string(string: str, hash_type: str = "sha256") -> str:
    """Hashes a string with specified hash-function.

    string: string to hash
    hash_type: string, represents the name of hash-function (sha256 by default)

    Returns a string representation of hexadecimal hash.
    """
    encoded_string = string.encode()
    hash = hashlib.new(hash_type)
    hash.update(encoded_string)
    return hash.hexdigest()
