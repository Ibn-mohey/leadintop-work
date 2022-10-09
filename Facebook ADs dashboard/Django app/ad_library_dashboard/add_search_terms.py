import sqlite3
terms = """better
works\worked
acne
breakouts
saggy
baggy
squint
correct
exfoliate
body 
after bath 
cool 
couple
armpit
skin 
smooth
soft 
boost 
shower 
cream 
scent 
nails
sweet 
trim
soap 
wrinkles
eyebrows
dollar
usd
dhr
درهم
ريال
sar
riyal
Your 
smell 
Avoid
Chose 
Choose 
Tired of 
get rid
you need""".split('\n')
for term in terms:
    try:
        conn = sqlite3.connect('FaceBoookADS.db')
        c = conn.cursor()
        c.execute('''INSERT INTO search_terms(search_term,search_type,active,country) VALUES (?,?,?,?)
        ;'''
        ,(term.trim(),'keyword',True,'ALL'))
        conn.commit()
        conn.close()
    except:
        pass
    
# 	text	NO		
# id	integer	NO		
# 	text	NO		
# 	text	NO		
# 	bool	NO		
# static_ID	text	YES		