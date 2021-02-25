import requests as r


# We need to geocode the adresss -> Inpt str of an address return -> raw lat long coordinates
# {house number} {street} {city} {state} {zip} THIS is the format we have to use
# We can pass params into this to clean it up, but for now this works


def geocode(x):
    y = r.get('https://api.mapbox.com/geocoding/v5/mapbox.places/' + x +
              '.json?access_token=pk.eyJ1IjoibmhleWxhbmQiLCJhIjoiY2toZHI4ZWNqMDgwaTMwczFuNnpvcGFuMiJ9.4LH3G0a18_HQY8t55W83lg').json()

    return y['features'][0]['center']
