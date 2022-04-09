from django import views
from django.urls import path
from contacts.views import *
from django.contrib.auth.views import LogoutView    


urlpatterns = [
    path('', ContactsListview.as_view(), name="contact_list" ),
    path('contact-detail/<int:pk>/', ContactDetailView.as_view(), name="contact_detail"),
    path('update-contact/<int:pk>/', UpdateContact.as_view(), name='update_contact'),
    path('audience/<int:pk>/', audience, name="audience"),
    path('audiences/', audiences, name="audiences"),
    path('form/', emailForm, name="email_form"),
    path('import/', csv_import, name="import_contacts"),
    path('send/<int:pk>/<int:pr>/', sendEmail, name="send"),
    path('delete/<int:pk>/', AudienceDeleteView.as_view(), name="delete_audience"),
    path('create_campaign/', createCampaign, name="create_campaign"),
    path('campaigns/', CampaignListView.as_view(), name="campaigns"),
    path('send/<int:pk>/', sendEmail, name="send_campaign"),
    path('search/', SearchResult.as_view(),name="search_results"),
    path('signup/', create_account, name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    


]
