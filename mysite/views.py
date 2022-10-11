from django.shortcuts import render
from places.models import Place, PlaceImage

def show_main(request):
    locations = Place.objects.all()
    locations_format_geojson = []
    for location in locations:

        formatted_location = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(location.lng), float(location.lat)]
            },
            "properties": {
                "title": location.title,
                "placeId": location.id,
                "detailsUrl": ""
            }
        }
        locations_format_geojson.append(formatted_location)

    context = {'geojson' :
        {
        "type": "FeatureCollection",
        'features': locations_format_geojson
        }
    }
    return render(request, 'index.html', context=context)
