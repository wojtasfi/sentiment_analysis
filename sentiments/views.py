import json

from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view

from sentiments.analysis.SentimentAnalysisService import SentimentAnalysisService
from .models import Analysis, AnalysisPending, OneDayResult, TwitterAuth

SentimentAnalysisService()


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def analysis_all(request):
    try:
        page = request.GET.get('page', 1)
        size = request.GET.get('size', 10)
        sort = request.GET.get('sort', 'text')
        order_param = __retrieve_order_param__(request)

        analysis = Analysis.objects.order_by(order_param + sort)

        paginator = Paginator(analysis, size)
        response = HttpResponse(__query_set_to_response_string__(paginator.page(page)), content_type="application/json")

        return response
    except Analysis.DoesNotExist:
        raise Http404("Could not retrieve analysis")


def __retrieve_order_param__(request):
    order = request.GET.get('order', 'asc')
    order_param = ''
    if order == 'desc':
        order_param = '-'
    return order_param


@api_view(['GET'])
def analysis(request, analysis_id):
    try:
        analysis = Analysis.objects.get(id=analysis_id)
        json_analysis = __query_result_to_json__(analysis)
        days_results = OneDayResult.objects.filter(analysis_id=analysis_id)
        json_days_results = __query_set_array_to_json_array__(days_results)

        json_analysis['days_results'] = json_days_results
        return HttpResponse(__to_response_string__(json_analysis), content_type="application/json")
    except Analysis.DoesNotExist:
        raise Http404("Analysis with id %s does not exist" % analysis_id)


@api_view(['GET', 'POST'])
def analysis_pending(request):
    if request.method == 'GET':
        return analysis_pending_all(request)
    elif request.method == 'POST':
        return submit_analysis(request)
    else:
        raise HttpResponse('Only GET and POST methods are supported')


def analysis_pending_all(request):
    try:
        pendings = AnalysisPending.objects.all()
        response = HttpResponse(__query_set_to_response_string__(pendings), content_type="application/json")

        return response
    except AnalysisPending.DoesNotExist:
        raise Http404("Could not retrieve analysis pending list")


def submit_analysis(request):
    query = request.data['text']
    analysis_pending = AnalysisPending(text=query)
    analysis_pending.save()

    return HttpResponse("Analysis submitted")


@api_view(['GET'])
def single_analysis_pending(request, analysis_pending_id):
    try:
        analysis_pending = AnalysisPending.objects.get(id=analysis_pending_id)
        response = "Analysis with id %s is: %s."
        return HttpResponse(__query_result_to_response_string__(analysis_pending), content_type="application/json")
    except AnalysisPending.DoesNotExist:
        raise Http404("Pending Analysis with id %s does not exist" % analysis_pending_id)


@api_view(['GET'])
def analysis_count(request):
    try:
        analysis = Analysis.objects.all()
        return HttpResponse(analysis.count())
    except Analysis.DoesNotExist:
        raise Http404("Could not get analysis count")


@api_view(['GET'])
def analysis_pending_count(request):
    try:
        pendings = AnalysisPending.objects.all()
        return HttpResponse(pendings.count())
    except Analysis.DoesNotExist:
        raise Http404("Could not get analysis pendings count")


@api_view(['GET'])
def twitter_auth_exists(request):
    try:
        auth = TwitterAuth.objects.all()
        return HttpResponse(auth.count() > 0)
    except Analysis.DoesNotExist:
        raise Http404("Could not get twitter auth")


@api_view(['GET'])
def twitter_auth_error(request):
    try:
        auth_query_set = TwitterAuth.objects.all()
        if (auth_query_set.count() > 0):
            auth = auth_query_set[0]
            if auth.error is None:
                return HttpResponse()
            return HttpResponse(auth.error)
        return HttpResponse()
    except Analysis.DoesNotExist:
        raise Http404("Could not get twitter error")


@api_view(['POST'])
def add_twitter_auth(request):
    try:
        TwitterAuth.objects.all().delete()
        auth = TwitterAuth(
            consumer_key=request.data['consumerKey'],
            consumer_secret=request.data['consumerSecret'],
            access_token=request.data['accessToken'],
            access_token_secret=request.data['accessTokenSecret']
        )
        TwitterAuth.save(auth)
        return HttpResponse("OK")
    except Analysis.DoesNotExist:
        raise Http404("Could not add twitter auth")


def __query_set_to_response_string__(query_set_array):
    json_resources = __query_set_array_to_json_array__(query_set_array)
    return __array_to_response_string__(json_resources)


def __query_result_to_response_string__(query_result):
    json_resource = __query_result_to_json__(query_result)
    return __to_response_string__(json_resource)


def __query_result_to_json__(result):
    resource_dict = {}
    json_array = serializers.serialize('json', [result])
    for object in json.loads(json_array):
        resource_dict['id'] = object['pk']
        for key in object['fields'].keys():
            resource_dict[key] = object['fields'].get(key)

    return resource_dict


def __query_set_array_to_json_array__(query_set_array):
    json_array = serializers.serialize('json', query_set_array)
    json_resources = []
    for object in json.loads(json_array):
        resource_dict = {'id': object['pk']}
        for key in object['fields'].keys():
            resource_dict[key] = object['fields'].get(key)
        json_resources.append(resource_dict)
    return json_resources


def __array_to_response_string__(json_resources):
    if len(json_resources) == 1:
        return json.dumps(json_resources[0])
    else:
        return json.dumps(json_resources)


def __to_response_string__(json_resource):
    return json.dumps(json_resource)
