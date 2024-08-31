function initMap() {
    // Coordinates passed from Django context
    var location = { lat:  latitude , lng:  longitude  };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: location
    });

    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}

// Ensure initMap is called when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initMap();
});
