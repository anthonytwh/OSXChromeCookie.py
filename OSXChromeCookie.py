#! /usr/bin/env python3

'''
Forked from n8henrie @ https://gist.github.com/n8henrie/8715089

Reference: http://n8h.me/HufI1w

Log:
2020055 Fork and update.
    - Extract host_key from Cookie db.
    - Modify URL input.
2015022 Now its own GitHub repo, and in PyPi. 
    - For most recent version: https://github.com/n8henrie/pycookiecheat
    - This gist unlikely to be maintained further for that reason.
20150221 v2.0.1: Now should find cookies for base domain and all subs.
20140518 v2.0: Now works with Chrome's new encrypted cookies.

'''

import sqlite3
import os.path
import keyring
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def chrome_cookies(URL):
    ''' Main.
    '''

    # Default values 
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16

    def chrome_decrypt(encrypted_value, key=None):
        ''' Decrypt host cookie.
        '''
        # Strip leading 'v10' from Chromium encrypted cookies.
        encrypted_value = encrypted_value[3:]

        # Strip padding by taking off number indicated by padding
        # eg if last is '\x0e' then ord('\x0e') == 14, so take off 14.
        def clean(x):
            return x[:-x[-1]].decode('utf8')

        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
        decrypted = cipher.decrypt(encrypted_value)

        return clean(decrypted)

    # Chrome Browser on OSX
    if sys.platform == 'darwin':
        my_pass = keyring.get_password('Chrome Safe Storage', 'Chrome')
        my_pass = my_pass.encode('utf8')
        iterations = 1003
        cookie_file = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies')

    # Generate decrypt key from values above
    key = PBKDF2(my_pass, salt, length, iterations)

    # Connect to DB file
    conn = sqlite3.connect(cookie_file)
    c = conn.cursor()
    sql = 'SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key == "' + URL + '"'
    c.execute(sql)
    cookies = {}
    cookies_list = []

    for host_key, name, value, encrypted_value in c.fetchall():
        # if there is a not encrypted value or if the encrypted value
        # doesn't start with the 'v10' prefix, return v
        if value or (encrypted_value[:3] != b'v10'):
            cookies_list.append((host_key+"_"+name, value))
        else:
            decrypted_tuple = (name, chrome_decrypt(encrypted_value, key=key))
            cookies_list.append(decrypted_tuple)
    cookies.update(cookies_list)

    return cookies