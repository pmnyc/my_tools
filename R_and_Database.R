#  R & PostgreSQL
library(RPostgreSQL);
con <- dbConnect(PostgreSQL(), host="NATABCD054", user= "postgres", password="mypassword", dbname="MyDB");
rs <- dbSendQuery(con, "SELECT * FROM data.mytable");
df <- fetch(rs, n=-1); #n=-1 fetches all rows, n=100 fetches first 100 rows
write.csv(df, file = "df.csv", row.names=FALSE, na="");
dbDisconnect(con);

##############################
#  R & Microsoft SQL Server
library(RODBC);
myconn <- odbcConnect('MyDB', uid='Myuser', pwd=''),
df <- sqlQuery(myconn,"select * from dbo.mytable");

##############################
#  R & Text Files
dir.create(file.path('c:/temp','new_folder'), showWarnings = TRUE); #create folder if it doesn't exist
write('abc',file='c:/temp/new_folder/a.txt',append=TRUE); #create file
myfile <- paste('c:/temp/new_folder/',"a.txt",sep="");
fileConn <- file(myTimelogfile);
writeLines('what is up',fileConn,sep="\n"); #add lines to text file
close(fileConn);