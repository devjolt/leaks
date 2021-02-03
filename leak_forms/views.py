from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic import ListView, CreateView
from django.conf import settings

import re, os, shutil

from formtools.wizard.views import SessionWizardView
from .forms import MeternoForm, LeakevidenceForm, GateKeeperForm, GateKeeperTwoForm, LeakFormOne, LeakFormTwo, LeakFormThree, LeakFormFour
from .models import LeakevidenceModel

import pypdftk
from pdf_forms import leak_pdf_filler as l

from django.core.mail import EmailMessage


TEMPLATE_PATH = 'leaks_app'
URL_PATH = 'leaks'

def instructions(request):
    request.session.flush()
    context = {}
    return render(request, f'{TEMPLATE_PATH}/instructions.html', context)

def gatekeeper(request):
    form = GateKeeperForm()
    context = {
        'first':True,
        'form':form
    }
    if request.method == 'POST':
        for key, value in request.POST.items():
            request.session[key] = 'Yes'
        #for key, value in request.session.items():
        #    print(key, value)

        form = GateKeeperForm(request.POST)
        counter = 0
        for item in request.POST:
            counter += 1
        if counter > 1:
            context = {
                'first':True,
                'warning':True,
                'warning1':True,
                'next_url':'/leaks/check_two',
                'form':form
            }
            return render(request, 'leaks_app/gatekeeper.html', context)
        else:
            
            return HttpResponseRedirect('/leaks/filler')

    return render(request, 'leaks_app/gatekeeper.html', context)

def filler(request):
    if request.method == 'POST':
        print('posty filler')
    for item in request.POST:
        del item
    return gateKeeperTwo(request)

def gateKeeperTwo(request):#changes need to be made
    #print(request.POST)

    form = GateKeeperTwoForm()
    context = {
        #'first':True,
        'form':form
    }
    if request.method == 'POST':#
        for key, value in request.POST.items():
            request.session[key] = 'Yes'
        for key, value in request.session.items():
            print(key, value)
        print('posty')
        form = GateKeeperTwoForm(request.POST)
        counter = 0
        for item in request.POST:
            counter += 1
        if counter < 7:
            context = {
                #'first':True,
                'warning':True,
                'warning1':True,
                'next_url':'/leaks/meter_form',
                'form':form
            }
            return render(request, 'leaks_app/gatekeepertwo.html', context)
        else:
            return HttpResponseRedirect('/leaks/meter_form')

    return render(request, 'leaks_app/gatekeepertwo.html', context)


from .forms import LeakevidenceForm, MeternoForm

def meter_number(request):
    if request.method == 'POST':
        form = MeternoForm(request.POST)
        if form.is_valid():
            response = HttpResponseRedirect(f"/{URL_PATH}/leak_evidence_form")
            response.set_cookie('meter', request.POST['meterno'])
            return response
    else:
        form = MeternoForm()
        return render(request, f'{TEMPLATE_PATH}/meterform.html', {'form':form})

def leak_evidence_form(request):
    if request.method == 'POST':
        form = LeakevidenceForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/{URL_PATH}/move')
    else:
        form = LeakevidenceForm(
            initial={
                'title': request.COOKIES['meter'],
                },)
        try:
            PATH = f"evidence/{request.COOKIES['meter']}"
            files = os.listdir(PATH)
            if len(files) > 0:
                uploaded = True
            else:
                uploaded = None
        except:
            uploaded = None
            files = None
        context = {
            'form':form,
            'files':files,
            'uploaded':uploaded
        }
    return render(request, f'{TEMPLATE_PATH}/leak_evidence.html', context)

def move_files(request):
    PATH = f"evidence/{request.COOKIES['meter']}"
    try:
        os.mkdir(PATH)
    except:
        print('Folder already there!')
        pass
    files = os.listdir('media/')
    print(files)
    for f in files:
        shutil.move('media/' + f, PATH)
    return HttpResponseRedirect(f"/{URL_PATH}/leak_evidence_form")


FORMS = [("LeakFormOne", LeakFormOne),
         ("LeakFormTwo", LeakFormTwo),
         ("LeakFormThree", LeakFormThree),
         ("LeakFormFour", LeakFormFour),]

TEMPLATES = {
    "LeakFormOne": "leaks_app/LeakFormOne.html",
    "LeakFormTwo": "leaks_app/LeakFormTwo.html",
    "LeakFormThree": "leaks_app/LeakFormThree.html",
    "LeakFormFour": "leaks_app/LeakFormFour.html",
}

class LeakFormTemplatesWizard(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        #print([form.cleaned_data for form in form_list])
        data_dict = {}
        for form in form_list:
            data_dict.update(form.cleaned_data)
        
        for key, value in self.request.session.items():
            if key == 'csrfmiddlewaretoken':
                pass
            new_key = re.sub('_', ' ', key)
            data_dict[new_key] = value

        for key, value in data_dict.items():
            if data_dict[key] == True:
                data_dict[key] = 'Yes'
            elif data_dict[key] == False:
                data_dict[key] = 'No'
            else:
                data_dict[key] = str(value)

        PATH = f"evidence/{self.request.COOKIES['meter']}/"
        #print(data_dict)
        l.fill_form(data_dict, f'{PATH}/poopy.pdf')
        context = {'form_data':[form.cleaned_data for form in form_list],}
        email = EmailMessage(
            'Hello',
            'Body goes here',
            'rbsrm100@hotmail.com',
            ['tom.m.warburton@gmail.com'],
            [],
            reply_to=['rbsrm100@hotmail.com'],
            headers={'Message-ID': 'Narf'},
        )
        #email.attach_file('poopy.pdf')
        PATH = f"evidence/{self.request.COOKIES['meter']}/"
        print(PATH)
        for file in os.listdir(PATH):
            print(file)
            email.attach_file(f'{PATH}/{file}')
        
        email.send()
        os.remove(f'{PATH}/poopy.pdf')
        shutil.rmtree(PATH)
        response = HttpResponseRedirect('/leaks/success')
        response.delete_cookie('meter')
        return response

class LeakFormWizard(SessionWizardView):
    def done(self, form_list, form_dict, **kwargs):
        data_dict = {}
        for form in form_list:
            data_dict.update(form.cleaned_data)
        
        for key, value in self.request.session.items():
            if key == 'csrfmiddlewaretoken':
                pass
            new_key = re.sub('_', ' ', key)
            data_dict[new_key] = value

        for key, value in data_dict.items():
            if data_dict[key] == True:
                data_dict[key] = 'Yes'
            elif data_dict[key] == False:
                data_dict[key] = 'No'
            else:
                data_dict[key] = str(value)
        #print(data_dict)
        l.fill_form(data_dict, 'poopy.pdf')
        context = {'form_data':[form.cleaned_data for form in form_list],}
        email = EmailMessage(
            'Hello',
            'Body goes here',
            'rbsrm100@hotmail.com',
            ['tom.m.warburton@gmail.com'],
            [],
            reply_to=['rbsrm100@hotmail.com'],
            headers={'Message-ID': 'Narf'},
        )
        email.attach_file('poopy.pdf')
        PATH = f"evidence/{request.COOKIES['meter']}/"
        print(PATH)
        for file in os.listdir(path):
            print(file)
            email.attach_file(f'{PATH}/{file}')
        
        email.send()
        os.remove('poopy.pdf')
        shutil.rmtree(PATH)
        response = HttpResponseRedirect('leaks/success')
        response.delete_cookie('meter')
        return response

def submission_successful(request):
    #code to populate a form
    request.session.flush()
    return HttpResponse('You got it')
# Create your views here.


