---
layout: post
title: SIT.blog - Helper functions to automate Blog post generation
comments: true
---


To install [Systematic Investor Toolbox (SIT)](https://github.com/systematicinvestor/SIT) please visit [About](/about) page.


SIT.blog package is the collection of functions to ease / automate Blog post generation.

{% highlight r %}
library(knitr)
library(markdown)
library(SIT.blog)

# genearte html
run.posts.html('2016-02-28-Post.r')


# genearte markdown post suitable for posting on GitHub pages
run.posts('2016-02-28-Post.r')


# process all post(s) that start with number(s)- and end with r
run.posts('^\\d*-.*.r$')

{% endhighlight %}



General Notes:
-----

* If you loading code that will use print statement, please use local = T
i.e. source('code.r',T)
this way the print function defined in SIT.blog will be used

* I used a modified theme from [JasonM23](https://github.com/jasonm23/markdown-css-themes)


Notes on writting post in R file with Rmarkdown synatx
----

* [Knitr's best hidden gem: spin](http://deanattali.com/2015/03/24/knitrs-best-hidden-gem-spin/)

* [Quick reporting Build a report based on an R script](http://yihui.name/knitr/demo/stitch/)
  + [knitr-spin.R source R file with Rmarkdown formating](https://raw.githubusercontent.com/yihui/knitr/master/inst/examples/knitr-spin.R)
  +	[knitr-spin.Rmd resulting Rmarkdown file](https://raw.githubusercontent.com/yihui/knitr/master/inst/examples/knitr-spin.Rmd)

* [Simple Markdown syntax for formatting your R scripts into WEB pages using knitr::spin()](https://rpubs.com/alobo/spintutorial)
	the chunk name is not required, for example
{% highlight r %}
#+ eval=FALSE
{% endhighlight %}

* [How to produce a report with spin() knitr AND save some plot in a pdf](http://stackoverflow.com/questions/17835366/how-to-produce-a-report-with-spin-knitr-and-save-some-plot-in-a-pdf)

* [Reproducible documents with R & knitr](http://muuankarski.github.io/luntti/toistettava/dynamic_docs.html)
