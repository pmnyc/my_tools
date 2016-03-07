require(twitteR)
require(wordcloud)
require(igraph)
require(tm)
require(SnowballC)

#searchTwitter("3G services", n=100,cainfo="cacert.pem")
# Download my binary file from the public DropBox folder

load("GSElevatorTweets.RData")
(nDocs <- length(rdmTweets))
df <- do.call("rbind", lapply(rdmTweets, as.data.frame))
dim(df)




#build a corpus, and specify the source to be character vectors
myCorpus <- Corpus(VectorSource(df$text))

# transform text using tm packages
# convert to lower case
myCorpus <- tm_map(myCorpus, tolower)
# remove punctuation
myCorpus <- tm_map(myCorpus, removePunctuation)
# remove numbers
myCorpus <- tm_map(myCorpus, removeNumbers)
# remove URLs
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
myCorpus <- tm_map(myCorpus, removeURL)
# add two extra stop words: "available" and "via"
myStopwords <- c(stopwords('english'), stopwords('portuguese'))
# remove "r" and "big" from stopwords
#idx <- which(myStopwords %in% c("r", "big"))
#myStopwords <- myStopwords[-idx]
# remove stopwords from corpus
myCorpus <- tm_map(myCorpus, removeWords, myStopwords)

# keep a copy of corpus to use later as a dictionary for stem completion
myCorpusCopy <- myCorpus
# stem words
myCorpus <- tm_map(myCorpus, stemDocument)
# stem completion
myCorpus <- tm_map(myCorpus, stemCompletion, dictionary=myCorpusCopy)
myTdm <- TermDocumentMatrix(myCorpus, control = list(wordLengths=c(1,Inf)))

findFreqTerms(myTdm, lowfreq=10)
termFrequency <- rowSums(as.matrix(myTdm))
termFrequency <- subset(termFrequency, termFrequency>=10)


#Find all terms co-occuring with the term 'solar'
#findAssocs(myTdm, 'solar', 0.25)

# Convert TermDocumentMatrix to a matrix
m <- as.matrix(myTdm)
# Construct a denser matrix with just the most frequent terms
m.sub <- subset(m, rowSums(m)>=3)

dev.new()
# calculate the frequency of words and sort it descending by frequency
wordFreq <- sort(rowSums(m.sub), decreasing=TRUE)
# word cloud
set.seed(375) # to make it reproducible
grayLevels <- gray( (wordFreq+10) / (max(wordFreq)+10) )
# plot the word cloud
wordcloud(words=names(wordFreq), freq=wordFreq, min.freq=3, random.order=F, colors=grayLevels)



