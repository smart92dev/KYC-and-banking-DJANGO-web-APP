from django.shortcuts import render,redirect
from account.models import Account
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Transaction
@login_required
def search_users_account_number(request):
    #account = Account.objects.filter(account_status="active")
    account=Account.objects.all()
    query=request.POST.get("account_number")

    if query:
        account=account.filter(
            Q(account_number=query) |
            Q(account_id=query)
        ).distinct()


    context = {
        "account":account,
        "query":query,
    }

    return render (request, "transfer/search-user-by-account-number.html", context)


def AmountTransfer(request, account_number):
    try:
        account=Account.objects.get(account_number)
    except:
        messages.warning(request,"Account Does not exist")
        return redirect("core:search-account")
    context={
        "account":account,
    }

    return render(request,"transfer/amount-transfer.html")

def AmountTransferProcess(request,account_number):
    account = Account.objects.get(account_number=account_number)
    sender=request.user
    receiver=account.user

    sender_account=request.user.account
    receiver_account=account

    if request.method == "POST":
        amount=request.POST.get("amount")
        description = request.POST.get("description")

        if sender_account.account_balance>0 and amount:
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                receiver=receiver,
                sender_account=sender_account,
                status="processing",
                transaction_type="transfer",
            )
            new_transaction.save()

            transaction_id=new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number,transaction_id)
        else:
             messages.warning(request,"Insufficient funds.")
             return redirect("core:amount-transfer",account.account_number)
    else:
        messages.warning(request,"Error. Try again later.")
        return redirect("account:account")

def TransferConfirmation(request,account_number,transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction= Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request,"Error.Transaction does not exst.")
        return redirect ("account:account")
    context = {
        "account":account,
        "transaction":transaction
    }

    return render(request,"transfer/transfer-confirmation.html",context)



