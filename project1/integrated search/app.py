# app.py (수정 완료된 전체 코드)

from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
import os
from flask_session import Session  # 👈 1. 라이브러리 임포트
from pymongo import MongoClient

# 모듈 임포트
from modules.nvd_fetcher import fetch_nvd_cves
from modules.hackernews_fetcher import fetch_hacker_news
from modules.data_processor import process_results
from modules.report_generator import create_excel_report
from modules.notification import send_slack_file, send_email_with_attachment
from bson.objectid import ObjectId
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SLACK_CHANNEL_ID = "C09544MKA74"

@app.route('/', methods=['GET'])
def index():

    session.pop('last_report_path', None)
    session.pop('last_results', None)
    client = MongoClient('mongodb://localhost:27017')

    db1 = client['keywods']
    collection1 = db1['keywods_data']
    pipeline = [
        {"$group": {"_id": "$keyword", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    keyword_ranking = list(collection1.aggregate(pipeline))

    db2 = client['keywods']  
    collection2 = db2['keywods_data']
    recent_keywords = list(collection2.find().sort("searched_at", -1).limit(10))

    return render_template(
        'index.html',
        keyword_ranking=keyword_ranking,
        recent_keywords=recent_keywords
    )

@app.route('/delete_keyword', methods=['POST'])
def delete_keyword():
    keyword_id = request.form.get("keyword_id")
    if keyword_id:
        client = MongoClient('mongodb://localhost:27017')
        db = client['keywods']
        collection = db['keywods_data']
        collection.delete_one({"_id": ObjectId(keyword_id)})
        flash("최근 검색 키워드가 삭제되었습니다.", "success")
    else:
        flash("삭제할 키워드를 찾을 수 없습니다.", "error")
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    keywords_str = request.form.get("keyword")
    sources = request.form.getlist("source")
    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
    
    if not keywords or not sources:
        flash("검색할 키워드를 입력하고, 소스를 1개 이상 선택해주세요.", "error")
        return redirect(url_for('index'))

    all_results = [] 

     
    client = MongoClient('mongodb://localhost:27017')
    db = client['keywods']
    collection = db['keywods_data']
    now = datetime.utcnow()

    for keyword in keywords:
        collection.insert_one({
            "keyword": keyword,
            "searched_at": now
        })


    print(f"검색 시작: 키워드({keywords}), 소스({sources})")
    
    if 'nvd' in sources:
        print("NVD 검색 중...")
        nvd_results = fetch_nvd_cves(keywords, days=30)
        all_results.extend(nvd_results)
        print(f"NVD 검색 완료: {len(nvd_results)}건")
    
    if 'hackernews' in sources:
        print("해커뉴스 검색 중...")
        for keyword in keywords:
            hackernews_results = fetch_hacker_news(keyword)
            all_results.extend(hackernews_results)
        print(f"해커뉴스 검색 완료")

    if not all_results:
        flash(f"'{keywords_str}'에 대한 검색 결과가 없습니다. 다른 키워드로 시도해보세요.", "info")
        return redirect(url_for('index'))

    print(f"총 {len(all_results)}건 검색 완료. 보고서 생성 중...")
    processed_data = process_results(all_results)
    report_path = create_excel_report(processed_data)
    session['last_report_path'] = report_path
    session['last_results'] = processed_data
    
    return redirect(url_for('show_result'))


@app.route('/keyword_ranking')
def keyword_ranking():
    client = MongoClient('mongodb://localhost:27017')
    db = client['keywods']
    collection = db['keywods_data']

    pipeline = [
        {"$group": {
            "_id": "$keyword",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]

    ranking = list(collection.aggregate(pipeline))
    return render_template("keyword_ranking.html", ranking=ranking)

@app.route('/recent_keywords')
def recent_keywords():
    client = MongoClient('mongodb://localhost:27017')
    db = client['keywords_db']
    collection = db['keywords_log']

    recent_logs = collection.find().sort("searched_at", -1).limit(20)  # 최신 20건
    return render_template('recent_keywords.html', logs=recent_logs)

    """
    client = MongoClient('mongodb://localhost:27017')
    db = client['keywods']
    collection = db['keywods_data']  # 검색 기록을 저장하는 컬렉션

    now = datetime.utcnow()

    # 키워드마다 시간과 함께 insert
    for keyword in keywords:
        collection.insert_one({
            "keyword": keyword,
            "searched_at": now
        })

        return redirect(url_for('show_result'))


    @app.route('/recent_keywords')
    def recent_keywords():
        client = MongoClient('mongodb://localhost:27017')
        db = client['keywords_db']
        collection = db['keywords_log']

        recent_logs = collection.find().sort("searched_at", -1).limit(20)  # 최신 20건
        return render_template('recent_keywords.html', logs=recent_logs)



    # -> Mongo DB에서 키워드 가져와서 표시. + 시간
    # 시간대별 정렬
    """


@app.route('/result')
def show_result():
    results = session.get('last_results')
    if not results:
        # 세션 데이터가 없으면 메인으로 리디렉션
        return redirect(url_for('index'))
    
    high_risk_results = [
        r for r in results 
        if isinstance(r.get('score'), (int, float)) and r.get('score') >= 9.0
    ]
    return render_template('result.html', 
                           data_all=results, 
                           data_high=high_risk_results)

@app.route('/download')
def download():
    report_path = session.get('last_report_path')
    if report_path and os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    flash("보고서 파일을 찾을 수 없습니다. 다시 검색해주세요.", "error")
    return redirect(url_for('index'))

@app.route('/send_slack')
def slack():
    report_path = session.get('last_report_path')
    if report_path and os.path.exists(report_path):
        total_count = len(session.get('last_results', []))
        message = f"새로운 보안 리포트가 생성되었습니다. (총 {total_count}건)"
        send_slack_file(SLACK_CHANNEL_ID, report_path, message)
        flash(f"'{os.path.basename(report_path)}' 파일을 슬랙으로 전송했습니다.", "success")
    else:
        flash("슬랙으로 보낼 보고서가 없습니다. 먼저 검색을 실행해주세요.", "error")
    return redirect(url_for('show_result'))

@app.route('/send_email', methods=['POST'])
def email():
    report_path = session.get('last_report_path')
    email_addr = request.form.get("email_address")
    if report_path and os.path.exists(report_path) and email_addr:
        send_email_with_attachment(report_path, email_addr)
        flash(f"보고서를 {email_addr} (으)로 전송했습니다.", "success")
    else:
        flash("이메일로 보낼 보고서가 없거나 이메일 주소가 올바르지 않습니다.", "error")
    return redirect(url_for('show_result'))

if __name__ == '__main__':
    if not os.path.exists('reports'):
        os.makedirs('reports')
    # flask_session이 세션 파일을 저장할 폴더 생성
    if not os.path.exists('flask_session'):
        os.makedirs('flask_session')
    app.run(host='0.0.0.0', port=5001, debug=True)