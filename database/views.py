from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import NSDLForm
from .backend import nsdl

class NSDL(FormView):
    template_name = 'database/index.html'
    form_class = NSDLForm

    def get(self, request):
        return render(request,
                      self.template_name, dict(form=self.form_class()))

    def form_valid(self, form):
       backend.main(form.cleaned_data["filepath"])
       return render(self.request,
                      self.template_name, dict(form=self.form_class()))

    def form_invalid(self, form):
        return HttpResponse("Invalid Form")
       