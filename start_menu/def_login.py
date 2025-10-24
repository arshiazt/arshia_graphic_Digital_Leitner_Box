from data_base.db import get_connection

def login(user_name,password,number,user_number):
    if user_name == '' or password == '' or user_number == '':
        return False,False,'Please fill in all fields.'
    if str(number) != user_number:
        return False,False,'Please enter corrcet number.'
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,password FROM users WHERE username=%s"
    cur.execute(query,(user_name,))
    result=cur.fetchone()
    conn.close()
    if not result:
        return False,False,'There is no username!'
    if result[1] == password:
        return True,result[0],f'Welcome my friend {user_name}'
    else:
        return False,False,'The password is incorrect!'