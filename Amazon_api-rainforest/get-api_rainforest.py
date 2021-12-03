import json
import requests
import pandas as pd
import sqlite3
from flask import Flask, app, render_template,request

conn = sqlite3.connect('amazon.db',check_same_thread=False)
c = conn.cursor()

params = {
  'api_key':'',
  'type':'' ,
  'amazon_domain':'' ,
  'asin': ''
}
def api_result(params):
  api_result = requests.get('https://api.rainforestapi.com/request', params)

  print(params)
  result = api_result.json()
  title = ''
  keywords_list = ''
  ASIN = ''
  rating = ''
  ratings_total = ''
  reviews_total = ''
  price = ''
  five_star_rating_percentage= ''
  five_star_rating_total= ''
  four_star_rating_percentage = ''
  four_star_rating_total = ''
  three_star_rating_percentage = ''
  three_star_rating_total = ''
  two_star_rating_percentage = ''
  two_star_rating_total = ''
  one_star_rating_percentage = ''
  one_star_rating_total = ''
  dim_weight = ''
  dimensions= ''
  weight= ''
  length=''
  breath=''
  height1=''
  height=''
  #print(result)
  try:
    title = result['product']['title']
    keywords_list = result['product']['keywords_list']
    ASIN = result['product']['asin']
    rating = result['product']['rating']
    ratings_total = result['product']['ratings_total']
    reviews_total = result['product']['reviews_total']
    price = result['product']['buybox_winner']['price']['raw']
    five_star_rating_percentage= result['product']['rating_breakdown']['five_star']['percentage']
    five_star_rating_total= result['product']['rating_breakdown']['five_star']['count']
    four_star_rating_percentage = result['product']['rating_breakdown']['four_star']['percentage']
    four_star_rating_total = result['product']['rating_breakdown']['four_star']['count']
    three_star_rating_percentage = result['product']['rating_breakdown']['three_star']['percentage']
    three_star_rating_total = result['product']['rating_breakdown']['three_star']['count']
    two_star_rating_percentage = result['product']['rating_breakdown']['two_star']['percentage']
    two_star_rating_total = result['product']['rating_breakdown']['two_star']['count']
    one_star_rating_percentage = result['product']['rating_breakdown']['one_star']['percentage']
    one_star_rating_total = result['product']['rating_breakdown']['two_star']['count']
    dim_weight = result['product']['dimensions']
    dimensions= dim_weight .split(';')[0]
    weight= dim_weight .split(';')[1]
    length=dimensions.split('x')[0]
    breath=dimensions.split('x')[1]
    height1=dimensions.split('x')[2]
    height=height1.split(' ')[1]
  except:
    pass
  c.execute('''INSERT INTO product_details VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (ASIN , title , price , rating ,five_star_rating_percentage ,five_star_rating_total ,four_star_rating_percentage ,four_star_rating_total ,three_star_rating_percentage ,three_star_rating_total ,two_star_rating_percentage ,two_star_rating_total ,one_star_rating_percentage ,one_star_rating_total, ratings_total , reviews_total , weight , length, breath , height ))
  conn.commit()
app = Flask(__name__)
@app.route('/',methods=['GET', 'POST'])
def home():
    Api_key= request.form.get('Api_key')
    Type= request.form.get('Type')
    Amazon_domain= request.form.get('Amazon_domain')
    ASIN= request.form.get('ASIN')
    print(Api_key,Amazon_domain,Type,ASIN)
    params['api_key']=Api_key
    params['type']=Type
    params['amazon_domain']=Amazon_domain
    params['asin']=ASIN
    api_result(params)
    return render_template('home.html')
 
if __name__ == '__main__':
 
    
    app.run(debug=True)











