from django.shortcuts import render
from subscribe_repo import helpers


def upload(request):

    error_dict = {}
    num_recs_processed = 0

    if request.method == 'POST' and request.FILES['input_file']:
        input_file = request.FILES['input_file']
        error_dict, num_recs_processed = helpers.parse_subs(input_file)

    return render(request, 'upload.html', context={"processed": num_recs_processed,
                                                   "errors": error_dict})

