import sqlite3
conn = sqlite3.connect('FaceBoookADS.db')
c = conn.cursor()
c.execute('''INSERT INTO ads VALUES 
(?, ?)'''
          , ('id1', 'text1'))
conn.commit()
conn.close()