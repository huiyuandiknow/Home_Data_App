//vars
var result = document.getElementById("zest");
var address = "2114+Bigelow+Ave";
var city = "Seattle";
var state = "WA";

var apiUrl = "http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz18s18qx40ln_4vl2o&address="+address+"&citystatezip="+city+"%2C+" + state;

//display result
function displayResult(res){
	result.innerHTML = "$ " + res;
}

//fetch API
var myHeader = new Headers();
myHeader.append("Referer", apiUrl);

var myInit = {headers: myHeader};

fetch(apiUrl, myInit)
	.then(response => response.text())
	.then(str => (new window.DOMParser()).parseFromString(str, "text/xml"))
    .then(data => displayResult(data));
    
