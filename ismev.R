# ismev

library(ismev)
data(dowjones)

#* @serializer hip_json
#* @post /gpd
model <- function(xdat, threshold) {
  gpd_model <- gpd.fit(xdat, threshold) 
  return(gpd_model)
}

#* @serializer hip_json
#* @get /dowjones
fnc <- function() {
	  return(dowjones)
}
