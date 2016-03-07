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
mycorpus <- tm_map(mycorpus, tolower, content_transformer(tolower))
mycorpus <- tm_map(mycorpus, removeWords, stopwords("english"))
mycorpus <- tm_map(mycorpus, removePunctuation)
mycorpus <- tm_map(mycorpus, removeNumbers)
# mycorpus <- tm_map(mycorpus, removeWords, custom_stop_words)
mycorpus <- tm_map(mycorpus, stemDocument)
  
dtm0 <- DocumentTermMatrix(mycorpus)

# TrigramTokenizer <- function (x) NGramTokenizer(x, Weka_control(min=1,max=3))
# BigramTokenizer <- function (x) NGramTokenizer(x, Weka_control(min=1,max=2))


dim(dtm0)
inspect(dtm0[1:5,1:10])
findFreqTerms(dtm0, 1000) #terms that occur at least 100 times


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


> rank_or[5:20]
[1] "stung"        "federal"      "alleged"      "lung"         "black"        "state"       
[7] "insect"       "glasses"      "foreign"      "nail"         "occupational" "irritation"  
[13] "trauma"       "hearing"      "eyes"         "cumulative"  



rank[,1] = sapply(1:length(dtm$dimnames[[2]]),
                              function(x) aor(df$IN_SUIT=="Y",x))


chisq[,2] = sapply(1:length(dtm$dimnames[[2]]),
                   function(x) chisq.test(df$adjusted_net0x)$statistic)



### Create document term matric
dtm$dimnames[[2]]
term_claim_summary <- matrix(0,nrow=ncol(dtm),ncol=4)
rownames(term_claim_summary) <- dtm$dimnames[[2]]
colnames(term_claim_summary) <- c("Total Net Amount","Number of Claims","Average Claim Size","Number Claims in Top 5%")

n <- floor(nrow(claims)/20)
offset <- ncol(claims)
term_claim_summary[,1] <- sapply(1:length(dtm$dimnames[[2]]),fun <- function(x) sum(claims$net_amt[dtm_claims[,x+offset]>0]))
term_claim_summary[,2] <- sapply(1:length(dtm$dimnames[[2]]),fun <- function(x) sum(dtm_claims[,x+offset]>0))
term_claim_summary[,3] <- sapply(1:length(dtm$dimnames[[2]]),fun <- function(x) mean(claims$net_amt[dtm_claims[,x+offset]>0]))
term_claim_summary[,4] <- sapply(1:length(dtm$dimnames[[2]]),fun <- function(x) sum(dtm_claims[1:n,x+offset]>0))
term_claim_summary[order(term_claim_summary[,3],decreasing=TRUE),]

term_claim_summary <- data.frame(term_claim_summary)
term_claim_summary$Rel_freq_top_5 <- term_claim_summary[,4]*nrow(claims)/(term_claim_summary[,2]*n)
term_claim_summary <- term_claim_summary[order(term_claim_summary[,3],decreasing=TRUE),]

#### Create chart with high average cost words that are meaningful - unclear what else to do

term_claim_summary <- term_claim_summary[order(term_claim_summary[,2],decreasing=TRUE),]
term_claim_summary[1:20,]


### Find relevant terms and output subsets of top key words and phrases
term_claim_summary <- term_claim_summary[order(term_claim_summary[,3],decreasing=TRUE),]
term_claim_summary[c(1,12,15,16,18,19,24,26,34,36,45,52,53,55,59,60),]
# 1,12,15,16,18,19,24,26,34,36,45,52,53,55,59,60 ## These are more interesting than the number of claims stories - slide 1 show these with number and average and example
# back v spine/disc; shoulder v rotator/cuff; drill - 3x as likely to be top 5 - what's happening to prevent - and need to monitor; highway/shipyard/airframe; arthritis - find out what's going on
#also investigate "prior"  oculd be prior claim, prioir injury, prior surgery
write.csv(term_claim_summary[c(1,12,15,16,18,19,24,26,34,36,45,52,53,55,59,60),],file="ng_adj_some_high_cost_terms_09_to_14.csv")

term_claim_summary <- term_claim_summary[order(term_claim_summary[,2],decreasing=TRUE),]
write.csv(term_claim_summary,file="ng_adj_notes_frequent_terms_081614.csv")



### Pick a relevant term and drill down into details - export to .csv file
claims.subset <-claims[(dtm_claims$rehabilit>0),]
search.text <- "rehabilit"
string.length <- 200
output.file <- "test_data.csv"

claims.subset <- claims.subset[order(claims.subset$net_amt,decreasing=TRUE),]
output.size <- nrow(claims.subset)
output.sheet <- data.frame(claims.subset$net_amt[1:output.size],notes="notes",stringsAsFactors = FALSE)
for (i in 1:output.size) {
  print(output.sheet$notes[i] <- substr(claims.subset$text[i],regexpr(search.text,claims.subset$text[i],ignore.case=TRUE)[[1]]-string.length/2,regexpr(search.text,claims.subset$text[i],ignore.case=TRUE)[[1]]+string.length/2))
}
write.csv(output.sheet,file=output.file)



















ds=DataframeSource(data.frame(df$tx))


  
  
tdm <- lapply(candidates, generateTDM, path = pathname)
tdm=generateTDM

# Bind Candidate Name to Term Document Matrices
bindCandidateToTDM <- function(tdm) {
  s.mat <- t(data.matrix(tdm[["tdm"]]))
  s.df <- as.data.frame(s.mat, stringsAsfactors = FALSE)
  s.df <- cbind(s.df, rep(tdm[["name"]], nrow(s.df)))
  colnames(s.df)[ncol(s.df)] <- "targetcandidate"
  return(s.df)
}

# Append Candidate Field to TDM
candTDM <- lapply(tdm, bindCandidateToTDM)

# Rbind Candidate TDMs
tdm.stack <- do.call(rbind.fill, candTDM)
tdm.stack[is.na(tdm.stack)] <- 0

# Random sample 70% for training of data mining model; remainder for test
train.idx <- sample(nrow(tdm.stack), ceiling(nrow(tdm.stack) * .70))
test.idx <- (1:nrow(tdm.stack))[- train.idx]

# Extract candidate name
tdm.cand <- tdm.stack[, "targetcandidate"]
tdm.stack.nl <- tdm.stack[,!colnames(tdm.stack) %in% "targetcandidate"]

# K-nearest Neighbor
knn.pred <- knn(tdm.stack.nl[train.idx, ], tdm.stack.nl[test.idx, ], tdm.cand[train.idx])
knn.train.data <- tdm.stack[train.idx, ]

# Confusion Matrix
conf.mat <- table("Predictions" = knn.pred, Actual = tdm.cand[test.idx])

# Accuracy
(accuracy <- sum(diag(conf.mat))/length(test.idx) * 100)

################################################################################

# Function to generate corpus where each paragraph is
# set as a document.
generateParagraphDocCorpus <- function(cand, path) {
  
  # Set directory and list files
  s.dir <- sprintf("%s/%s", path, cand)
  filelist <- list.files(s.dir, full.names = TRUE)
  
  # Read each paragraph and append to vector
  speech.v <- unlist(sapply(filelist, function(x) {
    speech.tmp <- readLines(x)
    speech.tmp <- speech.tmp[speech.tmp != ""]
    return(speech.tmp)
  }))
  
  # Instantiate Corpus
  s.cor <- Corpus(VectorSource(speech.v, encoding = "ANSI"))
  
  return(s.cor)
}

# Function to generate corpus from a single file
generateSpeechDocCorpus <- function(filepath) {
  
  # Read data from file
  vec <- scan(filepath, what = "", quiet = TRUE)
  
  # Collapse word vector
  vec <- paste(vec, collapse = " ")
  
  # Instantiate Corpus
  s.cor <- Corpus(VectorSource(vec, encoding = "ANSI"))
  
  return(s.cor)
}    

################################################################################

# Create Dendrograms of Policy Topics
generateDendrogram <- function(tdm, sparcity = 0.2) {
  tdm.sub <- removeSparseTerms(tdm, sparcity)
  euc.dist <- dist(tdm.sub, method = "euclidean")
  dendro <- hclust(euc.dist, method = "ward")
  plot(dendro)
}

# Generate Concept Dendrograms
generateDendrogram(tdm[[1]][[2]], 0.2)
generateDendrogram(tdm[[2]][[2]], 0.3)

# Find Concept Associations
findAssocs(tdm[[1]][[2]], 'economy', 0.50)
findAssocs(tdm[[2]][[2]], 'economy', 0.50)

findAssocs(tdm[[1]][[2]], 'energy', 0.40)
findAssocs(tdm[[2]][[2]], 'energy', 0.40)

findAssocs(tdm[[1]][[2]], 'health', 0.55)
findAssocs(tdm[[2]][[2]], 'health', 0.55)

findAssocs(tdm[[1]][[2]], 'military', 0.60)
findAssocs(tdm[[2]][[2]], 'military', 0.60)