from django.shortcuts import render

def index(request):
    return render(request, "home.html", {
        "a_list": [i for i in range(1,100)]
    })
