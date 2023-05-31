# 백엔드에 해당하는 Script
from flask import Flask, render_template
from flask import request
import pymysql # pip install pymysql 해주고 작성

#DB 연동
db_conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd= '1234',
    db = 'test',
    charset ='utf8'
)   
print(db_conn) # connection 되는지 확인
# 안되는 경우 -> 작업관리자 -> 서비스 -> oracle부분에 on/off 확인
#===========================================================================================

# Flask 객체 인스턴스 생성
app = Flask(__name__)

#signup.html 열기 위한 함수
@app.route('/')
def signup():
    return render_template('signup.html')


#
@app.route('/signup', methods=['POST'])  # method가 아니라 methods이고 s 붙이는거 명심
def signupPost():
    uid = request.form['user_id']  # dictonary라서 index방법 대괄호 사용 --> html에 name 기준으로 불러오기
    upwd = request.form['user_pwd']
    uemail = request.form['user_email']
    uphone = request.form['user_phone']
    print(uid, upwd, uemail, uphone)
    return render_template('signup.html')

# 커서 객체 생성
@app.route('/sqltest')
def sqltest():
    cursor = db_conn.cursor()

    query = 'select * from player'

    cursor.execute(query)  # 리스트형태로 반환

    result = []
    for i in cursor:
        temp = {'player_id' : i[0], 'player_name' : i[1]}
        result.append(temp)
    return render_template('sqltest.html', result_table = result)
# 선수 상세정보 만들기
@app.route('/detail')
def detailtest():
    temp = request.args.get('id')
    temp1 = request.args.get('name')

    cursor = db_conn.cursor()

    query = "select * from player where player_id = {} and player_name like '{}'".format(temp, temp1)

    cursor.execute(query)

    result = []
    for i in cursor:
        temp = {'player_id' : i[0], 'player_name' : i[1], 'team_name': i[2], 'height' : i[-2], 'weight' : i[-1]}
        result.append(temp)

    return render_template('detail.html', result_table = result)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="127.0.0.1", port='7000')   #host와 port를 변경하는 방법