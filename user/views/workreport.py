from django.shortcuts import render, HttpResponse


def workreport_list(request):
    return render(request, 'workreport_list.html')
