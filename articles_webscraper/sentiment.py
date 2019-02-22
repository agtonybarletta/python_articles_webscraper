import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('punkt')

def sentiment(text, lan='en'):
    sid = SentimentIntensityAnalyzer()
    #pdb.set_trace()
    acc = 0
    count = 0
    for sentence in nltk.word_tokenize(text):
       # print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in ss:
            if ss['compound'] != 0:
                acc += ss['compound']
                count+=1
            #print('{0}: {1}, '.format(k, ss[k]), end =' ')
        #print()
    if count != 0:
        return acc/count
    else:
        return 0
