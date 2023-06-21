import requests
import sqlite3
import baekjoon2
# 문제 변경사항 적용 기능 없음(새로고침 x)
columns = ["problemId", "titleKo", "isSolvable", "acceptedUserCount", "level", "votedUserCount", "averageTries", "official", "tips", "description"]

def check_and_save_problem(problemId:int):  # 이미 저장되었는지 확인하고 저장이 되어있지 않으면 검색 후 저장
    conn = sqlite3.connect('database.db')

    # 'titleKo' 값이 problemId인 행을 조회
    cursor = conn.execute("SELECT * FROM problems WHERE problemId = ?", (problemId,))
    row = cursor.fetchone()

    if row is None:
        # problemId가 데이터베이스에 존재하지 않으면 함수 실행
        save_to_database_byId(problemId)
        append_column_value(problemId, 'description', baekjoon2.get_problem_info(problemId))
    else:
        print("Problem already exists in the database.")

    conn.close()

def save_to_database(data):  # db에 저장
    conn = sqlite3.connect('database.db')

    # 데이터 삽입
    placeholders = ', '.join(['?' for _ in columns])
    query = f"INSERT INTO problems VALUES ({placeholders})"
    conn.execute(query, tuple(data))

    # 변경사항 커밋 및 연결 닫기
    conn.commit()
    conn.close()

def append_column_value(problemId, column_name, value):  # 특정 행열에 값 추가
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 기존 값 가져오기
    cursor.execute(f"SELECT {column_name} FROM problems WHERE problemId = ?", (problemId,))
    current_value = cursor.fetchone()

    # 새로운 값 추가
    new_value = current_value[0] + value if current_value[0] != None else value

    # 열 값 업데이트
    cursor.execute(f"UPDATE problems SET {column_name} = ? WHERE problemId = ?", (new_value, problemId))

    conn.commit()
    conn.close()

def clear_column_value(problemId, column_name):  # 특정 행열 값 제거
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 열 값 비우기
    cursor.execute(f"UPDATE problems SET {column_name} = NULL WHERE problemId = ?", (problemId,))

    conn.commit()
    conn.close()


def save_to_database_byTitle(problemTitle):  # 미완성, 제목으로 검색 후 저장
    url = f'https://solved.ac/api/v3/problem/show?problemTitle={problemTitle}'

    response = requests.get(url)
    data = response.json()
    
    # 데이터의 인덱스들을 리스트에 매핑
    indexes = [data[key] for key in columns]

    save_to_database(indexes)

def save_to_database_byId(problem_id):  # id로 검색 후 저장
    url = f'https://solved.ac/api/v3/problem/show?problemId={problem_id}'

    response = requests.get(url)
    data = response.json()
    for c in columns:
        if c not in data:
            data[c] = None
    # 데이터의 인덱스들을 리스트에 매핑
    indexes = [data[key] for key in columns]

    save_to_database(indexes)


def firstStart():  # 최초 실행 시 환경 설정
    conn = sqlite3.connect('database.db')
    # problems 테이블 생성
    conn.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            problemId INTEGER PRIMARY KEY,
            titleKo TEXT,
            isSolvable INTEGER,
            acceptedUserCount INTEGER,
            level INTEGER,
            votedUserCount INTEGER,
            averageTries REAL,
            official INTEGER,
            tips TEXT,
            description TEXT
        )
    ''')
    conn.close()


def retrieve_data(): # 모든 row 출력
    conn = sqlite3.connect('database.db')
    
    # SELECT 문 실행
    cursor = conn.execute("SELECT * FROM problems")

    # 결과 가져오기
    rows = cursor.fetchall()

    # 결과 출력
    for row in rows:
        print(row)

    conn.close()


def retrieve_data_titleKolevel():  # titleKo와 level 열의 값 조회
    conn = sqlite3.connect('database.db')

    cursor = conn.execute("SELECT titleKo, level FROM problems")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


def retrieve_data_by_title(title: str):  # 제목에 해당하는 데이터를 출력
    conn = sqlite3.connect('database.db')

    cursor = conn.execute(f"SELECT * FROM problems WHERE {columns[1]} = ?", (title,))

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


def retrieve_data_by_id(problemId: str):  # ID에 해당하는 데이터를 출력
    try:
        check_and_save_problem(int(problemId))
        conn = sqlite3.connect('database.db')
        cursor = conn.execute(f"SELECT * FROM problems WHERE {columns[0]} = ?", (problemId,))
        rows = cursor.fetchall()
        returningTup = ()
        for row in rows:
            returningTup+=row
        conn.close()
        return returningTup
    except:
        return '해당 문제를 업데이트 중입니다. 잠시후 다시 시도해 주세요.'

def problem_info(problemId: str):
    column = columns.index('description')
    return retrieve_data_by_id(problemId)[column]  # 문자열 반환

# 열을 추가할때 사용
def add_column(column_name, column_type): # 사용 예제 : add_column("tips", "TEXT")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 새로운 열 추가 쿼리 실행
    cursor.execute(f"ALTER TABLE problems ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()








#---------------------------------------------

# retrieve_data_by_title('A+B')
# retrieve_data_titleKolevel()
# check_and_save_problem(1002)
#append_column_value(1000, 'tips', 'Some tips')
# clear_column_value(1000, 'tips')
#append_column_value(1000, 'description', baekjoon2.get_problem_info(1000))
