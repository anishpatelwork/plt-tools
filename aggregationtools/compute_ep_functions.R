
## ------------------------------------------------------------
## get aa, bb from mu,sigma
## ------------------------------------------------------------
get.aa.bb <- function( fn.est ) {
  fn.mu <- fn.est$mu
  fn.sigma <- fn.est$sigma
  fn.cv <- fn.sigma / fn.mu
  fn.aa <- (1. - fn.mu)/ fn.cv^2 - fn.mu
  fn.bb <- fn.aa * (1. - fn.mu)/ fn.mu
  
  result <- data.frame( aa = fn.aa, bb = fn.bb, mu = fn.mu, sigma = fn.sigma, cv = fn.cv)

}

## ------------------------------------------------------------
## get mu,sigma2,cv from aa, bb 
## ------------------------------------------------------------
get.mu.sigma2.cv <- function( fn.par ) {
  fn.aa <- fn.par$aa
  fn.bb <- fn.par$bb
  fn.mu <- fn.aa / (fn.aa + fn.bb)
  fn.sigma2 <- (fn.aa * fn.bb) / ( (fn.aa + fn.bb)^2 * (fn.aa + fn.bb + 1) )
  fn.cv <- sqrt(fn.sigma2) / fn.mu
  
##  fn.cv0 <- sqrt(fn.bb / ( fn.aa * (fn.aa + fn.bb + 1) )) ## alternative 

  result <- data.frame( aa = fn.aa, bb = fn.bb, mu = fn.mu, sigma2 = fn.sigma2, cv = fn.cv)

}


### ========================================================== ###
## ------------------------------------------------------------
## get alpha, beta from mu,sigma
## ------------------------------------------------------------
get.alpha.beta <- function( fn.mu, fn.sigma ) {
  fn.cv <- fn.sigma / fn.mu
  fn.alpha <- (1. - fn.mu)/ fn.cv^2 - fn.mu
  fn.beta <- fn.alpha * (1. - fn.mu)/ fn.mu

  result <- data.frame( aa = fn.alpha, bb = fn.beta)

}

## -------------------------------------------- ##
## Compute OEP curve WITH 2ndary Uncertainty ##
## -------------------------------------------- ##
compute.ep.with2nd <- function(fn.rate, fn.loss, fn.sigma, fn.expsr, fn.nn = 2^14){
  
  ## loss ratios
  mlr <- fn.loss[] / fn.expsr []
  std <- fn.sigma[] / fn.expsr []
  alpha.beta <- get.alpha.beta(mlr, std)
  
  invalid.beta <- which( (alpha.beta$aa <= 0 ) | ( alpha.beta$bb <= 0 ) )
  if (length(invalid.beta)>0){
    cat('Invalid Betas: \n')
    print(invalid.beta)
    print(alpha.beta[invalid.beta,])
  }
  
  ## Use only valid events
  valid.beta <- which( (alpha.beta$aa > 0 ) & ( alpha.beta$bb > 0 ) )
  alpha.beta <- alpha.beta[ valid.beta, ]  
  fn.rate <- fn.rate[ valid.beta ]
  fn.loss <- fn.loss[ valid.beta ]
  fn.sigma <- fn.sigma[ valid.beta ]
  fn.expsr <- fn.expsr [ valid.beta ]
  mlr <- mlr[ valid.beta ]
  std <- std[ valid.beta ]
  fn.nevents <- length(fn.rate)
  lambda <- sum(fn.rate)
  
  my.info <- sprintf('*** EPs WITH 2nd, NN= %i, NEVENTS= %i',fn.nn,fn.nevents); cat('\n', my.info,'\n')
  
  
  ## Computational grid
  nn <- fn.nn
  
  ## ------------- original grid -----------------##
  max.ll <- 5.0*max(fn.loss, na.rm=TRUE)
  dx <- max.ll/nn
  xx <- c((1:nn)*dx)
  my.info <- sprintf('dx= %e, max(xx)= %e, min(xx)= %e', dx, max(xx), min(xx)); cat(my.info, '\n')
  ## ------------- original grid -----------------##
  
  ## ------------- alternative grid -----------------##
  ##max.ll <- 20.0*max(fn.loss, na.rm=TRUE)
  ##min.ll <- 0.2*min(fn.loss, na.rm=TRUE)
  ##dx <- (max.ll - min.ll) / (nn - 1)
  ##xx <- seq(min.ll, max.ll, by = dx)
  ##my.info <- sprintf('dx= %e, max.loss= %e, min.loss= %e', dx, max.ll, min.ll); cat(my.info, '\n')
  ## ------------- alternative grid -----------------##
  
  
  ## Initialize arrays
  FX1 <- array(0.0, nn)
  FX2 <- array(0.0, nn)
  
  for (ievent in 1:fn.nevents){
    
    this.lambda <- fn.rate[ievent]
    this.aa <- alpha.beta$aa[ievent]
    this.bb <- alpha.beta$bb[ievent]
    this.mlr <- mlr[ievent]
    this.std <- std[ievent]
    
    this.xx <- xx / fn.expsr[ievent]
    this.dx <- dx / fn.expsr[ievent]
    
    ## MAX EP
    this.FX <- pbeta( this.xx[1:nn], shape1 = this.aa, shape2 = this.bb)
    FX1 <- FX1 + (this.lambda/lambda)* this.FX
    
    ## SUM EP
    this.FX2 <- c()
    this.FX2[1] <- pbeta(this.xx[1] - this.dx/2, shape1 = this.aa, shape2 = this.bb)
    cdf2 <- pbeta( this.xx[2:nn-1] + this.dx/2, shape1 = this.aa, shape2 = this.bb)
    cdf1 <- pbeta( this.xx[2:nn-1] - this.dx/2, shape1 = this.aa, shape2 = this.bb)
    this.FX2[2:nn] <- cdf2 - cdf1    
    FX2 <- FX2 + (this.lambda/lambda)* this.FX2

    if ( (ievent %% 1000 == 0)) {  my.info <- sprintf('Event: %6i',ievent); cat(my.info,'\r') }
    
  }
  cat('\nFinished.\n')
  
  ## MAX
  CEP <- 1. - FX1
  OEP <- 1.0 - exp( -lambda* (1. - FX1))
  EEF <- lambda*CEP
  
  
  ## SUM
  fx.hat <- fft(FX2)
  fs.hat <- exp( -lambda* (1. - fx.hat) )
  fs <- Re( fft(fs.hat, inverse = TRUE) /nn)
  FS <- cumsum( fs )
  AEP <- 1.0 - FS
  
  rtrn <- data.frame( xr = xx, oep = OEP, eef = EEF, cep = CEP, aep = AEP)
  
}


## ---------------------------------------------- ##
## Compute the OEP curve using Sorting, return RP ##
## ---------------------------------------------- ##
compute.oep <- function(rate, value, sid){

  nn <- length(value)
  srt <- sort(value, decreasing = TRUE, index.return = TRUE)

  rate.srt <- rate[ srt$ix[1:nn] ]
  sid.srt <- sid[ srt$ix[1:nn] ]
    

  cumsum.rate <- cumsum( rate.srt )
  EP <- 1. - exp( -cumsum.rate )

  rtrn <- data.frame( xr = srt$x[1:nn], pp = 1-EP, ep = EP, rp = 1/EP, rate = rate.srt, sid = sid.srt, loss=srt)

}

## ---------------------------------------------- ##
## Compute the EEF curve using Sorting, return RP ##
## ---------------------------------------------- ##
compute.eef <- function(rate, value, sid){

  fn.val <- value
  fn.val[ fn.val <0 ] <- NA

  nn <- length(fn.val)
  srt <- sort(fn.val, decreasing = TRUE, index.return = TRUE)

  rate.srt <- rate[ srt$ix[1:nn] ]
  sid.srt <- sid[ srt$ix[1:nn] ]
  
  cumsum.rate <- cumsum( rate.srt )
  EP <- cumsum.rate

  rtrn <- data.frame( loss = srt$x[1:nn], eef = EP, erp = 1/EP, rate = rate.srt, sid = sid.srt)
}



## ------------------------------------------------------------
## Fit a spline through OEP to compute at standard RP values
## ------------------------------------------------------------
calc.standard.rps0 <- function(fn.ep, fn.standard.rp ) {

  fn.xr <- fn.ep$xr
  fn.oep <- fn.ep$oep
  fn.aep <- fn.ep$aep
  fn.eef <- fn.ep$eef
  fn.cep <- fn.ep$cep
  
  my.fit.oep <- approxfun(fn.oep, fn.xr, rule = 1)
  my.fit.aep <- approxfun(fn.aep, fn.xr, rule = 1)
  my.fit.cep <- approxfun(fn.cep, fn.xr, rule = 1)
  my.fit.eef <- approxfun(fn.eef, fn.xr, rule = 1)
  
  fn.xr.oep <- my.fit.oep(1/fn.standard.rp)
  fn.xr.aep <- my.fit.aep(1/fn.standard.rp)
  fn.xr.cep <- my.fit.cep(1/fn.standard.rp)
  fn.xr.eef <- my.fit.eef(1/fn.standard.rp)
  
  result <- data.frame(  rp = fn.standard.rp
                       , ep = 1./fn.standard.rp
                       , oep = fn.xr.oep
                       , aep = fn.xr.aep
                       , cep = fn.xr.cep 
                       , eef = fn.xr.eef
                      ) 
  
}

## ------------------------------------------------------------
## Fit a spline through OEP to compute at standard RP values
## ------------------------------------------------------------
calc.standard.rps <- function(fn.loss, fn.rp, fn.standard.rp ) {

  my.fit.rp <- approxfun(fn.rp, fn.loss, rule = 1)  
  fn.xr <- my.fit.rp(fn.standard.rp)  
  result <- data.frame(  rp = fn.standard.rp, ep = 1./fn.standard.rp, loss = fn.xr ) 
  
}


## ------------------------------------------------------------
## 
## ------------------------------------------------------------
invert.loss <- function(fn.loss, fn.ep, fn.xr ) {

  my.fit <- approxfun(fn.loss, fn.ep, rule = 1)  

  fn.ep.at.xr <- my.fit( fn.xr )
  
}







## ------------------------------------------------------------------------ ##
## NJM@RMS [06-Sep-2012]: Compute OEP curve WITH 2ndary Uncertainty, NO AEP ##
## ------------------------------------------------------------------------ ##
compute.ep.with2nd.njm <- function(fn.rate, fn.loss, fn.sigma, fn.expsr, fn.nn = 2^14){

  ## loss ratios
  mlr <- fn.loss[] / fn.expsr []
  std <- fn.sigma[] / fn.expsr []
  alpha.beta <- get.alpha.beta(mlr, std)
  
  invalid.beta <- which( (alpha.beta$aa <= 0 ) | ( alpha.beta$bb <= 0 ) )
  if (length(invalid.beta)>0){
    cat('Invalid Betas: \n')
    print(invalid.beta)
    print(alpha.beta[invalid.beta,])
  }
  
  ## Use only valid events
  valid.beta <- which( (alpha.beta$aa > 0 ) & ( alpha.beta$bb > 0 ) )
  alpha.beta <- alpha.beta[ valid.beta, ]  
  fn.rate <- fn.rate[ valid.beta ]
  fn.loss <- fn.loss[ valid.beta ]
  fn.sigma <- fn.sigma[ valid.beta ]
  fn.expsr <- fn.expsr [ valid.beta ]
  mlr <- mlr[ valid.beta ]
  std <- std[ valid.beta ]
  fn.nevents <- length(fn.rate)
  lambda <- sum(fn.rate)
  
  my.info <- sprintf('*** EPs WITH 2nd, NN= %i, NEVENTS= %i',fn.nn,fn.nevents); cat('\n', my.info,'\n')
  
  
  ## Computational grid
  nn <- fn.nn
  
  ## ------------- original grid -----------------##
  max.ll <- 5.0*max(fn.loss, na.rm=TRUE)
  dx <- max.ll/nn
  xx <- c((1:nn)*dx)
  my.info <- sprintf('dx= %e, max(xx)= %e, min(xx)= %e', dx, max(xx), min(xx)); cat(my.info, '\n')
  ## ------------- original grid -----------------##
  
  ## ------------- alternative grid -----------------##
  ##max.ll <- 20.0*max(fn.loss, na.rm=TRUE)
  ##min.ll <- 0.2*min(fn.loss, na.rm=TRUE)
  ##dx <- (max.ll - min.ll) / (nn - 1)
  ##xx <- seq(min.ll, max.ll, by = dx)
  ##my.info <- sprintf('dx= %e, max.loss= %e, min.loss= %e', dx, max.ll, min.ll); cat(my.info, '\n')
  ## ------------- alternative grid -----------------##
  
  
  ## Initialize arrays
  FX1 <- array(0.0, nn)
  FX2 <- array(0.0, nn)
  
  for (ievent in 1:fn.nevents){
    
    this.lambda <- fn.rate[ievent]
    this.aa <- alpha.beta$aa[ievent]
    this.bb <- alpha.beta$bb[ievent]
    this.mlr <- mlr[ievent]
    this.std <- std[ievent]
    
    this.xx <- xx / fn.expsr[ievent]
    this.dx <- dx / fn.expsr[ievent]
    
    ## MAX EP
    this.FX <- pbeta( this.xx[1:nn], shape1 = this.aa, shape2 = this.bb)
    FX1 <- FX1 + (this.lambda/lambda)* this.FX
    
    ## SUM EP
    ##this.FX2 <- c()
    ##this.FX2[1] <- pbeta(this.xx[1] - this.dx/2, shape1 = this.aa, shape2 = this.bb)
    ##cdf2 <- pbeta( this.xx[2:nn-1] + this.dx/2, shape1 = this.aa, shape2 = this.bb)
    ##cdf1 <- pbeta( this.xx[2:nn-1] - this.dx/2, shape1 = this.aa, shape2 = this.bb)
    ##this.FX2[2:nn] <- cdf2 - cdf1    
    ##FX2 <- FX2 + (this.lambda/lambda)* this.FX2

    if ( (ievent %% 1000 == 0)) {  my.info <- sprintf('Event: %6i',ievent); cat(my.info,'\r') }
    
  }
  cat('\nFinished.\n')
  
  ## MAX
  CEP <- 1. - FX1
  OEP <- 1.0 - exp( -lambda* (1. - FX1))
  EEF <- lambda*CEP
  
  
  ## SUM
  ##fx.hat <- fft(FX2)
  ##fs.hat <- exp( -lambda* (1. - fx.hat) )
  ##fs <- Re( fft(fs.hat, inverse = TRUE) /nn)
  ##FS <- cumsum( fs )
  ##AEP <- 1.0 - FS
  ##
  ##rtrn <- data.frame( xr = xx, oep = OEP, eef = EEF, cep = CEP, aep = AEP)
  rtrn <- data.frame(xr = xx, oep = OEP, eef = EEF, cep = CEP)
  
}
