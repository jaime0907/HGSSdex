from django.shortcuts import render
from django.http import JsonResponse
from .models import ForthGen
from django.db.models.functions import Greatest
from django.db.models import Q
import json


def main(request):
    locations = ForthGen.objects.all()[1:50]
    return render(request, 'hgss/main.html', {'locations':locations})

def postview(request):
    if request.method == "POST":
        data = json.loads(request.body)

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

        locs = ForthGen.objects.all()
        q = Q(hg__gt=4)
        if data['hg']:
            q = q | Q(hg__exact=1)
        if data['ss']:
            q = q | Q(ss__exact=1)
        if data['d']:
            q = q | Q(d__exact=1)
        if data['pe']:
            q = q | Q(pe__exact=1)
        if data['pt']:
            q = q | Q(pt__exact=1)
        locs = locs.filter(q)
        if nameIsDex:
            locs = locs.filter(dex__gte=filterdex)
        else:
            locs = locs.filter(name__istartswith=data['poke'])

        locs = locs.annotate(maxprob=Greatest('probdawn', 'probday', 'probnight')
                    ).order_by('dex', '-maxprob')

        lastpoke = ''
        pokes = []
        for l in locs.values():
            if lastpoke != l['name']:
                pokes.append(l)
                lastpoke = l['name']
        if limitON:
            pokes = pokes[0:limit]

        return JsonResponse(pokes, safe=False)
