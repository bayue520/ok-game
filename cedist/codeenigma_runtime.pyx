from datetime import datetime, UTC
import base64
import marshal
import zlib
import types
import sys

try:
    import rich
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ModuleNotFoundError:
    print("Error: rich and cryptography modules are required to run this code. Please install them using pip install rich cryptography or using poetry add rich cryptography.")
    sys.exit(1)

def execute_secure_code(secure_code: bytes, globals_dict=None) -> None:

    NONCE = b't\x1ezx\x9b\xe7\x0c{\x0b\xd6\xd3\xc0'
    
    # Auto-generated AES key reconstruction code

    p0 = [0x43, 0x26, 0x14, 0x37, 0x46, 0xB0, 0xC2, 0x4A]
    p1 = [0xF4, 0x33, 0xB9, 0xE8, 0xFC, 0x71, 0xA3, 0x3C]
    p2 = [0xF8, 0xB3, 0xE6, 0x4E, 0x98, 0xD6, 0xFC, 0x74]
    p3 = [0x03, 0x7B, 0xC5, 0x98, 0x38, 0xAB, 0xB4, 0x62]
    xor0 = [0x56, 0xE9, 0x9F, 0xEA, 0x1B, 0xE4, 0xDD, 0xF7]
    xor3 = [0x90, 0x1B, 0xD0, 0x21, 0xC8, 0xAA, 0xC6, 0xE3]

    def get_aes_key() -> bytes:
        key = bytearray(32)
        for i in range(8):
            key[i] = p0[i] ^ xor0[i]
            key[i + 8] = p1[7 - i]
            key[i + 16] = p2[i]
            key[i + 24] = p3[i] ^ xor3[i]
        return bytes(key)

    SECRET_KEY = get_aes_key()
    
    
    if globals_dict is None:
        globals_dict = globals()

    aesgcm = AESGCM(SECRET_KEY)

    try:
        decrypted = aesgcm.decrypt(NONCE, secure_code, None)
        del NONCE, SECRET_KEY, aesgcm
        compressed = base64.b64decode(decrypted)
        del decrypted
        marshaled = zlib.decompress(compressed)
        del compressed
        code_obj = marshal.loads(marshaled)
        del marshaled
        if isinstance(code_obj, types.CodeType):
            exec(code_obj, globals_dict)
        else:
            raise ValueError("Invalid code object in obfuscated module")
    except Exception as e:
        rich.print(f"[bold red]Error executing obfuscated code: {e}[/bold red]")
        raise
