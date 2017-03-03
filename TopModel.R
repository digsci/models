# TopModel.R

library(jsonlite)
library(topmodel)
data(huagrahuma)

#* @serializer hip_json
#* @post /topmodel
model <- function(parameters, topidx, delay, rain, ET0) {
  Qsim <- topmodel(as.vector(parameters), as.matrix(topidx), as.matrix(delay), as.matrix(rain), as.matrix(ET0)) 
  return(Qsim)
}

#* @serializer file_json
#* @post /topmodel_mc
model <- function(n, parameters, topidx, delay, rain, ET0) {
  runs <- n
  qs0 <- runif(runs, min=parameters$qs0[1], max=parameters$qs0[2])
  lnTe <- runif(runs, min=parameters$lnTe[1], max=parameters$lnTe[2])
  m <- runif(runs, min=parameters$m[1], max=parameters$m[2])
  Sr0 <- runif(runs, min=parameters$Sr0[1], max=parameters$Sr0[2])
  Srmax <- runif(runs, min=parameters$Srmax[1], max=parameters$Srmax[2])
  td <- runif(runs, min=parameters$td[1], max=parameters$td[2])
  vch <- parameters$vch
  vr <- runif(runs, min=parameters$vr[1], max=parameters$vr[2])
  k0 <- runif(runs, min=parameters$k0[1], max=parameters$k0[2])
  CD <- runif(runs, min=parameters$CD[1], max=parameters$CD[2])
  dt <- parameters$dt
  parameters_mc <- cbind(qs0,lnTe,m,Sr0,Srmax,td,vch,vr,k0,CD,dt)
  Qsim <- topmodel(parameters_mc, as.matrix(topidx), as.matrix(delay), as.matrix(rain), as.matrix(ET0)) 
}

#* @serializer hip_json
#* @get /huagrahuma
fnc <- function() {
  return(huagrahuma)
}

