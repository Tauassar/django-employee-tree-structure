from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from positions.models import Node


def index(request):
    # latest_question_list = Node.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'positions/index.html', context)
    return render(request, 'positions/index.html')
