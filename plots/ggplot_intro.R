###################################################################################""
# PLOTTING IN R -> THE 10 STEPS TO GGPLOT!
###################################################################################""
#
#Stijn Van Hoey
#
#
# thanks to http://chrisladroue.com/extra/ggplot2Intro/introductionGGplot2/
# and other internet sources...
###################################################################################""

setwd(dir='/media/DATA/Githubs/bw10/visualisation/testing_libraries')

#A priori, get some data and make some a factor
senicData = read.table("./senic.dat", header = T, sep = "")
senicData$region <- as.factor(senicData$region)
senicData$school <- as.factor(senicData$school)

#---------------------------------------------------------------------------
# 1. Default plotting is easy and available for a lot of functions, eg. lm
#---------------------------------------------------------------------------
model1 <- lm(senicData$stay ~ senicData$age)
plot(model1)

#-> graphics package (core R)

# plot of the fit
plot(x = senicData$age , y = senicData$stay)
lines(lowess(senicData$stay ~ senicData$age), lwd = 2, col = "red")
abline(lsfit(senicData$age , senicData$stay), lwd=2, col = 4)

#---------------------------------------------------------------------------
# 2. However, ggplot brings something 'sleek' stuff
#---------------------------------------------------------------------------
library("ggplot2")
qplot(senicData$age, senicData$stay) + 
  geom_smooth(method="lm",se=FALSE) +
  geom_smooth(method="loess", color="red", se=FALSE)

#---------------------------------------------------------------------------
# 3. Uhm, I heard of "lattice" package?!?
#---------------------------------------------------------------------------
library("lattice")
xyplot(stay~age, senicData,
       grid = TRUE,
       type = c("p", "r", "smooth"), 
       auto.key=list(lines=TRUE), lwd = 3,
       col.line = "grey")

#pfff... same color.. not quick enough understandable solution found;
xyplot(stay~age, senicData,# subset=-12,
       panel = function(x, y) {
         panel.grid(h = -1, v = 2) # -1 align horiz grid to ticks, 2 indicates 2 vertical lines
         panel.xyplot(x, y, col='black')
         panel.loess(x, y, span=0.5, col='red')  # Span is the loess smoothness parameter, default 2/3 
         panel.lmline(x, y, col='blue')  # Adds a least squares line 
       } )
#looks like nested-mathematica-stuff?!??

#---------------------------------------------------------------------------
# 4. doing + for putting something extra is more intuitive -> ggplot2!
#---------------------------------------------------------------------------
qplot(senicData$age, senicData$stay) + 
  geom_smooth(, method="lm", se=FALSE) +
  geom_smooth(, method="loess", se=FALSE, col = "red") +
  xlab("Age of patient (years)") + 
  ylab("Duration of stay (days)") +
  ggtitle("Duration in function of age")

#...except of legends; however you have to get the aes-idea (just in a minute!)
qplot(senicData$age, senicData$stay) + 
  geom_smooth(aes(colour="linear fit"), method="lm", se=FALSE) +
  geom_smooth(aes(colour="loess fit"), method="loess", se=FALSE) +
  xlab("Age of patient (years)") + 
  ylab("Duration of stay (days)") +
  ggtitle("Duration in function of age") +
  scale_colour_discrete("")

#http://www.noamross.net/blog/2012/10/5/ggplot-introduction.html

#---------------------------------------------------------------------------
# 5. #REMEMBER : Lattice is great in multivariate plotting options!
#---------------------------------------------------------------------------
xyplot(stay~age | region, senicData,
       group = region,
       grid = TRUE,  type = c("p", "smooth"))
#or regression
xyplot(stay~age | region, senicData,
       group = region,
       grid = TRUE,  type = c("p", "r"))
xyplot(stay~age, senicData,
       grid = TRUE,
       group = region, auto.key = list(columns = nlevels(senicData$region)),
       type = c("p", "smooth"), lwd = 3)

#---------------------------------------------------------------------------
# 5. However, ggplot can do that too!
#---------------------------------------------------------------------------
ggplot(senicData, aes(x = age, y = stay, shape = region, color = beds)) + geom_point(size = 5)

# 2 FACTORS CREATED... split it:
ggplot(senicData, aes(x = age, y = stay)) + 
  geom_point(size = 2) +
  geom_smooth(method="lm") +
  facet_grid(~region)
             

ggplot(senicData, aes(x = age, y = stay)) + 
         geom_point(size = 2) +
         facet_grid(region~school)

# 2 FACTORS CREATED... regressions, just +...
ggplot(senicData, aes(x = age, y = stay)) + 
  geom_point(size = 2) +
  facet_grid(~region) +
  stat_smooth(method = "lm", se = TRUE) +
  scale_y_log10() +
  theme_bw()

#---------------------------------------------------------------------------
# 6. you just used qplot and ggplot...?!? -> OK, some theory!
#---------------------------------------------------------------------------

# The basic concept of a ggplot2 graphic in R is that you combine different elements into layers. 

# qplot vs ggplot => qplot is 'quick-plot'; ggplot more generic
# run: ggplot(senicData, aes(x = age, y = stay)) 
#=> no layers... points need to be added as layer (geom_point)
#and:
qplot(age, data=senicData, geom="histogram")
#vs
ggplot(data=senicData) + geom_histogram(aes(x=age))

#checking ggplot command, we see:

# DATA
#   * The data that you want to plot: For ggplot(), this must be a data frame; eg senicData
#   * A mapping from the data to your plot: This usually is as simple as telling ggplot() 
#     what goes on the x-axis and what goes on the y-axis; eg aes(x = age, y = stay);
#     this can be added to the ggplot-object, but also to a specific layer
# LAYERS
#   * A geometric object, or geom in ggplot terminology: The geom defines the overall look of 
#     the layer (for example, whether the plot is made up of bars, points, or lines); eg geom_point
#   * A statistical summary, called a stat in ggplot: This describes how you want the data to be 
#     summarized (for example, binning for histograms, or smoothing to draw regression lines); stat_smooth
# => if data and aes() in ggplot object, geom_XXX just referring to this data and aes; but can also be specified in layer!
# FACETS
#   * facet_grid
#   * facet_wrap
# SCALES
#   * eg. scale_y_log10()
# THEMES
#   * color scheme to use (white, theme_bw() , or grey, theme_grey(), or...)
# OTHER OPTIONS
#   * eg xlab("..."), ggtitle("..")

#---------------------------------------------------------------------------
# 7. Some initial learning curve details
#---------------------------------------------------------------------------
# A. aesthetics etc... 
#-----------------------
#assigning <> setting!! => check following difference
ggplot(data=senicData) + geom_density(aes(x=age, color=school))
ggplot(data=senicData) + geom_density(aes(x=age), color="blue")
#NOT: ggplot(data=senicData) + geom_density(aes(x=age, color="blue")) #not finding factor blue, so just putting 1 ref to blue in legend!

# so, too wrap up,  different levels to use factors (view into multivariate variables):
# 1. color within an aes
# 2. shape witint aes
# 2. size witint aes
# 4. facet_XXX
#eg.
ggplot(senicData, aes(x = age, y = stay, shape = region, color = beds, size = nurses)) + 
  geom_point() +
  facet_wrap(~school)
#I'm not saying it makes things more clear...
#...maybe this is already better:
ggplot(senicData, aes(x = age, y = stay, color = beds, size = nurses)) + 
  geom_point() +
  facet_grid(region~school) +
  theme_bw()

# B. scale options !!
#-----------------------
#Following two plots are not at all the same outcome
qplot(senicData$age, model1$res^2) + 
  geom_smooth(method="lm", se=FALSE) +
  geom_smooth(method="loess",  color="red", se=FALSE) +
  coord_cartesian(ylim=c(0, 10))
qplot(senicData$age, model1$res^2, ylim=c(0, 10)) + 
  geom_smooth(method="lm", se=FALSE) +
  geom_smooth(method="loess",  color="red", se=FALSE)
#The second one is partly neglecting the data... luckily R/ggplot warns us for this!

# C. No direct function for qqnorm with line
#----------------------------------------------
#custom function to work on output of linear model:
ggQQ.lm <- function(LM) # argument: a linear model
{
  y <- quantile(LM$resid[!is.na(LM$resid)], c(0.25, 0.75))
  x <- qnorm(c(0.25, 0.75))
  slope <- diff(y)/diff(x)
  int <- y[1L] - slope * x[1L]
  p <- ggplot(LM, aes(sample=.resid)) +
    stat_qq(alpha = 0.5) +
    geom_abline(slope = slope, intercept = int, color="black")
  
  return(p)
}

#custom function applied:
ggQQ.lm(model1)

# D. Sometimes still third party packages to intall
#----------------------------------------------
#library("quantreg")
#library("Hmisc")

#---------------------------------------------------------------------------
# 8. Going beyond scatterplots and smooth lines
#---------------------------------------------------------------------------
# we have seen scatterplots, histograms, density plots so far.

# add rugs to the density or histogram plot
ggplot(data=senicData, aes(x=nurses, fill=school)) + geom_histogram()  + geom_rug(aes(color=school)) 
#(make sure you get the aes of the previous plot)

#boxplot:
ggplot(data=senicData, aes(x=region, y=stay)) + geom_boxplot() + theme_bw()

#errorbars on your data:
se=0.4 #normally these are not just a fixed value
ggplot(data=senicData, aes(x=age, y=stay)) + geom_point() + geom_errorbar(aes(ymax = stay + se, ymin=stay - se))

#2D density
ggplot(data=senicData, aes(x=age, y=stay))+ geom_point() + geom_density2d(aes(color=region)) + geom_rug(col="blue") 

#AND OTHERS: http://docs.ggplot2.org/current/
# geom_abline  	geom_jitter
# geom_area		geom_line
# geom_bar		geom_linerange 
# geom_bin2d		geom_path 
# geom_blank		geom_point 
# geom_boxplot		geom_pointrange 
# geom_contour		geom_polygon 
# geom_crossbar		geom_quantile 
# geom_density		geom_rect 
# geom_density2d		geom_ribbon
# geom_errorbar		geom_rug 
# geom_errorbarh		geom_segment 
# geom_freqpoly		geom_smooth 
# geom_hex		geom_step 
# geom_histogram		geom_text 
# geom_hline		geom_tile
# geom_vline

## eg, make this work for linear regression outcome:
##
interv.pred <- as.data.frame(predict(model1, interval="prediction"))
interv.conf <- as.data.frame(predict(model1, interval="confidence"))
ggplot(senicData, aes(x=age,y=stay)) +
  geom_ribbon(aes(ymin=interv.pred$lwr,ymax=interv.pred$upr, fill='prediction'), alpha=0.2) +
  geom_ribbon(aes(ymin=interv.conf$lwr,ymax=interv.conf$upr, fill='confidence'), alpha=0.8) +
  geom_smooth(method="lm",se=FALSE,color='black') +
  geom_point() +
  xlab('Age (years)') +
  ylab('Average length of stay of the patients (days)')
##

#geom_XXX and stat_XXX sometimes a bit overlap..
# quantiles of the data:
q10 <- c(0.1,0.9)
ggplot(data=senicData, aes(x=age, y=stay)) + stat_quantile(aes(color=region), quantile=q10) + geom_point()
ggplot(data=senicData, aes(x=age, y=stay)) + geom_quantile(aes(color=region), quantile=q10) + geom_point()

# adding summary satistics...
ggplot(data=senicData, aes(x=region, y=stay))+ 
  geom_point() +
  stat_summary(fun.data = "mean_cl_boot", colour = "red", lwd=1) #Hmisc package

#---------------------------------------------------------------------------
# 8. Further extensions...
#---------------------------------------------------------------------------
library("GGally")

#SCATTERMATRIX
#for both continuous and discrete variable, you can decide what to place in the upper and lower part:
ggpairs(data=senicData, # data.frame with variables
        columns=c("stay", "age", "risk", "region"),  #, "beds", "census", "nurses"
        upper = list(continuous = "cor"),
        lower = list(continuous = "smooth", discrete = "facetbar"))

ggpairs(data=senicData, # data.frame with variables
        columns=c("stay", "age", "school"),  #, "beds", "census", "nurses"
        upper = list(continuous = "density", discrete = "ratio"),
        lower = list(continuous = "smooth", discrete = "facetbar"),
        color = "region")

plotm <- ggpairs(data=senicData, # data.frame with variables
        columns=c("stay", "age", "school"),  #, "beds", "census", "nurses"
        upper = list(continuous = "density", discrete = "ratio"),
        lower = list(continuous = "smooth", discrete = "facetbar"),
        color = "region")


# one of them custom?
personal_plot <- ggally_text(
  "ggpairs allows you\nto put in your\nown plot.\nLike this one.\n"
)
putPlot(plotm, personal_plot, 1, 3)

library("ggthemes")

ggplot(senicData, aes(x = age, y = stay, color=region)) + 
  geom_smooth(aes(colour=region), method='lm') +
  geom_point() + geom_rug() +
  theme_wsj()

#THEMES
#---------
# theme_calc  Theme Calc
# theme_economist	ggplot color theme based on the Economist
# theme_economist_white	ggplot color theme based on the Economist
# theme_excel	ggplot color theme based on old Excel plots  ????!!!???WTF**
# theme_few	Theme based on Few's "Practical Rules for Using Color in Charts"
# theme_foundation	Foundation Theme
# theme_gdocs	Theme with Google Docs Chart defaults
# theme_igray	Inverse gray theme
# theme_solarized	ggplot color themes based on the Solarized palette
# theme_solarized_2	ggplot color themes based on the Solarized palette
# theme_solid	Theme with nothing other than a background color
# theme_stata	Themes based on Stata graph schemes
# theme_tufte	Tufte Maximal Data, Minimal Ink Theme
# theme_wsj	Wall Street Journal theme


#---------------------------------------------------------------------------
# 9. No Python?!?
#---------------------------------------------------------------------------
# GGPLOT IS ALSO AVAILABLE FOR PYTHON => http://ggplot.yhathq.com/
# + ggplot, seaborn, bokeh,...
# 
# EXAMPLE TODO


#---------------------------------------------------------------------------
# 10. To conclude:
#---------------------------------------------------------------------------
# IF(!) you have a dataframe like datatable with some factors (multivariate/categorical data) 
# => ggplot is really the way to check the data, fit statsitical models, etc...
#...otherwise...just one of the many plot options!

#---------------------------------------------------------------------------
# FINALLY; CODA!
#---------------------------------------------------------------------------
# 1. HORIZON PLOT
# EXAMPLE TODO

# 2. CONCLUDING FIGURE ABOUT HOW TO MAKE DIFFERENCES (slideshow)
# SEARCH FIG!







