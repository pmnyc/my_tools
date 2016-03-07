"""
Preprocess ufo_awesome.tsv file and generate different feature sets
"""

from nltk import clean_html
from nltk import SnowballStemmer
from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re

# Tokenizing (Document to list of sentences. Sentence to list of words.)
def tokenize(str):
	'''Tokenizes into sentences, then strips punctuation/abbr, converts to lowercase and tokenizes words'''
	return 	[word_tokenize(" ".join(re.findall(r'\w+', t,flags = re.UNICODE | re.LOCALE)).lower()) 
			for t in sent_tokenize(str.replace("'", ""))]

#Removing stopwords. Takes list of words, outputs list of words.
def remove_stopwords(l_words, lang='english'):
	l_stopwords = stopwords.words(lang)
	content = [w for w in l_words if w.lower() not in l_stopwords]
	return content
		
#Clean HTML / strip tags TODO: remove page boilerplate (find main content), support email, pdf(?)
def html2text(str):
	return clean_html(str)
		
#Stem all words with stemmer of type, return encoded as "encoding"
def stemming(words_l, type="PorterStemmer", lang="english", encoding="utf8"):
	supported_stemmers = ["PorterStemmer","SnowballStemmer","LancasterStemmer","WordNetLemmatizer"]
	if type is False or type not in supported_stemmers:
		return words_l
	else:
		l = []
		if type == "PorterStemmer":
			stemmer = PorterStemmer()
			for word in words_l:
				l.append(stemmer.stem(word).encode(encoding))
		if type == "SnowballStemmer":
			stemmer = SnowballStemmer(lang)
			for word in words_l:
				l.append(stemmer.stem(word).encode(encoding))
		if type == "LancasterStemmer":
			stemmer = LancasterStemmer()
			for word in words_l:
				l.append(stemmer.stem(word).encode(encoding))
		if type == "WordNetLemmatizer": #TODO: context
			wnl = WordNetLemmatizer()
			for word in words_l:
				l.append(wnl.lemmatize(word).encode(encoding))
		return l

#The preprocess pipeline. Returns as lists of tokens or as string. If stemmer_type = False or not supported then no stemming.		
def preprocess_pipeline(str, lang="english", stemmer_type="PorterStemmer", return_as_str=False, 
						do_remove_stopwords=False, do_clean_html=False):
	l = []
	words = []
	if do_clean_html:
		sentences = tokenize(html2text(str))
	else:
		sentences = tokenize(str)
	for sentence in sentences:
		if do_remove_stopwords:
			words = remove_stopwords(sentence, lang)
		else:
			words = sentence
		words = stemming(words, stemmer_type)
		if return_as_str:
			l.append(" ".join(words))
		else:
			l.append(words)
	if return_as_str:
		return " ".join(l)
	else:
		return l






import json
import pandas as pd
from dateutil import parser
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
# from preprocessing import preprocess_pipeline
from sklearn.feature_extraction import DictVectorizer
import logging
# import nimfa
import cPickle as pickle
import nltk
from scipy.sparse import hstack

logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s", level=logging.INFO, datefmt='%m/%d/%y %H:%M:%S')    

def main():
    
    with open('H:/TextMining/ZhaoXingExamples/tm.csv') as f:
        data = f.readlines()
    f.close()

    # remove messy data instances 
    data = [line.split('\t') for line in data if len(line.split('\t'))>=6]
    # replace '\t' in description with ' ', because '\t' is exclusively used as delimiter for columns
    for idx in xrange(len(data)):
        data[idx][5] = ' '.join(data[idx][5:])
        data[idx]='\t'.join(data[idx][:6])        
    # save cleaned data into ufo_awesome2.tsv file
    with open('H:/TextMining/ZhaoXingExamples/tm2.csv', 'w') as f:
        for line in data:
            f.write(line)    
    f.close()

    
    dm = pd.read_csv('H:/TextMining/ZhaoXingExamples/tm2.csv', sep='\t', names=['sighted_at','reported_at','location','shape','duration','description'], header=None)

    dm['sighted_at'] = dm['sighted_at'].astype(str)
    for idx in dm.index:
        try:
            dm['sighted_at'][idx] = parser.parse(dm['sighted_at'][idx])
        except:
            dm['sighted_at'][idx] = None        
    dm['sighted_at_year'] = dm['sighted_at'].map(lambda x: x.year if x is not None else -1)
    dm['sighted_at_month'] = dm['sighted_at'].map(lambda x: x.month if x is not None else -1)
    dm['sighted_at_day'] = dm['sighted_at'].map(lambda x: x.day if x is not None else -1)
    dm['sighted_at_weekday'] = dm['sighted_at'].map(lambda x: x.weekday() if x is not None else -1)

    dm['reported_at'] = dm['reported_at'].astype(str)
    for idx in dm.index:
        try:
            dm['reported_at'][idx] = parser.parse(dm['reported_at'][idx])
        except:
            dm['reported_at'][idx] = None        
    dm['reported_at_year'] = dm['reported_at'].map(lambda x: x.year if x is not None else -1)
    dm['reported_at_month'] = dm['reported_at'].map(lambda x: x.month if x is not None else -1)
    dm['reported_at_day'] = dm['reported_at'].map(lambda x: x.day if x is not None else -1)
    dm['reported_at_weekday'] = dm['reported_at'].map(lambda x: x.weekday() if x is not None else -1)

    # compute dlapse time between sighted_at and reported_at
    dm['days_elapse'] = np.nan
    for idx in dm.index:
        if dm['sighted_at'][idx] is not None and dm['reported_at'] is not None:
            dm['days_elapse'][idx] = (dm['reported_at'][idx] - dm['sighted_at'][idx]).days
    # want to quantify seasonality difference between sighted_at and reported_at
    dm['season_difference'] = dm['days_elapse'].map(lambda x: x/365.0 - int(x/365.0) if ~np.isnan(x) else np.nan)

    # one-hot encoding for state
    dm['state'] = dm['location'].map(lambda x: x.split(',')[1])
    vec = DictVectorizer()
    X_state = vec.fit_transform([ {'state': dm['state'][idx]} for idx in dm.index ])
    # tf-idf encoding for location
    tfv = TfidfVectorizer(min_df=10, strip_accents='ascii', analyzer='word', token_pattern=r'\w{1,}',ngram_range=(1,1), use_idf=1, smooth_idf=1, sublinear_tf=1)
    X_location = tfv.fit_transform(dm['location'])

    # regular expression to numeric value for duration 
    dm['duration2'] = np.nan
    for idx in dm.index:
        if type(dm['duration'][idx]) is str:
            search_string = dm['duration'][idx].lower()
            search_string = search_string.replace('an ', '1 ')
            search_string = search_string.replace('one ', '1 ')
            search_string = search_string.replace('two ', '2 ')
            search_string = search_string.replace('few ', '5 ')
            search_string = search_string.replace('several ', '5 ')
            
            m_obj = re.search(r"(\d*\.\d+|\d+)\s*(to|-|=)\s*(\d*\.\d+|\d+)\D*(min|sec|hour|hr|week|mims|mn\.).*", search_string)
            if m_obj:            
                num1 = float(m_obj.group(1))
                num2 = float(m_obj.group(3))
                num = (num1+num2)/2.0            
                if m_obj.group(2) in ('min','mims','mn.'):
                    num = num*60
                elif m_obj.group(4) in ('hour','hr'):
                    num = num*3600            
                elif m_obj.group(4) in('sec'):
                    pass
                elif m_obj.group(2)=='week':
                    num = num*7*24*3600
                dm['duration2'][idx] = num
                continue
            
            m_obj = re.search(r"(\d*\.\d+|\d+|)\D*(min|sec|hour|hr|week|mims|mn\.).*", search_string)
            if m_obj:            
                if m_obj.group(1)=='':
                    num = 5
                else:
                    num = float(m_obj.group(1))
                if m_obj.group(2) in ('min','mims','mn.'):
                    num = num*60
                elif m_obj.group(2) in ('hour','hr'):
                    num = num*3600            
                elif m_obj.group(2) in('sec'):
                    pass
                elif m_obj.group(2)=='week':
                    num = num*7*24*3600
                dm['duration2'][idx] = num
                continue

            m_obj = re.search(r"(\d*\.\d+|\d+)\D*(min|sec|hour|hr|week|mims|mn\.|).*", search_string)
            if m_obj:                        
                num = float(m_obj.group(1))
                if m_obj.group(2) in ('min','mims','mn.'):
                    num = num*60
                elif m_obj.group(2) in ('hour','hr'):
                    num = num*3600            
                elif m_obj.group(2) in('sec',''):
                    pass
                elif m_obj.group(2)=='week':
                    num = num*7*24*3600
                dm['duration2'][idx] = num
                continue
            
    # tf-idf encoding for duration
    tfv = TfidfVectorizer(min_df=10, strip_accents='ascii', analyzer='word', token_pattern=r'\w{1,}',ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1)
    duration = dm['duration'].map(lambda x: x if type(x) is str else '')
    X_duration = tfv.fit_transform(duration)

    # X_basic dataset
    X_basic = np.array(dm[['sighted_at_year', 'sighted_at_month', 'sighted_at_day', 'sighted_at_weekday', 'reported_at_year', \
                           'reported_at_month', 'reported_at_day', 'reported_at_weekday', 'days_elapse', 'season_difference', 'duration2']])

    # tf-idf encoding for description
    tfv = TfidfVectorizer(min_df=100, max_df = 0.3, strip_accents='ascii', analyzer='word', token_pattern=r'\w{1,}',ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1)
    origin_desc =  list(dm['description'])
    X_origin_desc = tfv.fit_transform(origin_desc)

    # do stemming&lemmalization on description, then then do tf-idf encoding
    try:
        with open("cache/preprocessed.pkl", 'rb') as f:
            X_preprocessed = pickle.load(f)
    except IOError:
        preprocessed = [ preprocess_pipeline(dm['description'][idx], "english", "WordNetLemmatizer", True, False, False) for idx in dm.index ]
        X_preprocessed = tfv.fit_transform(preprocessed)
        with open("cache/preprocessed.pkl", 'wb') as f:
            pickle.dump(X_preprocessed, f, pickle.HIGHEST_PROTOCOL)

    # nmf decomposition to extrect top 20 topics from tf-idf matrix
    try:
        with open("cache/topic20.pkl", 'rb') as f:
            X_topic20 = pickle.load(f)
    except IOError:
        logging.info('start nfm decomposition')
        fctr = nimfa.mf(X_origindesc, seed = 'random_vcol', method = 'lsnmf', rank = 20, max_iter = 10)
        fctr_res = nimfa.mf_run(fctr)
        X_topic20 = fctr_res.basis()
        logging.info('start nfm decomposition')
        with open("cache/topic20.pkl", 'wb') as f:
            pickle.dump(X_topic20, f, pickle.HIGHEST_PROTOCOL)

    # nltk tagging, it will take 3-4 hours to run in my machine (2.4GHz CPU, 64GB memory) 
    try:
        with open("cache/tagging_raw.pkl", 'rb') as f:
           tagging_raw= pickle.load(f)
    except IOError:
        logging.info('start tagging')
        tagging_raw = []
        for idx, sent in enumerate(origin_desc):
            if idx%100 == 0:
                logging.info('doing tagging %d', idx)
            tagging_raw.append(nltk.pos_tag(nltk.word_tokenize(sent)))
        with open("cache/tagging_raw.pkl", 'wb') as f:
            pickle.dump(X_txt_tag, f, pickle.HIGHEST_PROTOCOL)
        logging.info('finishe tagging')

    # tf-idf on nouns from nltk tagging
    tagging_noun =[' '.join([word[0] for word in words if word[1] in ('FW','NNS', 'NN', 'NNP', 'NNPS')]) for words in tagging_raw]
    X_noun =  tfv.fit_transform(tagging_noun)
    # tf-idf on adj&adv from nltk tagging
    tagging_adjv =[' '.join([word[0] for word in words if word[1] in ('JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS')]) for words in tagging_raw]
    X_adjv =  tfv.fit_transform(tagging_noun)

    # tf-idf on character level
    tfv = TfidfVectorizer(min_df=100, max_df = 0.1, strip_accents='ascii', analyzer='char', token_pattern=r'\w{1,}',ngram_range=(1, 4), use_idf=1, smooth_idf=1, sublinear_tf=1)
    X_origin_desc_char = tfv.fit_transform(origin_desc)

    return X_basic, X_location, X_state, X_duration, X_origin_desc, X_preprocessed, X_topic20, X_noun, X_adjv, X_origin_desc_char


if __name__ == '__main__':

    X_basic, X_location, X_state, X_duration, X_origin_desc, X_preprocessed, X_topic20, X_noun, X_adjv, X_origin_desc_char = main()

    # dense feature, used for advanced algorithms like GBM, random forest, etc.
    dense_feature1 = hstack([X_basic, X_topic20]).todense()
    # sparse features, used for linear algorithms like ridge regression, logistic regression, stochastic gredient descent, etc. 
    sparse_feature1 = hstack([X_basic, X_location, X_state, X_duration, X_origin_desc])
    sparse_feature2 = hstack([X_basic, X_location, X_state, X_duration, X_preprocessed])
    sparse_feature3 = hstack([X_basic, X_location, X_state, X_duration, X_noun])
    sparse_feature4 = hstack([X_basic, X_location, X_state, X_duration, X_adjv])
    sparse_feature5 = hstack([X_basic, X_location, X_state, X_duration, X_origin_desc_char])
    
    
    






                                                    
                
    

   
                 





