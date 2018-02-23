$(function(){


    $(function(){
        if (window.location.pathname == "/results") {

            // On page load, set footer position to relative
            // $("footer").css("position", "relative");
            // On page load, set body height to 100%
            $("body").css("height", "100%")
            $("footer").hide();
        } else {
            // $("footer").css("position", "absolute");
            $("body").css("height", "100vh")
        }
    });


});


// ZILLOW API

$.ajax({
    url: 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id=X1-ZWz1g9apq54fm3_5upah&zpid=48749425',
    dataType: 'xml',
    success: function(data){
        $(data).find('address').each(function(){
            var street = $(this).find('street').text();
            var zip = $(this).find('zipcode').text();
            var city = $(this).find('city').text();
            var state = $(this).find('state').text();
            

            $('.zillow_data ul').append('<li>' 
            + street + '<br>'
            + city + " " + state + " " + zip + '</li>');

        });
    },
    error: function(){
        $('.zillow_data').text('Failed to get feed');
    }
});





// ============== GOOGLE MAP ============== //

function initMap(){

    // Map options
    var options = {
        zoom: 14,
        center:{lat:47.6062,lng:-122.3321}
    }
    
    // New map
    var map = new google.maps.Map(document.getElementById('map'), options);



    // Hard coded markers
    addMarker({
        coords:{lat:47.6062,lng:-122.3321},
        content: "<p>House 1 Info</p>"
        });
    addMarker({
        coords:{lat:47.607335,lng:-122.337979},
        content: "<p>House 2 Info</p>"
        });
    addMarker({
        coords:{lat:47.613257,lng:-122.331342},
        content: "<p>House 3 Info</p>"
        });
    addMarker({
        coords:{lat:47.598036,lng:-122.324956},
        content: "<p>House 4 Info</p>"
        });
    

    // Add Marker Function
    function addMarker(props){
            var marker = new google.maps.Marker({
            position: props.coords,
            map:map
        });

        // Check for content / info window
        if(props.content){
            
            //  Location info window
            var infoWindow = new google.maps.InfoWindow({
                content: props.content
            });

            marker.addListener('click', function(){
                infoWindow.open(map, marker);
            });
        }

    }

}
//==========================Randomize About Me Page=========================================
var aboutMe = $(".about");
for(var i = 0; i < aboutMe.length; i++){
    var target = Math.floor(Math.random() * aboutMe.length -1) + 1;
    var target2 = Math.floor(Math.random() * aboutMe.length -1) +1;
    aboutMe.eq(target).before(aboutMe.eq(target2));
}
//=========================Zillow API/Results Page============================================
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

//fetch API without CORS should display as {object}
var myInit = {mode : "no-cors"};
fetch(apiUrl, myInit)
	.then(response => response.text())
	.then(str => (new window.DOMParser()).parseFromString(str, "text/xml"))
    .then(data => displayResult(data));