from django.shortcuts import render

def post_list(request):
    return render(request, 'hgss/post_list.html', {})
