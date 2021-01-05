from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Person


def index(request):
    return JsonResponse({"message": "Initial page"})


def read(request, id=1):
    try:
        prsn = Person.objects.get(id=id)
        return JsonResponse({"name": "{0}".format(prsn.name),
                             "age": "{0}".format(prsn.age)})
    except Person.DoesNotExist:
        return JsonResponse("null", safe=False)


@csrf_exempt
def create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prsn, created = Person.objects.get_or_create(name=data["name"], age=data["age"])
        if created:
            return JsonResponse(
                {"message": "POST success. User {0} ({1} years old) was created".format(prsn.name, prsn.age)}
            )
        else:
            return JsonResponse(
                {"message": "POST fail. User {0} ({1} years old) already exists".format(prsn.name, prsn.age)},
                status=400
            )


@csrf_exempt
def update(request, id):
    try:
        prsn = Person.objects.get(id=id)
        if request.method == "PUT":
            data = json.loads(request.body)
            prsn.name = data["name"]
            prsn.age = data["age"]
            prsn.save()

            return JsonResponse(
                {"message": "PUT success. User with ID={0} was updated".format(id)},
            )

        if request.method == "PATCH":
            data = json.loads(request.body)

            update_fields = []
            for d in data:
                if d == "name":
                    prsn.name = data[d]
                elif d == "age":
                    prsn.age = data[d]

                update_fields.append(d)

            prsn.save(update_fields=update_fields)
            return JsonResponse(
                {"message": "PATCH success. User with ID={0} was updated".format(id)},
            )

    except Person.DoesNotExist:
        return JsonResponse(
            {"message": "Update fail. User with ID={0} does not exist".format(id)},
            status=400
        )

# return HttpResponse("{0}<br>{1}".format(name, age))

# Скорее всего надо думать в сторону
# data = json.loads(request.body)
# custom_decks = data['custom_decks']
