from django.contrib import admin
from django.urls import path
from .views import AboutPage, ContactFormView, BlogPostList, BlogPostDetail, FAQPage, TestimonialPage, GalleryPost
from . import views


app_name = 'website'

urlpatterns = [
    path('about/', AboutPage.as_view(), name='about'),
    path('testimonials/', TestimonialPage.as_view(), name="testimonials"),
    path('faq/', FAQPage.as_view(), name="faq"),
    path('gallery/', GalleryPost.as_view(), name='gallery-portfolio'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('bloglist/', BlogPostList.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogPostDetail.as_view(), name='blog_detail'),


]
