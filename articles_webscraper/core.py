
from webscraper import SearchEngineArticles
from article import get_article, get_article_fast
from sentiment import sentiment
import datetime
import json
import csv
import os


data_dir = 'data'
start_date = '01/02/2017'
n_week =3 
list_scores = []

dt_start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
dt_end_date = dt_start_date + datetime.timedelta(days=6)
end_date = dt_end_date.strftime('%m/%d/%Y')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
with open(os.path.join(data_dir,'total-scores.csv'),'w') as total_file:
    writer = csv.writer(total_file, delimiter=',')
    for j in range(0,n_week):
        if not os.path.exists(os.path.join(data_dir,dt_start_date.strftime('%Y-%m-%d.json'))):
            list_articles = []
            score_item = {}
            it_obj= SearchEngineArticles("elon musk news", 'https://www.google.com/search?',n_articles=20, min_date=start_date, max_date=end_date)
            i = 0
            acc = 0
            count = 0
            for l in it_obj:
                try:
                    tmp_item = {}
                    tmp_item['url'] = l
                    print('fetching article at ',l)
                    title, article = get_article_fast(l)
                    tmp_item['title']= title
                    tmp_item['article'] = article
                    tmp_item['index'] = i


                    if title is not None and article is not None:
                        score = sentiment(article)
                        tmp_item['score']=score
                        list_articles.append(tmp_item)
                        if score != 0:
                            count+= 1
                            acc += score
                    print('parsed {0}, score {1}, url {2}'.format(i, score,l))
                    i+=1
                except Exception as e:
                    print(e)

            if count != 0:
                avg_score = acc/count
            else:
                avg_score = -1
            score_item['start-date'] = start_date
            score_item['end-date'] = end_date
            score_item['week'] = j
            score_item['score'] = avg_score
            list_scores.append(score_item)
            with open(os.path.join(data_dir,dt_start_date.strftime('%Y-%m-%d.json')),'w') as output:
                json.dump(list_articles,output)
                output.close()
            print('week {0}, date {1} score {2}'.format(j,start_date,avg_score))
            dt_start_date = dt_end_date + datetime.timedelta(days=1)
            start_date = dt_start_date.strftime('%m/%d/%Y')
            dt_end_date = dt_start_date + datetime.timedelta(days=6)
            end_date = dt_end_date.strftime('%m/%d/%Y')
            writer.writerow([score_item['start-date'],
                             score_item['end-date'],
                             score_item['week'],
                             score_item['score']])
