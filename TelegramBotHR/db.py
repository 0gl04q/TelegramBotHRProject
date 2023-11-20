import psycopg2
from psycopg2 import OperationalError
from datetime import datetime

'''
    Файл для работы с базой данных, все подключения и запросы выполняются здесь
'''


def create_connect():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost'
    )

    cursor = conn.cursor()
    return cursor, conn


def first_query():
    '''
    Запрос для инициализации базы данных, необходим только 1 раз перед самым первым запуском
    '''

    query_dict = {
        'create_tables': '''
                    CREATE TABLE IF NOT EXISTS roles (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(20) NOT NULL
                    );
                    
                    CREATE TABLE IF NOT EXISTS languages (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL
                    );
                    
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        role_id INT,
                        language_id INT,
                        name VARCHAR(100) NOT NULL,
                        status BOOLEAN,
                        tg_id BIGINT NOT NULL UNIQUE,
                        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL,
                        FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE SET NULL
                    );

                    CREATE TABLE IF NOT EXISTS tests_types (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(20) NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS tests (
                        id SERIAL PRIMARY KEY,
                        type_id INT NOT NULL,
                        FOREIGN KEY (type_id) REFERENCES tests_types(id) ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS tests_names (
                        id SERIAL PRIMARY KEY,
                        test_id INT NOT NULL,
                        language_id INT NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
                        FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE SET NULL
                    );

                    CREATE TABLE IF NOT EXISTS results_tests (
                        id SERIAL PRIMARY KEY,
                        user_id INT NOT NULL,
                        test_id INT NOT NULL,
                        total SMALLINT NOT NULL,
                        date TIMESTAMPTZ,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS questions (
                        id SERIAL PRIMARY KEY,
                        test_id INT NOT NULL,
                        language_id INT NOT NULL,
                        name VARCHAR(200) NOT NULL,
                        FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
                        FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE SET NULL
                    );
                
            ''',

        'insert_roles': '''
                INSERT INTO roles (id, name) VALUES (0, 'HR'), (1, 'Пользователь') ON CONFLICT DO NOTHING;
            ''',

        'insert_languages': '''
                INSERT INTO languages (id, name) VALUES (0, 'ru'), (1, 'en') ON CONFLICT DO NOTHING;
            ''',

        'insert_types': '''
                INSERT INTO tests_types (id, name) VALUES (0, 'Q12'), (1, 'eNps') ON CONFLICT DO NOTHING;
            ''',

        'insert_su': '''     
                INSERT INTO users (id, role_id, language_id, name, status, tg_id) 
                    VALUES (0, 0, 0, 'OglO4q', TRUE, 1027070887) 
                    ON CONFLICT DO NOTHING;
            ''',

        'insert_tests': '''
                INSERT INTO tests (id, type_id) VALUES (0, 0), (1, 1) ON CONFLICT DO NOTHING;        
            ''',

        'insert_tests_names': '''
                    INSERT INTO tests_names (id, test_id, language_id, name) 
                    VALUES 
                        (0, 0, 0, 'Оценка труда'), 
                        (1, 0, 1, 'Job evaluation'), 
                        
                        (2, 1, 0, 'Рекомендация места работы'),
                        (3, 1, 1, 'Recommendation of a place of work')
                        
                        ON CONFLICT DO NOTHING;        
                ''',

        'insert_questions': '''
                INSERT INTO questions (id, test_id, language_id, name) 
                    VALUES
                        (0, 0, 0, 'В последнее время, у меня была возможность заниматься интересными задачами и проектами на работе?'),
                        (1, 0, 0, 'Я чувствую, что мой труд и вклад в работу оцениваются и признаются моими руководителями?'),
                        (2, 0, 0, 'У меня есть возможность использовать свои профессиональные навыки и навыки, чтобы эффективно выполнять свою работу?'),
                        (3, 0, 0, 'Мне предоставляется достаточное количество задач и ответственности, чтобы чувствовать себя полезным и востребованным?'),
                        (4, 0, 0, 'У меня есть возможность развиваться и усовершенствовать свои профессиональные навыки на рабочем месте?'),
                        (5, 0, 0, 'Я чувствую, что моя работа имеет смысл и приносит вклад в общий успех компании?'),
                        (6, 0, 0, 'Меня поддерживают в развитии моих профессиональных целей?'),
                        (7, 0, 0, 'У меня есть возможность вносить предложения и идеи, касающиеся моей работы и рабочих процессов?'),
                        (8, 0, 0, 'Я ощущаю баланс между тем, что я делаю на работе, и тем, что мне интересно и важно?'),
                        (9, 0, 0, 'Мои руководители обеспечивают конструктивный обратную связь по моей работе, помогая мне расти и улучшаться?'),
                        (10, 0, 0, 'Я чувствую, что мои усилия направлены на достижение общих целей и стратегических приоритетов компании?'),
                        (11, 0, 0, 'У меня есть возможность принимать участие в проектах или инициативах, которые соответствуют моим интересам и профессиональным целям?'),
                        
                        (12, 0, 1, 'Lately, have I had the opportunity to take on interesting tasks and projects at work?'),
                        (13, 0, 1, 'Do I feel like my work and contributions are valued and recognized by my managers?'),
                        (14, 0, 1, 'Am I able to use my professional skills and abilities to do my job effectively?'),
                        (15, 0, 1, 'Am I given enough tasks and responsibilities to feel useful and needed?'),
                        (16, 0, 1, 'Do I have the opportunity to develop and improve my professional skills in the workplace?'),
                        (17, 0, 1, 'Do I feel like my work is meaningful and contributes to the overall success of the company?'),
                        (18, 0, 1, 'Am I supported in developing my professional goals?'),
                        (19, 0, 1, 'Do I have the opportunity to make suggestions and ideas regarding my work and work processes?'),
                        (20, 0, 1, 'Do I feel a balance between what I do at work and what is interesting and important to me?'),
                        (21, 0, 1, 'Do my managers provide constructive feedback on my performance to help me grow and improve?'),
                        (22, 0, 1, 'Do I feel like my efforts are aimed at achieving the overall goals and strategic priorities of the company?'),
                        (23, 0, 1, 'Do I have the opportunity to participate in projects or initiatives that align with my interests and professional goals?'),
                        
                        (24, 1, 0, 'Насколько вероятно, что вы порекомендуете Компанию в качестве места работы своим друзьям и знакомым?'),
                        (25, 1, 1, 'How likely is it that you would recommend the Company as a place of work to your friends and acquaintances?')
                        
                        ON CONFLICT DO NOTHING;    
                                 
            ''',

    }
    cursor, conn = create_connect()

    try:
        for query in query_dict:
            cursor.execute(query_dict[query])
            conn.commit()
        return True
    except OperationalError:
        return False
    finally:
        cursor.close()
        conn.close()


def get_user_tests(user_id, language_id):
    cursor, conn = create_connect()

    select_query = f'''
            SELECT t.id, tn.name
              FROM tests as t
              JOIN results_tests as rt ON rt.test_id = t.id
              JOIN tests_names as tn ON tn.test_id = t.id
             WHERE rt.user_id = {user_id} AND rt.date IS NULL AND tn.language_id={language_id}
    '''

    try:
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_questions(test_id, language_id):
    cursor, conn = create_connect()

    select_query = f'''
        SELECT name 
          FROM questions
         WHERE test_id={test_id} AND language_id={language_id}
    '''

    try:
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(tg_id):
    cursor, conn = create_connect()

    select_query = f'''       
            SELECT id, name, role_id, status
              FROM users
             WHERE tg_id={tg_id}
    '''

    try:
        cursor.execute(select_query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_type_test(test_id):
    cursor, conn = create_connect()

    select_query = f'''
        SELECT tt.id 
          FROM tests_types as tt
          JOIN tests as t ON t.type_id = tt.id
         WHERE t.id={test_id}
    '''

    try:
        cursor.execute(select_query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def update_result(test_id, user_id, result):
    cursor, conn = create_connect()

    formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    select_query = f'''
        UPDATE results_tests 
           SET 
               total={result}, 
               date='{formatted_datetime}' 
         WHERE 
               user_id={user_id} 
               AND test_id={test_id} 
               AND date IS NULL
       '''

    try:
        cursor.execute(select_query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def add_user(name, tg_id):
    cursor, conn = create_connect()
    select_query = f'''                 
        INSERT INTO users (role_id, language_id, name, status, tg_id)
             VALUES (1, 0, '{name}', TRUE, {tg_id})
        '''
    try:
        cursor.execute(select_query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_all_tests():
    cursor, conn = create_connect()
    select_query = f'''                 
        SELECT t.id, tn.name 
          FROM tests as t
          JOIN tests_names as tn ON tn.test_id = t.id
         WHERE tn.language_id = 0
        '''
    try:
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def check_test_result_user(tg_id, test_id):
    cursor, conn = create_connect()
    select_query = f'''       
            SELECT *
              FROM results_tests as rt
              JOIN users as u ON u.id = rt.user_id
             WHERE rt.test_id = {test_id} AND rt.date IS NULL AND u.tg_id = {tg_id}
        '''
    try:
        cursor.execute(select_query)
        return True if cursor.fetchone() else False

    finally:
        cursor.close()
        conn.close()


def check_admin_role(tg_id):
    cursor, conn = create_connect()
    select_query = f'''       
            SELECT role_id
              FROM users
             WHERE tg_id = {tg_id}
        '''
    try:
        cursor.execute(select_query)
        role = cursor.fetchone()[0]
        return role == 0

    finally:
        cursor.close()
        conn.close()


def check_user_role(tg_id):
    cursor, conn = create_connect()
    select_query = f'''       
            SELECT role_id
              FROM users
             WHERE tg_id = {tg_id}
        '''
    try:
        cursor.execute(select_query)
        role = cursor.fetchone()[0]
        return role == 1

    finally:
        cursor.close()
        conn.close()


def add_test_result_user(tg_id, test_id):
    cursor, conn = create_connect()

    user_id = get_user_by_id(tg_id)[0]

    select_query = f'''                 
        INSERT INTO results_tests (user_id, test_id, total, date)
             VALUES ({user_id}, {test_id}, 0, NULL)
        '''
    try:
        cursor.execute(select_query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_roles():
    cursor, conn = create_connect()
    select_query = f'''                 
        SELECT id, name 
          FROM roles
        '''
    try:
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def update_role_user(tg_id, role_id):
    cursor, conn = create_connect()

    select_query = f'''
        UPDATE users 
           SET 
               role_id={role_id}
         WHERE 
               tg_id={tg_id}
       '''

    try:
        cursor.execute(select_query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_types():
    cursor, conn = create_connect()
    select_query = f'''                 
        SELECT *
          FROM tests_types
        '''
    try:
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_results_tests(test_id):
    cursor, conn = create_connect()
    select_query = f'''                 
            SELECT id
              FROM results_tests
             WHERE test_id = {test_id}
            '''
    try:
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_results_tests_success(test_id):
    cursor, conn = create_connect()
    select_query = f'''                 
            SELECT u.name, rt.date
              FROM results_tests as rt
              JOIN users as u ON u.id = rt.user_id
             WHERE NOT rt.date IS NULL AND rt.test_id = {test_id}
            '''
    try:
        cursor.execute(select_query)
        rt_list = [f'{rt[0]} - {rt[1]}' for rt in cursor.fetchall()]
        return rt_list
    finally:
        cursor.close()
        conn.close()


def get_results_tests_no_success(test_id):
    cursor, conn = create_connect()
    select_query = f'''                 
            SELECT u.name
              FROM results_tests as rt
              JOIN users as u ON u.id = rt.user_id
             WHERE rt.date IS NULL AND rt.test_id = {test_id}
            '''
    try:
        cursor.execute(select_query)
        rt_list = [f'{rt[0]}' for rt in cursor.fetchall()]
        return rt_list
    finally:
        cursor.close()
        conn.close()


def get_language(tg_id):
    cursor, conn = create_connect()
    select_query = f'''       
                SELECT l.name
                  FROM languages as l
                  JOIN users as u ON l.id = u.language_id
                 WHERE u.tg_id = {tg_id}
            '''
    try:
        cursor.execute(select_query)
        language = cursor.fetchone()
        return language[0]

    finally:
        cursor.close()
        conn.close()


def get_language_id(tg_id):
    cursor, conn = create_connect()
    select_query = f'''       
                SELECT l.id
                  FROM languages as l
                  JOIN users as u ON l.id = u.language_id
                 WHERE u.tg_id = {tg_id}
            '''
    try:
        cursor.execute(select_query)
        language = cursor.fetchone()
        return language[0]

    finally:
        cursor.close()
        conn.close()


def get_all_languages():
    cursor, conn = create_connect()
    select_query = f'''       
                    SELECT id, name
                      FROM languages
                '''
    try:
        cursor.execute(select_query)
        language = cursor.fetchall()
        return language

    finally:
        cursor.close()
        conn.close()


def update_language(tg_id, language_id):
    cursor, conn = create_connect()

    select_query = f'''
        UPDATE users 
           SET 
               language_id={language_id}
         WHERE 
               tg_id={tg_id}
       '''

    try:
        cursor.execute(select_query)
        conn.commit()
    finally:
        cursor.close()
        conn.close()
