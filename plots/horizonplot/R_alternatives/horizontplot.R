#first attempt at implementing horizon plots in ggplot2
#pleased with result but code sloppy and inflexible
#as always very open to improvements and forks

require(ggplot2)
require(reshape2)
require(quantmod)
require(PerformanceAnalytics)
require(xtsExtra)

data(edhec)
origin = 0
horizonscale = 0.1
#get 12 month rolling return of edhec indexes
roc <- as.xts(apply(cumprod(edhec+1),MARGIN=2,ROC,n=12,type="discrete"),order.by=index(edhec))

roc.df <- as.data.frame(cbind(index(roc),coredata(roc)))
roc.melt <- melt(roc.df,id.vars=1)
roc.melt[,1] <- as.Date(roc.melt[,1])  #convert back to a Date


horizon.panel.ggplot <- function(df, title) {
  #df parameter should be in form of date (x), grouping, and a value (y)
  colnames(df) <- c("date","grouping","y")
  #get some decent colors from RColorBrewer
  #we will use colors on the edges so 2:4 for red and 7:9 for blue
  require(RColorBrewer)
  col.brew <- brewer.pal(name="RdBu",n=10)
  
  #get number of bands for the loop
  #limit to 3 so it will be much more manageable
  nbands = 3
  
  #loop through nbands to add a column for each of the positive and negative bands
  for (i in 1:nbands) {
    #do positive
    df[,paste("ypos",i,sep="")] <- ifelse(df$y > origin,
                                          ifelse(abs(df$y) > horizonscale * i,
                                                 horizonscale,
                                                 ifelse(abs(df$y) - (horizonscale * (i - 1) - origin) > origin, abs(df$y) - (horizonscale * (i - 1) - origin), origin)),
                                          origin)
    #do negative
    df[,paste("yneg",i,sep="")] <- ifelse(df$y < origin,
                                          ifelse(abs(df$y) > horizonscale * i,
                                                 horizonscale,
                                                 ifelse(abs(df$y) - (horizonscale * (i - 1) - origin) > origin, abs(df$y) - (horizonscale * (i - 1) - origin), origin)),
                                          origin)
  }
  #melt data frame now that we have added a column for each band
  #this will fit ggplot2 expectations and make it much easier
  df.melt <- melt(df[,c(1:2,4:9)],id.vars=1:2)    
  #name the columns for reference
  #try to be generic
  colnames(df.melt) <- c("date","grouping","band","value")
  
  #use ggplot to produce an area plot
  p <- ggplot(data=df.melt) +
    geom_area(aes(x = date, y = value, fill=band),
              #alpha=0.25,
              position="identity") +  #this means not stacked
    scale_fill_manual(values=c("ypos1"=col.brew[7],  #assign the colors to each of the bands; colors get darker as values increase
                               "ypos2"=col.brew[8],
                               "ypos3"=col.brew[9],
                               "yneg1"=col.brew[4],
                               "yneg2"=col.brew[3],
                               "yneg3"=col.brew[2])) +
    ylim(origin,horizonscale) +   #limit plot to origin and horizonscale
    facet_grid(grouping ~ .) +    #do new subplot for each group
    theme_bw() +                  #this is optional, but I prefer to default
    opts(legend.position = "none",    #remove legend
         strip.text.y = theme_text(),#rotate strip text to horizontal 
         axis.text.y = theme_blank(),#remove y axis labels
         axis.ticks = theme_blank(), #remove tick marks
         axis.title.y = theme_blank(),#remove title for the y axis
         axis.title.x = theme_blank(),#remove title for the x axis
         title = title,               #add a title from function parameter
         plot.title = theme_text(size=16, face="bold", hjust=0)) #format title
  
  return(p)
}



horizon.panel.ggplot(roc.melt, "EDHEC Indexes Return (Rolling 1 Year)")
