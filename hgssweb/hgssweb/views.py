from django.shortcuts import render
from django.http import JsonResponse
from .models import Locations
from django.db.models.functions import Greatest
import json


def main(request):
    locations = Locations.objects.all()[1:10]
    return render(request, 'hgss/main.html', {'locations':locations})

def postview(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if data['game'] == '0':
            games = [0,2]
        elif data['game'] == '1':
            games = [1,2]
        elif data['game'] == '2':
            games = [0,1,2]
        else:
            games = []

        limitON = False
        try:
            limit = int(data['limit'])
            limitON = True
        except ValueError:
            limitON = False

        nameIsDex = False
        try:
            filterdex = int(data['poke'])
            nameIsDex = True
        except ValueError:
            nameIsDex = False

        locs = Locations.objects.filter(game__in=games)
        if nameIsDex:
            locs = locs.filter(dex__gte=filterdex)
        else:
            locs = locs.filter(name__istartswith=data['poke'])

        locs = locs.annotate(maxprob=Greatest('probdawn', 'probday', 'probnight')
                    ).order_by('dex', '-maxprob')

        print(data)
        lastpoke = ''
        pokes = []
        for l in locs.values():
            if lastpoke != l['name']:
                pokes.append(l)
                lastpoke = l['name']
        if limitON:
            pokes = pokes[0:limit]

        return JsonResponse(pokes, safe=False)
