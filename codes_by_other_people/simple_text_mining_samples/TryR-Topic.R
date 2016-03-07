#########################################################################
# Copyright (c) 2012 All Rights Reserved, http://www.bostondecision.com
#
# This source is free to use and distribute so long as credit is provided.
# This code is provided "AS IS" without warranty of any kind, either
# expressed or implied, including but not limited to the implied
# warranties of merchantability and/or fitness for a particular purpose.
#
# Author: Timothy D'Auria
# Email: tdauria [at] bostondecision [dot] com
# Date: 5/14/2012
#
# TITLE: THE R TEXT CLASSIFIER - Brand Management, Plagiarism Detection
#
# Purpose: R tools to predict the author of a text document or url
# Uses a simple K-nearest Neighbor algorithm.
#
# Setup: Set pathname to a directory that contains 1 subdirectory
# for each candidate/author.  Each candidate subdirectory contains 1 or
# more speeches saved as .txt files.
# Set candidates to the names of the candidate subdirectories
#
#########################################################################

# Load libraries
library(tm)
library(wordcloud)
library(kernlab)
library(plyr)
library(class)
require(dplyr)
library(topicmodels)
# library(wordnet) 
# library(RWeka)
# library(Snowball)

# Set options
options(stringsAsFactors = FALSE)

# Set parameters
# candidates <- c("romney", "obama")
pathname <- "H:/TextMining/ZhaoXingExamples"

# Function to convert pretty apostrophe
convertPrettyApostrophe <- function(x) gsub("'", "'", x)

# Function to clean Corpus text
cleanCorpus <- function(corpus) {
  
  # Apply Text Mining Clean-up Functions
  corpus.tmp <- tm_map(corpus, convertPrettyApostrophe)
  corpus.tmp <- tm_map(corpus.tmp, removePunctuation)
  corpus.tmp <- tm_map(corpus.tmp, stripWhitespace)
  corpus.tmp <- tm_map(corpus.tmp, tolower)
  corpus.tmp <- tm_map(corpus.tmp, removeWords, stopwords("english"))
  # corpus.tmp <- tm_map(corpus.tmp, stemDocument, language = "english")
  
  return(corpus.tmp)
}

# Function to generate term document matrices
generateTDM <- function(cand, path) {
  # Set directory
  s.dir <- sprintf("%s/%s", path, cand)
  
  # Instantiate Corpus
  s.cor <- Corpus(DirSource(directory = s.dir, encoding = "ANSI"))
  
  # Clean corpus
  s.cor.cl <- cleanCorpus(s.cor)
  
  # Create term document matrix
  s.tdm <- TermDocumentMatrix(s.cor.cl)
  
  # Remove sparse terms
  s.tdm <- removeSparseTerms(s.tdm, 0.7)
  
  # Construct return object
  result <- list(name = cand, tdm = s.tdm)
  
  return(result)
}

# Run term document matrix function on all candidates
df=read.csv("H:/TextMining/ZhaoXingExamples/tm.csv")

df$tx=paste(df$LOSS_DESC_1,df$LOSS_DESC_2, sep='')
mycorpus <- Corpus(VectorSource(df$tx))
# mycorpus <- Corpus(DataframeSource(df$tx))
mycorpus <- tm_map(mycorpus, stripWhitespace)
mycorpus <- tm_map(mycorpus,  content_transformer(tolower))
mycorpus <- tm_map(mycorpus, removeWords, stopwords("english"))
mycorpus <- tm_map(mycorpus, removePunctuation)
mycorpus <- tm_map(mycorpus, removeNumbers)
# mycorpus <- tm_map(mycorpus, removeWords, custom_stop_words)
mycorpus <- tm_map(mycorpus, stemDocument)
  
dtm0 <- DocumentTermMatrix(mycorpus)

# TrigramTokenizer <- function (x) NGramTokenizer(x, Weka_control(min=1,max=3))
# BigramTokenizer <- function (x) NGramTokenizer(x, Weka_control(min=1,max=2))


dim(dtm0)
# inspect(dtm0[1:5,1:10])
# findFreqTerms(dtm0, 1000) #terms that occur at least 100 times


### Remove terms that show up in few documents.  You may need to adjust the coefficent downwards if m can't be created
dtm <- removeSparseTerms(dtm0, 0.999)
dim(dtm)
# inspect(dtm)
m <- as.matrix(dtm)
m <- m>0 #depending on analysis, knowing if the word exists in the document at all may be all you need

### Inspect common terms
# v <- sort(colSums(m), decreasing=TRUE)
# v <- v/nrow(claims)
# head(v, 50)
# v[51:100]


data <- data.frame(cbind(df$IN_SUIT,df$adjusted_net,m))
data[1:5,1:10]

df$adjusted_net0=df$adjusted_net
df$adjusted_net0[df$adjusted_net<0]=0

aor=function (x,y) {
  x=as.vector(x)
  y=as.vector(y)
  n00=sum(x==0 & y==0)
  n11=sum(x==1 & y==1)
  n01=sum(x==0 & y==1)
  n10=sum(x==1 & y==0)
  or= (n00 * n11)/(n01 * n10)
  if (or<1) or=1/or
  return(or)
}

aor(df$IN_SUIT=="Y",dtm[,1]==1)

rank=matrix(0,nrow=ncol(dtm),ncol=2)
rank[,1]=apply(dtm,2,function(x) aor(df$IN_SUIT=="Y",x==1))
rank_or <- dtm$dimnames[[2]] [order(rank[,1],decreasing=TRUE)] 
rank[,1] [order(rank[,1],decreasing=TRUE)][1:10]
rank_or[1:20]


# > rank_or[5:20]
# [1] "stung"        "federal"      "alleged"      "lung"         "black"        "state"       
# [7] "insect"       "glasses"      "foreign"      "nail"         "occupational" "irritation"  
# [13] "trauma"       "hearing"      "eyes"         "cumulative"  




# Beware: this step takes a lot of patience!  My computer was chugging along for probably 10 or so minutes before it completed the LDA here.
k=20 #number of topics
dtm2=dtm[apply(dtm,1,sum)>0,]
dim(dtm)
dim(dtm2)
lda.model = LDA(dtm2, k)

# This enables you to examine the words that make up each topic that was calculated.  Bear in mind that I've chosen to stem all words possible in this corpus, so some of the words output will look a little weird.

terms(lda.model,10)


# Topic 1   Topic 2   Topic 3   Topic 4   Topic 5  
# [1,] "emp"     "back"    "left"    "emp"     "employe"
# [2,] "right"   "employe" "back"    "hit"     "lift"   
# [3,] "fell"    "finger"  "caus"    "right"   "emp"    
# [4,] "left"    "fell"    "hit"     "fell"    "struck" 
# [5,] "employe" "pain"    "employe" "employe" "slip"   
# [6,] "caus"    "caus"    "pain"    "cut"     "lower"  
# [7,] "pain"    "slip"    "ankl"    "hand"    "right"  
# [8,] "slip"    "pipe"    "eye"     "pull"    "pipe"   
# [9,] "step"    "pull"    "fell"    "caus"    "caus"   
# [10,] "knee"    "caught"  "strain"  "back"    "twist" 

# Here I construct a dataframe that scores each document according to how closely its content 

# matches up with each topic.  The closer the score is to 0, the more likely its content matches

# up with a particular topic. 

topics = posterior(lda.model, dtm)$topics

df.topics = as.data.frame(emails.topics)

df.topics = cbind(email=as.character(rownames(df.emails.topics)), 
                            
df.topics, stringsAsFactors=F)



