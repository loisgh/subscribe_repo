from django.shortcuts import render
from subscribe_repo import helpers


def upload(request):
    error_dict = {}
    num_recs_processed = 0
    num_recs_updated = 0
    if request.method == 'POST' and request.FILES['input_file']:
        input_file = request.FILES['input_file']
        str_text = ''
        for line in input_file:
            str_text += line.decode()
            str_text = str_text.replace('\n', '')
            error_dict = helpers.parse_subs(str_text)
            str_text = ""
            num_recs_processed += 1
        num_recs_updated = num_recs_processed - len(error_dict)

    return render(request, 'upload.html', context={"processed": num_recs_processed, "updated": num_recs_updated,
                                                   "errors": error_dict})