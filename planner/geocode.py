import geocoder
# We need to geocode the adresss -> Inpt str of an address return -> raw lat long coordinates
import requests as r


# {house number} {street} {city} {state} {zip} THIS is the format we have to use


def geocode(x):
    return r.get('https://api.mapbox.com/geocoding/v5/mapbox.places/' + x +
                 '.json?access_token=pk.eyJ1IjoibmhleWxhbmQiLCJhIjoiY2toZHI4ZWNqMDgwaTMwczFuNnpvcGFuMiJ9.4LH3G0a18_HQY8t55W83lg').text
