
let map;
async function initMap() {
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    
    // Coordinates passed from Django context
    var location = { lat:  latitude , lng:  longitude  };
    
    const { Map } = await google.maps.importLibrary("maps");
    map = new Map(document.getElementById('map'), {
        zoom: 15,
        center: location,
        mapId: '{{ GOOGLE_MAPS_MAP_ID }}'
        
        // https://console.cloud.google.com/google/maps-apis/studio/maps/27a4b3580577b009?project=clear-aurora-434315-s8
    });

    const marker = new AdvancedMarkerElement({
        map,
        position: location,
        title: 'Uluru',
    });
}

// Ensure initMap is called when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initMap();
});

