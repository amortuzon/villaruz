from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from .models import *
from django import forms
from django.forms import CheckboxSelectMultiple
from .forms import TermsRecaptchaForm, ReviewsForm, ReservationForm, MessageFormUpdate, \
    CreateUserForm, ReservationUpdateForm, ReservationUpdateFormAdmin, CustomerForm, MessageForm, SetPasswordForm, \
    PasswordResetForm
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from . decorators import unauthenticated_user, allowed_users, admin_only
from datetime import date, time
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.db.models.query_utils import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.safestring import mark_safe


# Create your views here.
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, "Thank you for activating your account. You can now login your account!")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("shop/user/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            mark_safe(
                f"Dear <strong>{user}</strong>, please go to your email account <strong>{to_email}</strong> and click the received activation link to confirm and complete the registration. Check your spam folder."
            ),
        )
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                name=username,
                email=email,
            )
            messages.success(
                request, 'Account Created Successfully for ' + username + '! Read the Terms and Conditions and click agree to continue. Thank you!')

            return redirect('terms')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    context = {'form': form}
    return render(request, 'shop/register.html', context)


@unauthenticated_user
def termsPage(request):
    if request.method == 'POST':
        form = TermsRecaptchaForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'You need to verify first your email account. Go to your email and click the link to login!')
            return redirect('login')

        else:
            messages.error(
                request, 'Please check the reCAPTCHA to confirm you are not a robot.')
    else:
        form = TermsRecaptchaForm()

    context = {'captcha': form}
    return render(request, 'shop/user/terms.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('/')
            else:
                try:
                    user.customer
                    login(request, user)
                    return redirect('dashboard')
                except Customer.DoesNotExist:
                    messages.info(
                        request, 'You are not a Customer yet, please register as a customer.')
        else:
            messages.info(
                request, 'Username or password is incorrect. If new user, you have to verify your account in your email address.')

    context = {}
    return render(request, 'shop/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def indexPage(request):
    return render(request, 'shop/index.html')


@login_required(login_url='login')
@admin_only
def dashboardPage(request):
    reservation = Shop.objects.all()

    jan_res = Shop.objects.filter(created__month=1).count()
    feb_res = Shop.objects.filter(created__month=2).count()
    mar_res = Shop.objects.filter(created__month=3).count()
    apr_res = Shop.objects.filter(created__month=4).count()
    may_res = Shop.objects.filter(created__month=5).count()
    jun_res = Shop.objects.filter(created__month=6).count()
    jul_res = Shop.objects.filter(created__month=7).count()
    aug_res = Shop.objects.filter(created__month=8).count()
    sep_res = Shop.objects.filter(created__month=9).count()
    oct_res = Shop.objects.filter(created__month=10).count()
    nov_res = Shop.objects.filter(created__month=11).count()
    dec_res = Shop.objects.filter(created__month=12).count()

    new_reservation = reservation.filter(status='New').count()
    approved_reservation = reservation.filter(status='Approved').count()
    completed = reservation.filter(status='Completed').count()

    context = {'reservation': reservation, 'new_reservation': new_reservation,
               'approved_reservation': approved_reservation, 'completed': completed,
               'jan_res': jan_res, 'feb_res': feb_res, 'mar_res': mar_res, 'apr_res': apr_res,
               'may_res': may_res, 'jun_res': jun_res, 'jul_res': jul_res, 'aug_res': aug_res,
               'sep_res': sep_res, 'oct_res': oct_res, 'nov_res': nov_res, 'dec_res': dec_res}
    return render(request, 'shop/admin/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    reservations = request.user.customer.shop_set.all()

    jan_res = Shop.objects.filter(created__month=1).count()
    feb_res = Shop.objects.filter(created__month=2).count()
    mar_res = Shop.objects.filter(created__month=3).count()
    apr_res = Shop.objects.filter(created__month=4).count()
    may_res = Shop.objects.filter(created__month=5).count()
    jun_res = Shop.objects.filter(created__month=6).count()
    jul_res = Shop.objects.filter(created__month=7).count()
    aug_res = Shop.objects.filter(created__month=8).count()
    sep_res = Shop.objects.filter(created__month=9).count()
    oct_res = Shop.objects.filter(created__month=10).count()
    nov_res = Shop.objects.filter(created__month=11).count()
    dec_res = Shop.objects.filter(created__month=12).count()

    new_reservation = reservations.filter(status='New').count()
    approved_reservation = reservations.filter(status='Approved').count()
    completed = reservations.filter(status='Completed').count()

    context = {'reservations': reservations, 'new_reservation': new_reservation,
               'approved_reservation': approved_reservation, 'completed': completed,
               'jan_res': jan_res, 'feb_res': feb_res, 'mar_res': mar_res, 'apr_res': apr_res,
               'may_res': may_res, 'jun_res': jun_res, 'jul_res': jul_res, 'aug_res': aug_res,
               'sep_res': sep_res, 'oct_res': oct_res, 'nov_res': nov_res, 'dec_res': dec_res}
    return render(request, 'shop/user/user_page.html', context)


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


@login_required(login_url='login')
def createReservation(request, pk):
    ReservationForm = inlineformset_factory(
        Customer, Shop, fields=('service', 'date', 'time'),
        extra=1, can_delete=False, widgets={'date': DateInput(attrs={'min': date.today(), 'required': True}),
                                            'time': TimeInput(format='%H:%M', attrs={'min': '09:00', 'max': '17:00', 'required': True}),
                                            'service': CheckboxSelectMultiple()})
    customer = Customer.objects.get(id=pk)
    formset = ReservationForm(
        queryset=Shop.objects.none(), instance=customer)
    services = Service.objects.all()  # retrieve all services
    if request.method == 'POST':
        formset = ReservationForm(request.POST, instance=customer)
        if formset.is_valid():
            print(formset.errors)
            formset.save()
            messages.success(request, 'Reservation Created!')
            return redirect('user_page')
        else:
            messages.error(request, 'Error creating reservation')
    # add services to the context
    context = {'formset': formset, 'services': services}
    return render(request, 'shop/user/reservation_form.html', context)


@ login_required(login_url='login')
def updateReservation(request, pk):
    shop = Shop.objects.get(id=pk)
    formset = ReservationUpdateForm(instance=shop)
    if request.method == 'POST':
        formset = ReservationUpdateForm(request.POST, instance=shop)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Reservation Updated Successly!')
            return redirect('reservations')

    context = {'formset': formset}
    return render(request, 'shop/user/reservationupdate_form.html', context)


@ login_required(login_url='login')
def updateReservationAdmin(request, pk):
    shop = Shop.objects.get(id=pk)
    formset = ReservationUpdateFormAdmin(instance=shop)
    if request.method == 'POST':
        formset = ReservationUpdateFormAdmin(request.POST, instance=shop)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Reservation Updated Successly!')
            return redirect('/')

    context = {'formset': formset, 'shop': shop}
    return render(request, 'shop/admin/reservationupdateadmin.html', context)


@ login_required(login_url='login')
def deleteReservation(request, pk):
    reservation = Shop.objects.get(id=pk)
    if request.method == "POST":
        reservation.delete()
        return redirect('reservations')

    context = {'reservation': reservation}
    return render(request, 'shop/user/delete.html', context)


@ login_required(login_url='login')
def deleteReservationAdmin(request, pk):
    reservation = Shop.objects.get(id=pk)
    if request.method == "POST":
        reservation.delete()
        return redirect('/')

    context = {'reservation': reservation}
    return render(request, 'shop/delete.html', context)


@login_required(login_url='login')
def aboutPage(request):

    context = {}
    return render(request, 'shop/user/about.html', context)


@login_required(login_url='login')
def servicesPage(request):

    context = {}
    return render(request, 'shop/user/services.html', context)


@login_required(login_url='login')
def contactPage(request):

    context = {}
    return render(request, 'shop/user/contact.html', context)


@login_required(login_url='login')
def reservationPage(request):
    reservations = request.user.customer.shop_set.all().order_by('-created')

    new_reservation = reservations.filter(status='New').count()
    approved_reservation = reservations.filter(status='Approved').count()
    completed = reservations.filter(status='Completed').count()

    context = {'reservations': reservations, 'new_reservation': new_reservation,
               'approved_reservation': approved_reservation, 'completed': completed}
    return render(request, 'shop/user/reservations.html', context)


@login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def profileSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated!')
            return redirect('profile')

    context = {'form': form}
    return render(request, 'shop/profile.html', context)


def submit_message(request, pk):
    form = MessageForm()
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=customer)
        if form.is_valid():
            data = Comments()
            data.email = form.cleaned_data['email']
            data.message = form.cleaned_data['message']
            data.rating = form.cleaned_data['rating']
            data.customer = customer
            data.save()
            messages.success(request, 'Message submitted successfully')
            return redirect('message_page')

    context = {'form': form, 'customer': customer}
    return render(request, 'shop/user/contact.html', context)


@ login_required(login_url='login')
def updatemessage(request, pk):
    comment = Comments.objects.get(id=pk)
    formset = MessageFormUpdate(instance=comment)
    if request.method == 'POST':
        formset = MessageFormUpdate(request.POST, instance=comment)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Message Updated Successfully!')
            return redirect('message_page')
        else:
            messages.error(request, 'Error updating message')
    context = {'formset': formset, 'comment': comment}
    return render(request, 'shop/user/updatemessage.html', context)


@ login_required(login_url='login')
def messagePage(request):
    comment = request.user.customer.comments_set.all().order_by('-created_date')

    context = {'comment': comment}
    return render(request, 'shop/user/messages.html', context)


@ login_required(login_url='login')
def allmessagePage(request):
    messages = Comments.objects.all()

    context = {'messages': messages}
    return render(request, 'shop/admin/allmessage.html', context)


@ login_required(login_url='login')
def allCustomers(request):
    customer = Customer.objects.all()

    context = {'customer': customer}
    return render(request, 'shop/admin/customer.html', context)


@ login_required(login_url='login')
def deletemessageAdmin(request, pk):
    comments = Comments.objects.get(id=pk)
    if request.method == "POST":
        comments.delete()
        return redirect('allmessage_page')

    context = {'comments': comments}
    return render(request, 'shop/admin/deletemessageadmin.html', context)


@ login_required(login_url='login')
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer')

    context = {'customer': customer}
    return render(request, 'shop/admin/deletecustomer.html', context)


# Change password part
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed!")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'shop/user/password_reset_confirm.html', {'form': form, 'customer': user})


# Reset Password
# @unauthenticated_user
# def password_reset_request(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             user_email = form.cleaned_data['email']
#             associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
#             if associated_user:
#                 subject = "Password Reset request"
#                 message = render_to_string("shop/user/template_reset_password.html", {
#                     'user': associated_user,
#                     'domain': get_current_site(request).domain,
#                     'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
#                     'token': account_activation_token.make_token(associated_user),
#                     'protocol': 'https' if request.is_secure() else 'http'
#                 })
#                 email = EmailMessage(subject, message, to=[
#                                      associated_user.email])
#                 if email.send():
#                     messages.success(request,
#                                      """
#                         <h2>Password reset sent</h2>
#                         <p>
#                             We have emailed you instructions for setting your password, if an account exists with the email you entered.
#                             You should receive them shortly. <br> If you don't receive an email, please make sure you've entered the address
#                             you registered with, and check your spam folder.

#                         </p>
#                         """
#                                      )
#                 else:
#                     messages.error(
#                         request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

#             return redirect('login')

#         for key, error in list(form.errors.items()):
#             if key == 'captcha' and error[0] == 'This field is required.':
#                 messages.error(request, "You must pass the reCATCHA test")
#                 continue

#     form = PasswordResetForm()
#     return render(
#         request=request,
#         template_name="shop/user/password_reset.html",
#         context={"form": form}
#     )


# def passwordResetConfirm(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         if request.method == 'POST':
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 # print(form.cleaned_data)  # Print form data before saving
#                 form.save()
#                 # print(user.password)  # Print new password after saving
#                 messages.success(
#                     request, "Your password has been set. You may go ahead and login now.")
#                 return redirect('login')

#             else:
#                 for error in list(form.errors.values()):
#                     messages.error(request, error)

#         form = SetPasswordForm(user)
#         return render(request, 'shop/user/password_reset_confirm2.html', {'form': form})
#     else:
#         messages.error(request, "Link is expired!")

#     messages.error(
#         request, 'Something went wrong, redirecting back to login page')
#     return redirect("login")


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_users = get_user_model().objects.filter(Q(email=user_email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset request"
                    message = render_to_string("shop/user/template_reset_password.html", {
                        'user': user,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http'
                    })
                    email = EmailMessage(subject, message, to=[user.email])
                    if email.send():
                        messages.success(request,
                                         """
                            <h2>Password reset sent</h2>
                            <p>
                                We have emailed you instructions for setting your password, if an account exists with the email you entered.
                                You should receive them shortly. <br> If you don't receive an email, please make sure you've entered the address
                                you registered with, and check your spam folder.
                            
                            </p>
                            """
                                         )
                    else:
                        messages.error(
                            request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
            else:
                messages.error(
                    request, "No user found with that email address")

            return redirect('login')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCATCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name="shop/user/password_reset.html",
        context={"form": form}
    )


@unauthenticated_user
def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = User.objects.filter(pk=uid)
    except:
        users = None

    if users is not None:
        for user in users:
            if account_activation_token.check_token(user, token):
                if request.method == 'POST':
                    form = SetPasswordForm(user, request.POST)
                    if form.is_valid():
                        form.save()
                    else:
                        for error in list(form.errors.values()):
                            messages.error(request, error)
                else:
                    form = SetPasswordForm(user)
                    return render(request, 'shop/user/password_reset_confirm2.html', {'form': form})
        messages.success(
            request, "Your password has been set. You may go ahead and login now.")
        return redirect('login')
    else:
        messages.error(request, "Link is expired!")

    messages.error(
        request, 'Something went wrong, redirecting back to login page')
    return redirect("login")
