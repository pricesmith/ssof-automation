import os
import sqlite3
import tempfile
import logging



def init_db():
    # t_file = os.path.join(tempfile.gettempdir(), 'nvd')
    conn = sqlite3.connect('nvd')
    return conn.cursor()

def init_tables(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS cve_requests(request, datetime)")
    # cur.execute("CREATE TABLE IF NOT EXISTS cve_vulnerabilities")

def insert_into_cve_request(cur, req, iso_datetime):
    cur.execute("INSERT INTO cve_requests VALUES {req} {iso_datetime}")