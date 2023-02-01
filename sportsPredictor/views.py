from django.shortcuts import render

# Create your views here.


def main(request):
    return render(request, "index.html")

def predictOptions(request):
    return render(request, "predictOptions.html")