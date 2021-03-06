import data_manager, connection, bcrypt

@connection.connection_handler
def sort_questions(cursor, header='submission_time'):
    cursor.execute(f""" SELECT question.id,submission_time,view_number,vote_number,title,message,users.username FROM question
                            LEFT JOIN users ON (users.id=user_id)
                        ORDER BY {header} DESC 
                        LIMIT 5; """)
    sorted_list = cursor.fetchall()
    return sorted_list


@connection.connection_handler
def answer_elements(cursor):
    cursor.execute(f"""
                    SELECT  answer.id, submission_time, vote_number, question_id, message,image, users.username FROM answer 
                        LEFT JOIN users ON (user_id=users.id)
                    """)
    sorted_list = cursor.fetchall()
    return sorted_list

@connection.connection_handler
def comment_elements(cursor):
    cursor.execute(f"""
                    SELECT  comment.id, question_id, answer_id, message,submission_time, users.username FROM comment 
                        LEFT JOIN users ON (user_id=users.id)
                    """)
    sorted_list = cursor.fetchall()
    return sorted_list


@connection.connection_handler
def answer_elements(cursor):
    cursor.execute(f"""
                    SELECT  answer.id, submission_time, vote_number, question_id, message,image, users.username, marked FROM answer 
                        LEFT JOIN users ON (user_id=users.id)
                    """)
    sorted_list = cursor.fetchall()
    return sorted_list

@connection.connection_handler
def comment_elements(cursor):
    cursor.execute(f"""
                    SELECT  comment.id, question_id, answer_id, message,submission_time, user_id, users.username FROM comment 
                        LEFT JOIN users ON (user_id=users.id)
                    """)
    sorted_list = cursor.fetchall()
    return sorted_list

@connection.connection_handler
def remove_question(cursor,id):
    cursor.execute(f"""
                    DELETE FROM question
                    WHERE id = {id}; 
                    """)


@connection.connection_handler
def remove_answer(cursor,id):
    cursor.execute(f"""
                        DELETE FROM answer
                        WHERE question_id = {id}; 
                        """)

@connection.connection_handler
def question_vote(cursor,question_id, vote):
    cursor.execute(f"""
                            UPDATE question
                            SET vote_number = vote_number+{vote}
                            WHERE id = {question_id}; 
                            """)


@connection.connection_handler
def answer_vote(cursor,answer_id, vote):
    cursor.execute(f"""
                        UPDATE answer
                        SET vote_number = vote_number+{vote}
                        WHERE id = {answer_id}; 
                    """)


@connection.connection_handler
def increase_view(cursor, question_id):
    cursor.execute(f"""
                    UPDATE question
                    SET view_number = view_number+ 1
                    WHERE id = {question_id};
                    """)



@connection.connection_handler
def edit_an_answer(cursor ,message, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET message = %s
                    WHERE id = %s;
                    """,(message,answer_id))

@connection.connection_handler
def get_question_id(cursor,answer_id):
    cursor.execute(f"""
                        SELECT question_id FROM answer
                        WHERE id = {answer_id};
                    """)
    question_id = cursor.fetchone()
    return  question_id['question_id']

@connection.connection_handler
def remove_coment(cursor, comment_id):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE id = {comment_id};
                    """)

@connection.connection_handler
def remove_comment_of_question(cursor, question_id):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE question_id = {question_id};
                    """)

@connection.connection_handler
def remove_comment_of_answer(cursor, answer_id):
    cursor.execute(f"""
                    DELETE FROM comment
                    WHERE answer_id= {answer_id};
                    """)

@connection.connection_handler
def get_question_id_from_ans(cursor, question_id):
    cursor.execute(f"""
                    SELECT id FROM answer
                    WHERE question_id={question_id};
                    """)
    id_of_answer = cursor.fetchall()
    return id_of_answer

@connection.connection_handler
def get_question_id_by_comm(cursor, comment_id):
    cursor.execute(f"""
                    SELECT question_id FROM comment
                    WHERE id={comment_id};
                    """)
    question_id = cursor.fetchone()
    return question_id['question_id']

@connection.connection_handler
def get_answer_id_by_com(cursor, comment_id):
    cursor.execute(f"""
                    SELECT answer_id FROM comment
                    WHERE id ={comment_id};
                    """)
    answer_id = cursor.fetchone()
    return answer_id['answer_id']

@connection.connection_handler
def edit_comment(cursor, message, comment_id):
    cursor.execute("""
                    UPDATE comment
                    SET message = %s
                    WHERE id = %s;
                    """, (message, comment_id))


@connection.connection_handler
def search_a_phrase(cursor, phrase):
    cursor.execute(f"""SELECT * FROM question
                        WHERE message LIKE '%{phrase}%' OR title LIKE '%{phrase}%';""")
    result=cursor.fetchall()
    return result

@connection.connection_handler
def confirm_user(cursor, usrname):
    cursor.execute(f"""
                    SELECT username FROM users
                    WHERE username = '{usrname}'; 
                    """)
    result = cursor.fetchall()
    if result != []:
        return True
    else:
        return False


@connection.connection_handler
def check_credentials(cursor, user):
    cursor.execute(f"""
                    SELECT password FROM users
                    WHERE username = '{user}';
                    """)
    result = cursor.fetchone()
    return result

def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

@connection.connection_handler
def get_username_id(cursor, usrname):
    cursor.execute(f'''
                        SELECT id FROM users
                        WHERE username = '{usrname}';
                        ''')
    result=cursor.fetchone()
    return result['id']

@connection.connection_handler
def get_username_by_id(cursor,id):
    cursor.execute(f'''
                        SELECT username FROM users
                        WHERE id = '{id}';
                    ''')
    result=cursor.fetchone()
    return result['username']

@connection.connection_handler
def get_question_by_user_id(cursor,user_id):
    cursor.execute(f'''
                    SELECT submission_time, view_number, vote_number, title, message FROM question
                    WHERE user_id='{user_id}';
                    ''')
    result=cursor.fetchall()
    return result

@connection.connection_handler
def get_answer_by_user_id(cursor,user_id):
    cursor.execute(f'''
                    SELECT submission_time, vote_number, message FROM answer
                    WHERE user_id='{user_id}';
                    ''')
    result=cursor.fetchall()
    return result


@connection.connection_handler
def get_comment_by_user_id(cursor,user_id):
    cursor.execute(f'''
                    SELECT submission_time, message FROM comment
                    WHERE user_id='{user_id}';
                    ''')
    result=cursor.fetchall()
    return result

@connection.connection_handler
def accept_answer(cursor,answer_id):
    cursor.execute(f'''
                    UPDATE answer SET marked=TRUE
                    WHERE id ='{answer_id}';
                    ''')



@connection.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    cursor.execute(f'''
                        SELECT user_id FROM question
                        WHERE id='{question_id}';
                    ''')
    result=cursor.fetchone()
    return result['user_id']

@connection.connection_handler
def change_reputation(cursor,user_id, points):
    cursor.execute(f"""
                    UPDATE users SET reputation=reputation+{points}
                    WHERE id='{user_id}';
                    """)

@connection.connection_handler
def remove_answer2(cursor, answer_id):
    cursor.execute(f"""
                    DELETE FROM answer
                    WHERE id = {answer_id};
                    """)

