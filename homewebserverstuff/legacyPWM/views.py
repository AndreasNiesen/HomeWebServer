from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render
from .legMan import getPW


def legacyManager(request):
    if request.method == "POST":
        buff = request.POST
        try:
            result = getPW(buff["uname"], buff["passw"], buff["site"], int(buff["len"]), "nums" in buff.keys(), "specs" in buff.keys())
            context = {"uname": buff["uname"],
                       "passw": buff["passw"],
                       "site": buff["site"],
                       "len": buff["len"],
                       "num": "yes" if "nums" in buff.keys() else "no",
                       "spec": "yes" if "specs" in buff.keys() else "no",
                       "result": result[0]}
        except MultiValueDictKeyError:
            context = {"ERROR": "Stop playing around with the POST request!"}
        return render(request, "legacyPWM/manager.html", context)
    return render(request, "legacyPWM/manager.html")