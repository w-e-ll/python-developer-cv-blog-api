from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.views import generic


class ContactView(generic.TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['form'].is_valid():
            cd = context['form'].cleaned_data
            name = cd['name']
            phone = cd['phone']
            company = cd['company']
            subject = cd['subject']
            from_email = cd['email']
            message = cd['message']

            try:
                send_mail(
                    subject + " from {}".format(from_email),
                    "\nNAME: {}, \nPHONE: {}, \nCOMPANY: {}, \nSUBJECT: {}, \nMESSAGE: {}".format(name, phone, company, subject, message),
                    from_email,
                    [settings.EMAIL_HOST_USER]
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contacts/thankyou/')

        return super(generic.TemplateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        form = ContactForm(self.request.POST or None)
        context['form'] = form
        return context


def thankyou(request):
    return render_to_response('thankyou.html')
