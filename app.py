from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

client = MongoClient('mongodb://farhan:farhan@ac-amvpek4-shard-00-00.fydd3ha.mongodb.net:27017,ac-amvpek4-shard-00-01.fydd3ha.mongodb.net:27017,ac-amvpek4-shard-00-02.fydd3ha.mongodb.net:27017/?ssl=true&replicaSet=atlas-qout9c-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.sparta

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    description = og_description['content']
    
    doc = {
        'image': image,
        'title': title,
        'description': description,
        'star': star_receive,
        'comment': comment_receive,
    }

    db.movies.insert_one(doc)

    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
   
   
