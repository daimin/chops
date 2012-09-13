"""
"""
from django.shortcuts import render_to_response
 
def PageWithJquery( request ):
    return render_to_response( 'default.html',
            {"mytitle":"customize_title"})