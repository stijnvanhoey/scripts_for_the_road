#should have known R already has horizon plot functionality
#latticeExtra (already a favorite package of mine) has it sitting right there
#http://rgm2.lab.nig.ac.jp/RGM2/func.php?rd_id=latticeExtra:horizonplot


require(lattice)
require(latticeExtra)
require(reshape2)
require(quantmod)

tckrs <- c("^W0DOW","^GSPC","^RUT","^E1DOW","^P1DOW","^DJUBS")

getSymbols(tckrs,from="2011-12-31")

#combine prices together
prices <- na.omit(merge(W0DOW[,4],GSPC[,4],RUT[,4],E1DOW[,4],P1DOW[,4],DJUBS[,4]))
#get change since beginning of period
change <- prices/matrix(rep(prices[1,],NROW(prices)),nrow=NROW(prices),ncol=NCOL(prices),byrow=TRUE) -1
colnames(change) <- tckrs

#using the example as presented in horizonplot documentation
horizonplot(change,layout=c(1,NCOL(change)),
            scale=0.05,
            par.settings=theEconomist.theme(box="transparent"),
            #if you want y labels in the graph uncomment
            #           panel = function (x,y,...) {
            #             panel.horizonplot(x,y,...)
            #             panel.text(x=x[1],y=0,label=colnames(change)[panel.number()],pos=3)
            #            },
            strip.left = FALSE,
            scales = list(y = list(draw = FALSE,relation = "same",alternating=FALSE)),
            main="World Indexes Change Since 2011",
            xlab=NULL,
            ylab = list(rev(colnames(change)), rot = 0, cex = 0.8)) +
  #add some separation between graphs with small white band
  layer(panel.xblocks(height=0.001,col="white",...))
