from data_base.db import get_connection

def password_check(password):
    point=0
    if len(password)>8:
        point+=1
    for char in password:
        if char.isupper():
            point+=1
            break
    for char in password:
        if char.islower():
            point+=1
            break
    for num in password:
        if num.isdigit():
            point+=1
            break
    return point

def register(user_name,password,password2):
    if user_name == '' or password == '' or password2 == '':
        return False,'Please fill in all fields.'
    if password != password2:
        return False,'Passwords do not match.'
    point=password_check(password)
    if point != 4:
        return False,'At least 8 characters\nContains uppercase and lowercase letters \nContains numbers'
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT username FROM users WHERE username=%s"
    cur.execute(query,(user_name,))
    result=cur.fetchone()
    if result:
        conn.close()
        return False,'This username is available.'
    query2="INSERT INTO users (username,password) VALUES (%s,%s)"
    cur.execute(query2,(user_name,password))
    conn.commit()
    conn.close()
    return True,f'You registered with the user name {user_name}'