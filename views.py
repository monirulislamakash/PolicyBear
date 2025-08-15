from django.shortcuts import render
from app.API_Integration import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def affordable_health_insurance(request):
    if request.method=="POST":
        get_Zip = request.POST.get("zip")
        get_income = int(request.POST.get("income"))
        get_age = int(request.POST.get("age"))
        get_gender = request.POST.get("gender")

        county_fips, state_abbr = get_county_fips_with_state(get_Zip)
        Result=get_Offer_details(get_Zip,county_fips,state_abbr,get_income,get_age,get_gender)
        OurAllOffer=Carrier.objects.all()
        Get_Filtered_Data=[]
        FinalResult={}
        try:
            for Offer in OurAllOffer:
                for r in Result:
                    if str(Offer) in str(r['name']):
                        bar=r
                        bar['carrier']=str(Offer)
                        Get_Filtered_Data.append(bar)
        except:
                import random
                choice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                # print()
                GetTheSecondaryOffer=SecondaryOffer.objects.filter(AgeFrom__lte=int(get_age),AgeTo__gte=int(get_age))[random.choice(choice)]
                # GetTheSecondaryOffer=SecondaryOffer.objects.last().AgeFrom
                print(GetTheSecondaryOffer,'=================>>>>>>>>>>')
                return render(request, 'aca_health.html')
        for i in Get_Filtered_Data:
            try:
                GetConfirmation=Our_Partner_And_Location.objects.get(Carrier=Carrier.objects.get(carrier=i['carrier']),State=State.objects.get(state=i['state']))
                if GetConfirmation:
                    if bool(FinalResult)==False:
                        barTow=i
                        barTow['Payout']=str(GetConfirmation.Payout) 
                        FinalResult=barTow
                    else:
                        if FinalResult['Payout'] < GetConfirmation.Payout:
                            barTow=i
                            barTow['Payout']=str(GetConfirmation.Payout) 
                            FinalResult=barTow
            except:
                sendvar={
                    "error":"something is wrong try again"
                }
                return render(request, 'aca_health.html',sendvar)
       
        if FinalResult:
            sendvar={
                'responce':FinalResult
            }
            return render(request, 'aca_health.html',sendvar)
        else:
            sendvar={
                'responce':Result[0]
            }
            return render(request, 'aca_health.html',sendvar)
    return render(request, 'aca_health.html')
    

def supplement_insurance(request):
    
    return render(request, 'supplement_insurance.html')


# ========================>>>>>>>>>>>
#   API For AI Agent======>>>>>>>>>>>
# ========================>>>>>>>>>>>
@api_view(['POST'])
def api_for_ai_agent(request):
    get_Zip = request.data.get("zip")
    get_income = request.data.get("income")
    get_age = request.data.get("age")
    get_gender = request.data.get("gender")
    
    county_fips, state_abbr = get_county_fips_with_state(get_Zip)
    
    Result=get_Offer_details(get_Zip,county_fips,state_abbr,get_income,get_age,get_gender)
    OurAllOffer=Carrier.objects.all()
    Get_Filtered_Data=[]
    
    FinalResult={}
    try:
        for Offer in OurAllOffer:
            for r in Result:
                print(r['name'],"========>>>>>")
                if 'molina' in str(r['issuer_name'].lower()):
                    FinalResult=r
                    return Response(FinalResult)
                if str(Offer) in str(r['name']):
                    bar=r
                    bar['carrier']=str(Offer)
                    Get_Filtered_Data.append(bar)
        # print(Get_Filtered_Data,"======================>>>>>>>>")
    except:
        import random
        choice = []
        counter=0
        GetTheSecondaryOffer=SecondaryOffer.objects.filter(AgeFrom__lte=int(get_age),AgeTo__gte=int(get_age))
        for i in GetTheSecondaryOffer:
            choice.append(counter)
            counter+=1
        GetTheSecondaryOffer=SecondaryOffer.objects.filter(AgeFrom__lte=int(get_age),AgeTo__gte=int(get_age))[random.choice(choice)]
        offers_list = {'name': str(GetTheSecondaryOffer.PolicyPlan),'carrier': str(GetTheSecondaryOffer.Carrier)}
        return Response(offers_list)
    for i in Get_Filtered_Data:
        try:
            GetConfirmation=Our_Partner_And_Location.objects.get(Carrier=Carrier.objects.get(carrier=i['carrier']),State=State.objects.get(state=i['state']))
            if GetConfirmation:
                if bool(FinalResult)==False:
                    barTow=i
                    barTow['Payout']=str(GetConfirmation.Payout)
                    FinalResult=barTow
                else:
                    if int(FinalResult['Payout']) < int(GetConfirmation.Payout):
                        barTow=i
                        barTow['Payout']=str(GetConfirmation.Payout) 
                        FinalResult=barTow
            
        except Exception as e:
            return Response({"error":f"something is wrong try again {e}"})
            # if FinalResult:
            #     return Response(FinalResult)
            # else:
            #     return Response(Result[0])
    if FinalResult:
        return Response(FinalResult)
    else:
        return Response(Result[0])
