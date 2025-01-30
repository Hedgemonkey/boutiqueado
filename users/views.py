from allauth.account.views import LoginView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from allauth.account.adapter import get_adapter
from allauth.account.utils import perform_login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from allauth.account.forms import LoginForm

class MyLoginView(LoginView):
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        form_class = kwargs.get('form_class', LoginForm)  # Default to LoginForm
        # Remove the 'form' kwarg if present:
        if 'form' in kwargs:
            kwargs.pop('form') # removes the form kwarg.
        form_kwargs = kwargs.get('form_kwargs', {}) # Use kwargs if provided otherwise empty dict.

        # Pass the form instance as the *first positional argument*:
        form = form_class(self.request.POST or None, **form_kwargs)

        if form:
            form.helper = FormHelper()
            form.helper.form_method = 'post'
            form.helper.form_tag = False
            form.helper.form_action = reverse('account_login')
            form.helper.layout = Layout(
                Field('login'),  # Or username, email - check your allauth setup
                Field('password'),
                Submit('submit', _('Sign In'), css_class='btn-primary')
            )
            kwargs['form'] = form # updates the kwargs
        return kwargs

    def form_valid(self, form):
        success_url = self.get_success_url()
        response = perform_login(self.request, form.user, email_verification=self.adapter.get_email_verification_setting(self.request))
        get_adapter(self.request).add_message(self.request,
                                            messages.SUCCESS,
                                            'account/messages/login_successful.txt',
                                            {'user': form.user})
        return redirect(success_url or response)


    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        redirect_field_name = get_adapter(self.request).redirect_field_name(self.request)
        ret[redirect_field_name] = self.request.POST.get(redirect_field_name,
                                                        self.request.GET.get(redirect_field_name, ''))
        form = ret.get('form', None)
        if form:
            form.fields[redirect_field_name].initial = ret[redirect_field_name]
        ret['redirect_field_value'] = ret[redirect_field_name]
        ret['redirect_field_name'] = redirect_field_name
        return ret
