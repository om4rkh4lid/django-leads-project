from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm, LeadForm, CustomCreateUserForm


class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomCreateUserForm

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("login")


class LandingPageView(TemplateView):
    # required field
    template_name = 'landing.html'


class LeadListView(ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, "leads/lead_list.html", context)


class LeadDetailView(DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_detail.html', context)


class LeadCreateView(CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="New lead created!",
            message="Please visit the site to view the new lead.",
            from_email='xom4rxkh4lidx@gmail.com',
            recipient_list=['xom4rxkh4lidx@gmail.com']
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()  # create the form to send to the template
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            print('Lead object successfully created!')
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, 'leads/lead_create.html', context)


class LeadUpdateView(UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            print('Lead object successfully updated!')
            return redirect('/leads')
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    # what happens after the form is saved successfully?s
    def get_success_url(self):
        # works the same way as template URLs
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    print('Lead object successfully deleted!')
    return redirect('/leads')


# def landing_page(request):
#     return render(request, "landing.html")

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()  # create the form to send to the template
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             fname = form.cleaned_data['first_name']
#             lname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = fname
#             lead.last_name = lname
#             lead.age = age
#             lead.save()  # commit changes
#             print('Lead object successfully created!')
#             return redirect('/leads')
#     context = {
#         "form": form
#     }
#     return render(request, 'leads/lead_create.html', context)

# def lead_create(request):
    # form = LeadForm()  # create the form to send to the template
    # if request.method == 'POST':
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         fname = form.cleaned_data['first_name']
    #         lname = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=fname,
    #             last_name=lname,
    #             age=age,
    #             agent=agent
    #         )
    #         print('Lead object successfully created!')
    #         return redirect('/leads')
    # context = {
    #     "form": form
    # }
    # return render(request, 'leads/lead_create.html', context)
