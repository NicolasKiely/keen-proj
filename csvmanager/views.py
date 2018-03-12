import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .validator import Validator


TEMP_FILE_NAME = 'csvmanager/static/files/temp.csv'
DATA_FILE_NAME = 'csvmanager/static/files/data.csv'


def index(request):
    ''' Default view '''
    return HttpResponseRedirect(reverse('csvmanager:upload'))


def upload(request):
    ''' Page for uploading cvs document '''
    return render(request, 'csvmanager/upload.html', {})


def document(request):
    ''' View document '''
    data = {}
    with open(DATA_FILE_NAME, 'rb') as fh_in:
        records = [x.split(',') for x in fh_in.read().split('\n')]
        data['header'] = records[0]
        data['records'] = records[1:]
    return render(request, 'csvmanager/document.html', data)


def post_upload(request):
    ''' Handle upload '''
    error = ''
    if request.method == 'POST' and request.FILES:
        fh_in = request.FILES.values()[0]
        if fh_in.size > 1024*1024:
            error = 'File too large'
        else:
            #data = fh_in.read()
            validator = Validator()
            with open(TEMP_FILE_NAME, 'wb+') as fh_out:
                for record in fh_in:
                    is_valid, msg = validator.is_valid(record)
                    if not is_valid:
                        error = msg
                        break
                    fh_out.write(record)

            if not error:
                ''' Successful download and validation, move temporary file '''
                os.rename(TEMP_FILE_NAME, DATA_FILE_NAME)
                
    if error:            
        return render(request, 'csvmanager/error.html', {'error': error})
    else:
        return HttpResponseRedirect(reverse('csvmanager:document'))
