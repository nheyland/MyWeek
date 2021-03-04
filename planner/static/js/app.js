mapboxgl.accessToken = 'pk.eyJ1IjoibmhleWxhbmQiLCJhIjoiY2toZHI4ZWNqMDgwaTMwczFuNnpvcGFuMiJ9.4LH3G0a18_HQY8t55W83lg';
var map = new mapboxgl.Map({
    container: 'map',
    center: [-98, 39],
    zoom: 2,
    style: 'mapbox://styles/mapbox/streets-v11'
});
map.on('load', function () {
    map.addSource('event', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': {{ geo | safe}}

        }
    });


map.addLayer({
    'id': 'event',
    'type': 'circle',
    'source': 'event',
    'paint': {
        'circle-radius': 6,
        'circle-color': 'red'
    },
    'filter': ['==', '$type', 'Point']
});
});

map.on('click', 'event', function (e) {
    map.flyTo({
        center: e.features[0].geometry.coordinates
    });
});
map.on('mouseenter', 'event', function () {
    map.getCanvas().style.cursor = 'pointer';
});
map.on('mouseleave', 'event', function () {
    map.getCanvas().style.cursor = '';
});
map.on('click', 'event', function (e) {
    var coordinates = e.features[0].geometry.coordinates.slice();
    var name = e.features[0].properties.name;
    var desc = e.features[0].properties.desc;
    var link = e.features[0].properties.link;
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    }
    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(`<a style="text-decoration: none;font-size: 1.0rem" href="${link}" <h3>` + name + '</h3> </a>')
        .addTo(map);
});
