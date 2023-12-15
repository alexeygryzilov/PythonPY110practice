from django.shortcuts import render

from django.http import JsonResponse
from weater_api import current_weather


#def my_view(request):
#   if request.method == "GET":
#        data = current_weather(59.93, 30.31)
#        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                    'indent': 4})

def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get('lat')  # данные придут в виде строки
        lon = request.GET.get('lon')  # данные придут в виде строки
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(59.93, 30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})