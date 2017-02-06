###############################################################################
# Common functions used internally
############################################################################### 
change.ext = function(filename, new.ext) sub('\\.R.*$', new.ext, filename, ignore.case=T)
len = function(x) length(x)
spl = function(s, delim = ',') unlist(strsplit(s,delim))

###############################################################################
#' Convert R script to Rmd file
#'
#' @param r.script.post.filename R script post filename
#' @param out.filename output Rmd filename, \strong{defaults to r.script.post.filename} 
#'
#' @return output Rmd filename
#'
#' @examples
#' \dontrun{ 
#' filename = 'post.test.r'
#' make.rmd(filename, 'post.r')
#' make.rmd(filename)
#' }
#'
#' @export 
############################################################################### 
make.rmd <- function
(
	r.script.post.filename,
	out.filename = r.script.post.filename
)
{
	if (out.filename != r.script.post.filename) {
		txt = readLines(r.script.post.filename)  
    	temp = file(out.filename,'w')
		writeLines(txt,con=temp)
		close(temp)		
	}
	spin(out.filename, knit =F)
}


###############################################################################
#' Generate figure path given post
#'
#' @param post.filename post filename
#' @param figure.folder figure folder, \strong{defaults to "public/images/"} 
#'
#' @return figure folder path for given post
#'
#' @examples
#' \dontrun{ 
#' filename = 'post.test.r'
#' make.rmd(filename, 'post.r')
#' make.rmd(filename)
#' }
#'
#' @export 
############################################################################### 
post.figure.path <- function
(
	post.filename,
	figure.folder = "public/images/"
)
{
	paste0(figure.folder, change.ext(basename(post.filename),""), "/")
}


###############################################################################
#' Generate Markdown file given RMarkdown post file
#'
#' @param post.filename RMarkdown post filename
#' @param temp.filename intermidiate RMarkdown post filename, \strong{defaults to post.filename} 
#' @param figure.folder figure folder, \strong{defaults to "public/images/"} 
#' @param fig.path figure folder, \strong{defaults to post.figure.path(post.filename)} 
#' @param base.url blog base url, \strong{defaults to "/"} 
#' @param default.img.filename prefix for images generated, \strong{defaults to "plot"} 
#' @param fig.width figure width, \strong{defaults to 9} 
#' @param fig.height figure height, \strong{defaults to 6} 
#' @param remove.UTF remove the non-ASCII characters, \strong{defaults to TRUE} 
#' @param render.fn knitr render function, \strong{defaults to render_jekyll} 
#'
#' @return figure folder path for given post
#'
#' @examples
#' \dontrun{ 
#' filename = 'post.test.r'
#' knit.post(filename)
#' }
#'
#' @export 
############################################################################### 
knit.post <- function(
	post.filename,
	temp.filename = post.filename,
	figure.folder = "public/images/", 
	fig.path = post.figure.path(post.filename, figure.folder),
	base.url = '/', 
	default.img.filename = 'plot',
	fig.width=9, 
	fig.height=6,
	remove.UTF = T,
	render.fn = render_jekyll
) 
{
	# remove the non-ASCII characters
	if(remove.UTF) {
		txt = readLines(temp.filename)  
		txt = iconv(txt, "latin1", "ASCII", sub="")	
    	temp = file(temp.filename,'w')
		writeLines(txt,con=temp)
		close(temp)		
	}
	
	# knitr settings
	opts_knit$set(unnamed.chunk.label = default.img.filename)    
    opts_knit$set(base.url = base.url)
    
	# set to asis, so that print -> cat works (i.e. there is no ## signs)
	opts_chunk$set(results = 'asis')
	opts_chunk$set(warning = F)
	opts_chunk$set(message = F)

    opts_chunk$set(fig.path = fig.path)
    #opts_chunk$set(fig.cap = "center")
    
	# http://auctionrepair.com/pixels.html
	#opts_chunk$set(fig.width=9, fig.height=6)
	opts_chunk$set(fig.width=fig.width, fig.height=fig.height)       
    
	# create figure folder
	dir.create(fig.path, recursive = T)

    # setup for github, jekyll
    render.fn()

    
    # use print function that supports Markdown tables   
    envir = parent.frame()
    	envir[['print']] = print
	knit(temp.filename, envir = envir)	
	file.rename(change.ext(temp.filename,'.md'),change.ext(basename(post.filename),'.md'))
}

# print function for markdown documents to
# properly format matrices and lists
# cat function output is directly printed
print = function(...) { 
	out = list( ... )

	# process result
	if ( length(out) == 1 )
		x = out[[1]]
	else
		x = paste( ... )
	
	# use kable for matrices
	if ( is.matrix(x) || is.data.frame(x) || is.xts(x) )
		x = kable(x)
	
	if ( is.vector(x) && !is.null(names(x)) )
		x = kable(t(as.matrix(x)))

		
	# mode(x), typeof(x)
	if(is.list(x))
		cat('\n', '<pre>', capture.output(x),  '</pre>','    \n\n', sep='\n')	
	else {
		# remove NAs
		x = sapply(x, function(x) gsub('NA','  ',gsub('NA%', '   ',x)),USE.NAMES=F)    	
		cat('\n', x, '    \n\n', sep='\n')
	}
}


###############################################################################
#' Clean figure folder
#'
#' @param fig.path figure folder, \strong{defaults to post.figure.path(post.filename)} 
#'
#' @return nothing
#'
#' @examples
#' \dontrun{ 
#' clean.figure.folder()
#' }
#'
#' @export 
############################################################################### 
clean.figure.folder <- function
(
	figure.folder = "public/images/"
)
{
	shell(paste('rd /s /q ', gsub('/','\\\\', figure.folder), sep=''), wait = TRUE)
}


###############################################################################
#' Compress plot(s)
#'
#' @param post.filename post filename
#' @param figure.folder figure folder, \strong{defaults to "public/images/"} 
#' @param fig.path figure folder, \strong{defaults to post.figure.path(post.filename)} 
#' @param pngout.location pngout location, \strong{defaults to 'c:/Library/exe/pngout.exe'} 
#'
#' @return nothing
#'
#' @examples
#' \dontrun{ 
#' compress.plots()
#' }
#'
#' @export 
############################################################################### 
compress.plots <- function
(
	post.filename,
	figure.folder = "public/images/", 
	fig.path = post.figure.path(post.filename, figure.folder),
	pngout.location = 'c:/Library/exe/pngout.exe'
)
{
	if(file.exists(pngout.location))
    	for(f in list.files(fig.path, '*.png')) {
    		f1 = file.path(fig.path,f)
    		system(paste(pngout.location, ' ', f1, ' ', f1, ' /s1 /y',sep=''), wait = TRUE)
    	}
}


###############################################################################
#' Move post markdown and figures to blog folder
#'
#' @param post.filename post filename
#' @param blog.folder blog folder
#' @param figure.folder figure folder, \strong{defaults to "public/images/"} 
#' @param fig.path figure folder, \strong{defaults to post.figure.path(post.filename)} 
#' @param move.source.post flag to indicate to move source post to blog folder, \strong{defaults to FALSE} 
#'
#' @return nothing
#'
#' @examples
#' \dontrun{ 
#' move.post()
#' }
#'
#' @export 
############################################################################### 
move.post <- function
(
	post.filename, 
	blog.folder,
	figure.folder = "public/images/", 
	fig.path = post.figure.path(post.filename, figure.folder),
	move.source.post = F
) 
{	
	blog.folder = gsub('/','\\\\', blog.folder)
		
	# copy post filename
	md.file = change.ext(post.filename, '.md') 
	shell(paste('xcopy /Y ', gsub('/','\\\\',md.file), ' ', blog.folder, '\\_posts\\*.*', sep=''), wait = TRUE)		
	
	if(move.source.post)
		shell(paste('xcopy /Y ', gsub('/','\\\\',post.filename), ' ', blog.folder, '\\rposts\\*.*', sep=''), wait = TRUE)
	
	# clean figure folder in blog folder
	fig.path = gsub('/','\\\\', fig.path)
	shell(paste('rd /s /q ', blog.folder, '\\', fig.path, '\\', sep=''), wait = TRUE)
	
	# copy figures
	shell(paste('xcopy /S /E /Y ', fig.path, '* ', blog.folder, '\\', fig.path, sep=''), wait = TRUE)
}


###############################################################################
#' Add info to the post. Custom version for SIT blog.
#'
#' @param post.filename R script post filename
#' @param out.filename output filename
#' @param fig.path figure folder, \strong{defaults to post.figure.path(post.filename)} 
#' @param add.source.post.link flag to indicate to include source post link, \strong{defaults to FALSE} 
#' @param add.date flag to indicate to include date when post was run, \strong{defaults to TRUE} 
#'
#' @return output filename
#'
#' @examples
#' \dontrun{ 
#' filename = 'post.test.r'
#' temp.filename = 'post.r'
#' make.rmd(add.SIT.info2post(filename, temp.filename))
#' }
#'
#' @export 
############################################################################### 
add.SIT.info2post <- function
(
	post.filename, 
	out.filename, 
	fig.path = post.figure.path(post.filename),
	add.source.post.link = F,
	add.date = T
) 
{
    # load file and locate header
    txt = readLines(post.filename)  
    
   	index = which(grepl('---',txt))[2]
   	
   	source.post.link.token = ''
	if(add.source.post.link) 
		source.post.link.token = paste(
			"#' For your convenience, the",
			paste0('[', change.ext(basename(post.filename),""), '](https://github.com/systematicinvestor/systematicinvestor.github.io/blob/master/rposts/', post.filename, ')'),
			"post source code."
		)
		
	date.token = ''
   	if(add.date) date.token = "#' *(this report was produced on: `r as.character(Sys.Date())`)*"
   	
   	# insert SIT info
   	txt = c(txt[1:index],
		"",
		"#' To install [Systematic Investor Toolbox (SIT)](https://github.com/systematicinvestor/SIT) please visit [About](/about) page.",
		"",
		
		"#+ results = 'hide', echo=F",
		"try(setInternet2(TRUE),T)",
		"#Load SIT",
		"try(detach('package:SIT', unload = T),T)",
		"library(SIT)",
		
		"#Load post functions to be moved to SIT",
		# loading with source, please use local = T, so that print function defined in SIT.blog is used
		"if(file.exists('post.fn.r')) source('post.fn.r',T)",
		"if(file.exists('../ds.r')) source('../ds.r',T)",
		"",

		"#Assign folder where images will be stored",
		paste0("IMG.POST.FOLDER = '",fig.path,"'"),
		paste0("POST.FILENAME = '",spl(basename(post.filename),'\\.')[1],"'"),
		
		txt[-c(1:index)],
		"",
		"",
		source.post.link.token,
		"",
		"#' ",
		date.token
	)
		
    temp = file(out.filename,'w')
	writeLines(txt,con=temp)
	close(temp)
	out.filename
}


#' @export 
add.SIT.info2postRmd <- function
(
	post.filename, 
	out.filename, 
	fig.path = post.figure.path(post.filename)
) 
{
    # load file and locate header
    txt = readLines(post.filename)  
    
   	index = which(grepl('---',txt))[2]
   	
   	# insert SIT info
   	txt = c(txt[1:index],
		"",
		"To install [Systematic Investor Toolbox (SIT)](https://github.com/systematicinvestor/SIT) please visit [About](/about) page.",
		"",
		
		"```{r, results = 'hide', echo=F}",
		"try(setInternet2(TRUE),T)",
		"#Load SIT",
		"try(detach('package:SIT', unload = T),T)",		
		"library(SIT)",
		"#Load post functions to be moved to SIT",
		"if(file.exists('post.fn.r')) source('post.fn.r',T)",
		"if(file.exists('../ds.r')) source('../ds.r',T)",
		"",

		"#Assign folder where images will be stored",
		paste0("IMG.POST.FOLDER = '",fig.path,"'"),
		paste0("POST.FILENAME = '",spl(basename(post.filename),'\\.')[1],"'"),
		
		"```",		
		txt[-c(1:index)],
		"",
		"*(this report was produced on: `r as.character(Sys.Date())`)*"
	)
	
    temp = file(out.filename,'w')
	writeLines(txt,con=temp)
	close(temp)
	out.filename
}

