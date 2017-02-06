###############################################################################
#' Helper function used for SIT blog
#'
#' @param filename.pattern post files to process, \strong{defaults to '^\\d*-.*.r$'} 
#'
#' @param move.post flag to inidicate to move post to blog folder, \strong{defaults to FALSE} 
#' @param blog.folder blog folder
#' @param move.source.post flag to indicate to move source post to blog folder, \strong{defaults to FALSE} 
#'
#' @param compress.plots flag to inidicate that plots must be compressed, \strong{defaults to FALSE} 
#' @param pngout.location pngout location, \strong{defaults to 'c:/Library/exe/pngout.exe'} 
#'
#' @param clean.figure.folder flag to inidicate that figure folder must be cleaned, \strong{defaults to TRUE} 
#'
#' @param add.info2post.fn add custom info to the post function, \strong{defaults to add.SIT.info2post} 
#' @param add.date flag to indicate to include date when post was run, \strong{defaults to TRUE} 
#'
#' @param base.url blog base url, \strong{defaults to "/"} 
#' @param fig.width figure width, \strong{defaults to 9} 
#' @param fig.height figure height, \strong{defaults to 6} 
#' @param remove.UTF remove the non-ASCII characters, \strong{defaults to TRUE} 
#' @param render.fn knitr render function, \strong{defaults to render_jekyll} 
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
run.posts <- function
(
	# http://rubular.com/
	filename.pattern ='^\\d*-.*.r$',
	
	move.post = F,
	blog.folder = 'web',
	move.source.post = F,	
	
	compress.plots = F,
	pngout.location = 'c:/Library/exe/pngout.exe',
	
	clean.figure.folder = T,	
	
	add.info2post.fn = add.SIT.info2post,
	add.date = T,

	base.url = '/', 	
	fig.width=9, 
	fig.height=6,
	remove.UTF = T,
	render.fn = render_jekyll
)
{
	require(knitr)
	if( clean.figure.folder ) clean.figure.folder()
	
	filenames = list.files(pattern = filename.pattern, ignore.case = T)

	temp.filename = 'post.r'
	for(post.filename  in filenames) {
		if( is.null(add.info2post.fn) ||  is.na(add.info2post.fn) ) add.info2post.fn = function(f1, f2) file.copy(f1, f2)
		
		knit.post(post.filename, make.rmd(
			add.info2post.fn(post.filename, temp.filename, 
				add.source.post.link = move.source.post, add.date = add.date)
			),
			base.url=base.url, fig.width=fig.width, fig.height = fig.height,
			remove.UTF=remove.UTF, render.fn = render.fn)
		
		if( compress.plots ) compress.plots(post.filename, pngout.location=pngout.location)
		
		if(	move.post ) move.post(post.filename, blog.folder, move.source.post = move.source.post)		
	}
}

#' @export 
run.posts.html <- function
(
	# http://rubular.com/
	filename.pattern ='^\\d*-.*.r$',
	
	clean.figure.folder = T,
	
	add.info2post.fn = add.SIT.info2post,

	base.url = '', 	
	fig.width=9, 
	fig.height=6,
	remove.UTF = T,
	render.fn = render_html
)
{
	require(knitr)
	require(markdown)
	if( clean.figure.folder ) clean.figure.folder()
	
	filenames = list.files(pattern = filename.pattern, ignore.case = T)

	temp.filename = 'post.r'
	for(post.filename  in filenames) {
		if( is.null(add.info2post.fn) ||  is.na(add.info2post.fn) ) add.info2post.fn = function(f1, f2) file.copy(f1, f2)
		
		knit.post(post.filename, make.rmd(add.info2post.fn(post.filename, temp.filename)),
			base.url=base.url, fig.width=fig.width, fig.height = fig.height,
			remove.UTF=remove.UTF, render.fn = render.fn)
	}
	
	
	markdownToHTML(change.ext(post.filename,'.md'), change.ext(post.filename,'.html'),
		stylesheet = file.path(system.file('themes', package = 'SIT.blog') ,'prettymarkdown.css'))
}

