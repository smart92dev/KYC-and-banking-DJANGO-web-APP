from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages

# Create your views here.
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "Please submit your KYC")
            return redirect("account:kyc-reg")

        account=Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to log in in order to access the dashboard")
        return redirect("userauths:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
    }
    return render(request, "account/account.html", context)

def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        kyc = None

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC Form submitted successfully. Review pending.")
            return redirect("core:index")
    else:
        form = KYCForm(instance=kyc)

    context = {
        "account": account,
        "form": form,
    }
    return render(request, "account/kyc-form.html", context)
