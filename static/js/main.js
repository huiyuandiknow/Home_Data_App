$(function(){

    // Change backgroung images
    var count = 0;
    var bgImages = ['/static/img/bg-img1.jpg',
                    '/static/img/bg-img2.jpg', 
                    '/static/img/bg-img3.jpg'];
    var bgImg = $(".bg-fader");

    bgImg.css("background-image", "url(" + bgImages[1] + ")");
    $('.bg-fader').css('background-size', 'cover');
    $('.bg-fader').css('background-position', 'center');
    $('.bg-fader').css('background-repeat', 'no-repeat');
    
    setInterval(function(){
        bgImg.fadeOut(2000, function(){
            bgImg.css("background-image", "url(" + bgImages[count++] + ")");
            bgImg.fadeIn(1000);
        });
        if (count == bgImages.length){
            count = 0;
        }
    }, 20000);



    // $(function(){
    //     if (window.location.pathname == "/results" || window.location.pathname == "/about") {
    //         // On page load, set body height to 100%
    //         $("body").css("height", "100%")
    //         // Hide footer on results page
    //         // $("footer").hide();
    //     } else {
    //         // $("footer").css("position", "absolute");
    //         $("body").css("height", "100vh")
    //     }
    // });


});


// ZILLOW API

$.ajax({
    url: 'https://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id=X1-ZWz1g9apq54fm3_5upah&zpid=48749425',
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
var obj = zil;
var lat =47.6062;
var lng =-122.3321;
var zilh=zil_home;
    if (zil_home != 'none'){
       lat=parseFloat(zilh.full_address.latitude);
       lng=parseFloat(zilh.full_address.longitude);
    }

function initMap(){

    // Map options
    var options = {
        zoom: 15,
         center:{lat:lat,lng:lng}

    }
    
    // New map
    var map = new google.maps.Map(document.getElementById('map'), options);
    var markers = [];
    setMarkers();
    setMarker();


        function setMarkers()  {
        var contentStrings = [];
        var i, marker;
        for (i = 0; i < obj.length; i++){
            var contentString = '<div id="content">'+
                   '<div id="siteNotice">'+
                   '</div>'+
                      '<h6 >'+ obj[i].zpid +'</h6>'+
                      '<div id="bodyContent">'+
                        '<p>similarity score:' + obj[i].similarity_score +  '</p>'+
                        '<p>address:' + obj[i].full_address.street + ' ' + obj[i].full_address.city + ' ' +
                        obj[i].full_address.zipcode + ' ' + obj[i].full_address.state +  '</p>'+
                        '<a href="'+obj[i].links.home_details+'">Detailed information</a>'+
                        '<p>zestimate value: $' + obj[i].zestimate.amount +  '</p>'+
                        '<a href="'+obj[i].links.graphs_and_data+'">graphs and data</a>'+
                      '</div>'+
                   '</div>'+

                '</div>';
            contentStrings.push(contentString);
            var infowindow = new google.maps.InfoWindow({
                content: contentString});
                console.log(obj[i].full_address.latitude)
            var curMarker = {lat: parseFloat(obj[i].full_address.latitude), lng: parseFloat(obj[i].full_address.longitude)};
            marker = new google.maps.Marker({
                position: curMarker,
                animation: google.maps.Animation.DROP,
                map:map,
                title: obj[i].name,
                infowindow: infowindow
            });
            marker.addListener('click', function() {
                this.infowindow.open(map, this);
            });
            markers.push(marker);
        }

}
function setMarker()  {
        var contentStrings = [];
        var  marker;

            var contentString = '<div id="content">'+
                   '<div id="siteNotice">'+
                   '</div>'+
                      '<h6 >'+ zilh.zpid +'</h6>'+
                      '<div id="bodyContent">'+
                        '<p>similarity score:' + zilh.similarity_score +  '</p>'+
                        '<p>address:' + zilh.full_address.street + ' ' + zilh.full_address.city + ' ' +
                        zilh.full_address.zipcode + ' ' + zilh.full_address.state +  '</p>'+
                        '<a href="'+zilh.links.home_details+'">Detailed information</a>'+
                        '<p>zestimate value: $' + zilh.zestimate.amount +  '</p>'+
                        '<a href="'+zilh.links.graphs_and_data+'">graphs and data</a>'+
                      '</div>'+
                   '</div>'+

                '</div>';
            contentStrings.push(contentString);
            var infowindow = new google.maps.InfoWindow({
                content: contentString});
                console.log(zilh.full_address.latitude)
            var curMarker = {lat: parseFloat(zilh.full_address.latitude), lng: parseFloat(zilh.full_address.longitude)};
            marker = new google.maps.Marker({
                position: curMarker,
                icon: 'http://maps.google.com/mapfiles/ms/icons/'+'green'+'.png',
                animation: google.maps.Animation.DROP,
                map:map,
                title: zilh.name,
                infowindow: infowindow
            });
            marker.addListener('click', function() {
                this.infowindow.open(map, this);
            });
            markers.push(marker);


}



    // Hard coded markers
/*    addMarker({
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
    */

    // Add Marker Function
/*    function addMarker(props){
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

    }*/

}

//==========================twitter Button events=========================
var tweet = document.getElementById("tweet");
var toTweet = "My home estimate is $" + 1000 + " Find yours at hom-es.herokuapp.com";

tweet.addEventListener("click", function () {
    var twitRL = "https://twitter.com/intent/tweet?text=" + toTweet;
   window.open(twitRL);
 });

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
$.ajax({
    url: apiUrl,
    crossDomain:true,
    dataType: 'xml',
    success: function(data){
        $(data).find('zestimate').each(function(){
            var amount = $(this).find('amount').text();
            displayResult(amount);
        });
    },
    error: function(){
        $('.zillow_data').text('Failed to get feed');
    }
});

//fetch API without CORS should display as {object}
// var myInit = {mode : "no-cors"};
// fetch(apiUrl, myInit)
// 	.then(response => response.text())
// 	.then(str => (new window.DOMParser()).parseFromString(str, "text/xml"))
//     .then(data => displayResult(data));