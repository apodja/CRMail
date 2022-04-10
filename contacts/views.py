
from re import template
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from contacts.models import Contact, Audience,EmailTemplate,Campaign,CustomUser
from contacts.forms import ContactModelForm,CustomUserCreationForm
from bootstrap_modal_forms.generic import BSModalUpdateView,BSModalDeleteView
from django.urls import reverse_lazy
from django.db.models import Count
import csv
import io
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.views import LoginView    
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin




class ContactsListview(LoginRequiredMixin,ListView):
    model= Contact
    template = 'contacts/contacts_list.html'
    context_object_name = 'contacts'
    paginate_by = 1

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

class ContactDetailView(LoginRequiredMixin,DetailView):
    model = Contact
    template = 'contacts/contacts_detail.html'
    context_object_name = 'contact'
    

class UpdateContact(BSModalUpdateView):
    model = Contact
    template_name='contacts/update_contact.html'
    form_class = ContactModelForm
    success_url="Success: Contact was updated successfully !"
    success_url = reverse_lazy('contact_list')


@login_required
def audience(request, pk):
    audience = Audience.objects.get(id=pk)

    contacts = Contact.objects.filter(audience = audience.id)

    context={'audience': audience, 'contacts':contacts}

    return render(request,'contacts/audience.html',context)

@login_required
def audiences(request):
    #audiences = Audience.objects.annotate(nr_contacts=Count('contact'))
    user = CustomUser.objects.get(id= request.user.id)
    audiences=Audience.objects.filter(user=user)
    return render(request, 'contacts/audiences.html',{'audiences':audiences})

@login_required
def emailForm(request):
    if request.method == "POST": 
        
        now = datetime.now().strftime("%d%m%Y%H%M")
        tinymce = request.POST.get('tinymce')
        filepath='contacts/templates/emails/{}.html'.format(now)
        dbfilepath = filepath.split('templates/')[1]
        f = open(filepath,'w')
        f.write(tinymce)
        f.close()

        email = EmailTemplate.objects.create(path = dbfilepath)
        email.save()
        id = email.id

    return JsonResponse({"email_id":id})

@login_required
def csv_import(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        audience_id = request.POST.get('aud')
        audience = Audience.objects.get(id=audience_id)
        user = CustomUser.objects.get(id= request.user.id)

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "Please import a csv file!")

    data = csv_file.read().decode('UTF-8')
    io_str = io.StringIO(data)
    next(io_str)
    for column in csv.reader(io_str):
        _, created = Contact.objects.update_or_create(
        first_name = column[0],
        last_name = column[1],
        email = column[2],           
        audience = audience,
        user = user
        )
    return redirect('/audience/'+audience_id)


@login_required
def sendEmail(request, pk):
    campaign = Campaign.objects.get(id=pk)
    audience_id = campaign.audience_id
    temp_id = campaign.template_id
    contacts = Contact.objects.filter(audience_id=audience_id)
    template = EmailTemplate.objects.get(id = temp_id)
    
    campaign.status = "ONGOING"
    for contact in contacts:
        ctx={
            'name':contact.first_name,
            'lname':contact.last_name,
            'email':contact.email,
        }
        message = render_to_string(template.path, ctx)
        msg = EmailMessage(campaign.subject,
        message,
        'marketing@procedo-consulting.com',
        [contact.email]
        )
        msg.content_subtype = 'html'
        msg.send()
    campaign.status = "STOPPED"    
    return JsonResponse({"message": "campaign sent"})


class AudienceDeleteView(BSModalDeleteView):
    model = Audience
    template_name = 'contacts/confirm_delete.html'
    success_message = "Audience deleted successfully"
    success_url = reverse_lazy('audiences')

@login_required
def createCampaign(request):
    audiences = Audience.objects.all()
    user = CustomUser.objects.get(id = request.user.id)
    if request.method=="POST":
        audience_id = request.POST.get("audience")
        title = request.POST.get("title")
        fro = request.POST.get("from")
        subject = request.POST.get("subject")
        email_id = request.POST.get("mail")

        email= EmailTemplate.objects.get(id=email_id)
        audience =Audience.objects.get(id=audience_id)
        
        campaign = Campaign.objects.create(title=title,audience=audience, subject =subject, template=email,user=user)

    return render(request, 'contacts/create_campaign.html',{'audiences':audiences})

class CampaignListView(LoginRequiredMixin,ListView):
    model = Campaign
    template_name = 'contacts/campaigns.html'
    context_object_name = 'campaigns'

    def get_queryset(self) :
        user = self.request.user
        campaigns = Campaign.objects.filter(user=user)
        return campaigns


class SearchResult(ListView):
    model= Contact
    template_name="contacts/search.html"
    context_object_name = 'contacts_list'

    def get_queryset(self) :
        query= self.request.GET.get("query")
        contacts_list = Contact.objects.filter(
            Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)
        )
        print(contacts_list)
        return contacts_list


def create_account(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("form valid")
            return redirect("contact_list")
        
    else :
        form = CustomUserCreationForm()

    return render(request, 'contacts/create_account.html',{'form':form})

class LoginView(LoginView):
    template_name  = "contacts/login.html"