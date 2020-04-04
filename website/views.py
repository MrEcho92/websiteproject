from django.shortcuts import render
from django.views.generic import (TemplateView,
                                    FormView,
                                    ListView,
                                    DetailView, )
from django.core.mail import send_mail
from website.models import Post
#from django.conf import settings
from .forms import ContactForm
from django.core.paginator import Paginator

# Create your views here.

class HomePageView(TemplateView):
    template_name ='index.html'

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class AboutPage(TemplateView):
    template_name ='about.html'

class TestimonialPage(TemplateView):
    template_name ='testimonials.html'

class FAQPage(TemplateView):
    template_name ='faq.html'

class GalleryPost(TemplateView):
    template_name = 'gallery-portfolio.html'

class ContactFormView(FormView):
    template_name='contact.html'
    form_class = ContactForm
    success_url = 'contact.html'

    def form_valid(self, form):
        message="{name}/ {email} said: ".format(
        name=form.cleaned_data.get('name'),
        email=form.cleaned_data.get('email')
        )
        message+="\n\n{0}".format(form.cleaned_data.get('message'))

        send_mail(
        subject=form.cleaned_data.get('subject').strip(),
        message=message,
        from_email='contact@eugeneauto.com',
        #recipient_list=[settings.LIST_OF_EMAIL_RECEIPIENTS],
        )
        return super(ContactFormView, self).form_valid(form)


class BlogPostList(ListView):
    model = Post
    template_name = 'blog_list.html'
    paginate_by = 10
    post = Post.objects.filter(status=1).order_by('-created_on')

def listing(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10) # Show 10 blogs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'page_obj': page_obj})

class BlogPostDetail(DetailView):
    model = Post
    template_name = 'blog_detail.html'
