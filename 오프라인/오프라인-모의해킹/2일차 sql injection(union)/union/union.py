from flask import Flask
from flask import request
import sqlite3

# Seyong Kim.
app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get('name', "")
    html = '''
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Union SQL Injection</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css"
        integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
        integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js"
        integrity="sha384-oesi62hOLfzrys4LxRF63OJCXdXDipiYWBnvTl9Y9/TRlw5xlKIEHpNyvvDShgf/"
        crossorigin="anonymous"></script>
</head>

<body>
    <div class="container">
        <form class="row g-3">
            <div class="col-md-1">
                <label for="name" class="form-label">이름</label>
            </div>
            <div class="col-md-4">
                <input type="text" class="form-control" id="name" name="name">
            </div>
            <div class="col-md-3">
                <button class="btn btn-secondary" type="submit">검색</button>
            </div>
        </form>
    </div>
    <div class="container">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">이름</th>
                    <th scope="col">점수</th>
                    <th scope="col">지역</th>
                    <th scope="col">취미</th>
                    <th scope="col">나이</th>
                </tr>
            </thead>
            <tbody>
          
            

    '''
    con = sqlite3.connect('union.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    query = "SELECT * FROM profile WHERE name like '%" + name + "%';"
    #query = "SELECT * FROM profile;"    
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        html += "<tr><th scope='row'>" + str(row[0]) + "</th><td>" + str(row[1]) + "</td><td>" + str(row[2]) + "</td><td>" + str(row[3]) + "</td><td>" + str(row[4]) + "</td></tr>"
    html += '''
    </tbody>
        </table>
    </div>
</body>

</html>
    '''
    return html


if __name__ == '__main__':
    app.run(debug=True)
