from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import ForthGen, Profile, Evos
from django.db.models.functions import Greatest
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json


def main(request):
    return render(request, 'hgss/main.html')

@csrf_exempt
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
        evos = Evos.objects.all()
        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            listapoke = p.pokedex.split(",")
            locs = locs.filter(dex__in=listapoke)
            evos = evos.filter(dex2__in=listapoke)
        evos = evos.exclude(dex1__exact=0)
        evos = evos.exclude(dex2__exact=0)

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
            evos = evos.filter(dex2__gte=filterdex)
        else:
            locs = locs.filter(name__istartswith=data['poke'])
            evos = evos.filter(poke2__istartswith=data['poke'])

        locs = locs.annotate(maxprob=Greatest('probdawn', 'probday', 'probnight')
                    ).order_by('dex', '-maxprob')
        if data['selector'] == '1':
            lastpoke = ''
            pokes = []
            for l in locs.values():
                if lastpoke != l['name']:
                    pokes.append(l)
                    lastpoke = l['name']
        else:
            pokes = list(locs.values())

        if data['evo']:
            evolist=list(evos.values())
            for e in evolist:
                evotext = e["method"] + " " + e["level"]
                if e["method"] == "Level":
                    evotext = "Level up to lv." + e["level"]
                if e["method"] == "One level":
                    evotext = "Level up " + e["level"]
                if e["method"] == "Stone":
                    evotext = "Use a " + e["level"]
                if e["method"] == "Friendship":
                    evotext = "Level up with high friendship " + e["level"]
                if e["method"] == "Trade":
                    if e["level"] != "":
                        evotext = "Trade while holding a " + e["level"]
                    else:
                        evotext = "Trade"
                pokes.append({"dex":int(e["dex2"]), "name":e["poke2"], "place":evotext, "method":e["method"], "hg":2, "levelmin":"",
                "levelmax":"", "probdawn":-1, "probday":-1, "probnight":-1})

            pokes = sorted(pokes, key = lambda i: i["dex"])
            if limitON:
                pokes = pokes[:limit]
        return JsonResponse(pokes, safe=False)

def listToPokedex(lista):
    dex = ""
    for l in lista:
        dex += l + ","
    return dex[:-1]

def catchpoke(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        p = Profile.objects.get(user=request.user)
        pokedex = p.pokedex
        listapoke = pokedex.split(",")
        try:
            listapoke.remove(str(data['dex']))
        except ValueError:
            print("Value error al eliminar el pokemon " + str(data['dex']))
        p.pokedex = listToPokedex(listapoke)
        p.save()
    return HttpResponseRedirect('/')

def uncatchpoke(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        p = Profile.objects.get(user=request.user)
        pokedex = p.pokedex
        listapoke = pokedex.split(",")
        try:
            listapoke.append(str(data['dex']))
            listapoke.sort()
        except ValueError:
            print("Value error al eliminar el pokemon " + str(data['dex']))
        p.pokedex = listToPokedex(listapoke)
        p.save()
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            dexdefault = ""
            for i in range(1, 494):
                dexdefault += str(i) + ","
            dexdefault = dexdefault[:-1]
            p = Profile(user=User.objects.get(username__exact=form.cleaned_data.get('username')), pokedex=dexdefault)
            p.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        msg = ""
        pokes = []
        if request.method == "POST":
            i = 1
            listapokes = []
            print(len(request.POST['poketext']))
            if len(request.POST['poketext']) > 493:
                msg = "Input data must not exceed 493 numbers."
            else:
                for c in request.POST['poketext']:
                    if c != '0' and c != '1':
                        msg = "Input data must consist of only zeros and ones."
                        break
                    if c == "0":
                        listapokes.append(str(i))
                    i = i + 1
                for x in range(i, 494):
                    listapokes.append(str(x))
                if msg == "":
                    msg = listToPokedex(listapokes)
                    p = Profile.objects.get(user=request.user)
                    p.pokedex = listToPokedex(listapokes)
                    p.save()
        else:
            p = Profile.objects.get(user=request.user)
            listapoke = p.pokedex.split(",")
            i = 1
            pokes = []
            listacinco = []
            for x in range(1,496):
                if str(x) in listapoke:
                    haypoke = 0
                else:
                    haypoke = 1
                if(x > 493):
                    haypoke = 2
                listacinco.append({'catch':haypoke, 'zerodex':str(x).zfill(3), 'dex':x})
                if i == 5:
                    pokes.append(listacinco)
                    listacinco = []
                    i = 0
                i = i + 1

        return render(request, 'hgss/profile.html', {'msg':msg, 'pokes':pokes})
    else:
        return HttpResponseRedirect('/accounts/login')


def help(request):
    return render(request, 'hgss/help.html')