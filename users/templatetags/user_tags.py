from django import template
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.utils import render_crispy_form
# from allauth.account.forms import LoginForm  # REMOVE IMPORT FROM HERE

register = template.Library()

@register.simple_tag(takes_context=True)
def crispy_login_form(context):
    from allauth.account.forms import LoginForm  # Import LoginForm HERE
    form = LoginForm(context['request'].POST or None) # Get POST data from context
    form.helper = FormHelper()
    form.helper.form_method = 'post'
    form.helper.form_show_errors = True # Ensure form errors are rendered.
    form.helper.form_tag = False  # Remove outer <form> tag
    # Return the crispy form rendering
    return render_crispy_form(form, context=context) 

@register.simple_tag(takes_context=True)  # Removed the render_crispy_form in this function
def crispy_signup_form(context): # No more rendering in the tag
    form = context.get('form') # Get form from template context!
    if form: # form might not be present in all contexts
        form.helper = FormHelper()
        form.helper.form_method = 'post'
        form.helper.form_show_errors = True
        form.helper.form_tag = False  # <--- It should render the tags itself!
    return render_crispy_form(form, context=context) 


@register.simple_tag(takes_context=True)
def crispy_password_reset_form(context):
    from allauth.account.forms import ResetPasswordForm  
    form = ResetPasswordForm(context['request'].POST or None)
    form.helper = FormHelper()
    form.helper.form_method = 'post'
    form.helper.form_show_errors = True
    form.helper.form_tag = False
    from crispy_forms.utils import render_crispy_form
    return render_crispy_form(form, context=context)

