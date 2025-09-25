from django.shortcuts import render, redirect
from app.API_Integration import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.mail import send_mail,EmailMultiAlternatives
from policyBear import settings
from django.core.paginator import Paginator
from math import ceil
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
# Image Upload CkEditor
import uuid
from PIL import Image
from django.http import JsonResponse, HttpResponseBadRequest, Http404, FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
emailRisiveFromWeb="akash.rayadvertising@gmail.com"
# Create your views here.


def send_email(subject_name,recipient_email,message):
    subject = subject_name
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = recipient_email
    mseg=EmailMultiAlternatives( subject, message, email_from, recipient_list )
    mseg.content_subtype="html"
    mseg.send()

def index(request):
    faq=Frequently_Asked_Question.objects.all()
    sendvar={
        'faq':faq
    }
    return render(request, 'index.html',sendvar)

def affordable_health_insurance(request):
    faq=Frequently_Asked_Question.objects.all()
    sendvar={
        'faq':faq
    }
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
                    if 'molina' in str(r['issuer_name'].lower()):
                        FinalResult=r
                        sendvar={
                            'responce':FinalResult
                        }
                        return render(request, 'aca_health.html',sendvar)
                    if str(Offer) in str(r['name']):
                        bar=r
                        bar['carrier']=str(Offer)
                        Get_Filtered_Data.append(bar)
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
            sendvar={
                'responce':offers_list
            }
            return render(request, 'aca_health.html',sendvar)
        try:
            all_carriers_by_name = {carrier.carrier: carrier for carrier in Carrier.objects.all()}
            all_states_by_name = {state.state: state for state in State.objects.all()}
        except Exception as e:
            return render(request, 'aca_health.html')

        for i in Get_Filtered_Data:
            try:
                carrier_obj = all_carriers_by_name.get(i.get('carrier'))
                state_obj = all_states_by_name.get(i.get('state'))
                GetConfirmation=Our_Partner_And_Location.objects.get(Carrier=carrier_obj,State=state_obj)
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
                return render(request, 'aca_health.html')
                # if FinalResult:
                #     return Response(FinalResult)
                # else:
                #     return Response(Result[0])
        if FinalResult:
            items_to_remove = ['id','name',"pediatric_ehb_premium","aptc_eligible_premium","metal_level","state","issuer_name","deductibles"]
            for item_key in items_to_remove:
                if item_key in FinalResult:
                    FinalResult.pop(item_key)
            sendvar={
                'responce':FinalResult
            }
            return render(request, 'aca_health.html',sendvar)
        else:
            items_to_remove = ['id','name',"pediatric_ehb_premium","aptc_eligible_premium","metal_level","state","issuer_name","deductibles"]
            for item_key in items_to_remove:
                if item_key in Result[0]:
                    Result[0].pop(item_key)
            sendvar={
                'responce':Result[0]
            }
            return render(request, 'aca_health.html',sendvar)
    return render(request, 'aca_health.html',sendvar)
    
def supplement_insurance(request):
    faq=Frequently_Asked_Question.objects.all()
    sendvar={
        'faq':faq
    }
    if request.method == "POST":
        sendvar={
            'responce':'success'
        }
        return render(request, 'supplement_insurance.html',sendvar)
    return render(request, 'supplement_insurance.html',sendvar)

def about_us(request):
    
    return render(request, 'about_us.html')

def contact_us(request):
    if request.method=="POST":
        Name=request.POST.get("FirstName")+" "+request.POST.get("LastName")
        Phone=request.POST.get("phone")
        Email=request.POST.get("email")
        Message=request.POST.get("message")
        Subject=f"{Name} trying to reach us from the website"
        MessageBody=f"<strong>Phone:&nbsp;</strong>{Phone}<br><strong>Email:&nbsp;</strong>{Email}<p>{Message}</p>"
        recipient_email=[emailRisiveFromWeb]
        send_email(Subject,recipient_email,MessageBody)
        sendvar={
            'success':'success,'
        }
        return render(request,"contact.html",sendvar)
    return render(request, 'contact.html')

def resources(request):
    allBlog=Blog.objects.filter(Visibility="published").order_by('-id')
    pagination=Paginator(allBlog,9)
    pageNumber=request.GET.get('page')
    pageObject=pagination.get_page(pageNumber)
    sendvar={
        "allBlog":pageObject,
        'totalpage':range(1,pagination.num_pages+1)
    }
    return render(request, 'blog.html',sendvar)

def resourcesdtails(request,slug):
    allBlog=Blog.objects.get(slug=slug)
    resentPost = Blog.objects.filter(Visibility="published").order_by('-id')[:9]
    domain = request.get_host()
    canonical_url = f"http://{domain}/{allBlog.slug}/"
    resentPost
    sendvar={
        "allBlog":allBlog,
        'domain':domain,
        'canonical_url':canonical_url,
        'resentPost':resentPost,
        'resentPostLent':len(resentPost)
    }
    return render(request, 'blogDetails.html',sendvar)

@login_required
def privew_blog(request,slug):
    allBlog=Blog.objects.get(slug=slug)
    domain = request.get_host()
    canonical_url = f"http://{domain}/{allBlog.slug}/"
    sendvar={
        "allBlog":allBlog,
        'domain':domain,
        'canonical_url':canonical_url,
    }
    return render(request, 'blogDetails.html',sendvar)



def career(request):
    career=JobPost.objects.all()
    sendvar={
        'career':career
    }
    return render(request, 'career.html',sendvar)
def careerdtails(request,id):
    career=JobPost.objects.get(id=id)
    sendvar={
        'career':career
    }
    return render(request, 'careerdtails.html',sendvar)

def careersubmitdtails(request,id):
    career=JobPost.objects.get(id=id)
    sendvar={
        'career':career
    }
    if request.method == "POST":
        titel=career.Titel
        name=request.POST.get('fullname')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        cv=request.FILES['cvfile']
        coverlatter=request.POST.get('CoverLetter')
        fm=AppliedCandidates(Position=titel,Full_Name=name,Phone=phone,Email=email,CV=cv,Cover_Letter=coverlatter)
        fm.save()

        getcv=AppliedCandidates.objects.filter(Phone=phone)
        if len(getcv) > 1:
            renamecv=AppliedCandidates.objects.filter(Phone=phone)[0].CV
        else:
            renamecv=AppliedCandidates.objects.get(Phone=phone).CV

        Subject=f"{name} Applied for {titel} in our company"
        MessageBody=f"<p>{coverlatter}</p><p>{name}</p><p>{phone}</p><p>{email}</p><p><strong>CV Link:</strong>https://policybear.com/media/media/CandidatesCV/{renamecv}</p>"
        recipient_email=[emailRisiveFromWeb]
        send_email(Subject,recipient_email,MessageBody)
        return redirect("career")
    return render(request, 'careersubmitdtails.html',sendvar)

def PrivacyPolicy(request):
    getPrivacyPolicy=Privacy_Policy.objects.last()
    sendvar={
        'getPrivacyPolicy':getPrivacyPolicy
    }
    return render(request, 'PrivacyPolicy.html',sendvar)

def TermsofService(request):
    getPrivacyPolicy=Terms_of_Service.objects.last()
    sendvar={
        'getPrivacyPolicy':getPrivacyPolicy
    }
    return render(request, 'TermsofService.html',sendvar)

def accessibility(request):
    getPrivacyPolicy=Accessibility.objects.last()
    sendvar={
        'getPrivacyPolicy':getPrivacyPolicy
    }
    return render(request, 'accessibility.html',sendvar)

def disclaimer(request):
    getPrivacyPolicy=Disclaimer.objects.last()
    sendvar={
        'getPrivacyPolicy':getPrivacyPolicy
    }
    return render(request, 'disclaimer.html',sendvar)

def download_document(request,filename):
    print(filename)
    # This is a basic example; for security, you should use a model to validate filenames.
    file_path = os.path.join(settings.MEDIA_ROOT, 'documents', filename)

    if not os.path.isfile(file_path):
        raise Http404("File not found.")
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@csrf_exempt
def ckeditor_upload_to_webp(request):
    """
    This function is the "special function" that handles the image upload.
    It takes an image, converts it to WebP, and saves it.
    """
    if request.method != 'POST' or 'upload' not in request.FILES:
        return HttpResponseBadRequest('Invalid request')

    uploaded_file = request.FILES['upload']
    
    # 1. Open the image file that CKEditor sent.
    try:
        img = Image.open(uploaded_file)
    except Exception:
        return JsonResponse({
            "uploaded": 0,
            "error": {"message": "Invalid image file."}
        })
        
    # 2. Create a unique name for the new WebP file.
    unique_filename = f"{uuid.uuid4()}.webp"
    
    # 3. Define the path where the file will be saved.
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'ckeditor', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, unique_filename)
    
    # 4. Convert and save the image as a WebP file.
    img.save(save_path, 'webp', quality=85)
    
    # 5. Get the public URL for the newly saved WebP file.
    image_url = os.path.join(settings.MEDIA_URL, 'ckeditor', 'uploads', unique_filename)
    
    # 6. Send the new WebP URL back to CKEditor so it can display it.
    response_data = {
        "uploaded": 1,
        "fileName": unique_filename,
        "url": image_url.replace(os.sep, '/') 
    }
    return JsonResponse(response_data)



# ========================>>>>>>>>>>>
# Chat Bot With ChatGPT======>>>>>>>>
# ========================>>>>>>>>>>>

from .utils import (
    load_faqs,
    build_corpus,
    Embedder,
    SearchIndex,
    BOT_NAME,
    BOT_TONE,
    CONFIDENCE_THRESHOLD,
    TOP_K,
)

# Load env (.env next to manage.py)
load_dotenv()

# ---- Prepare FAQ + embeddings once ----
APP_DIR = os.path.dirname(__file__)
FAQS_PATH = os.path.join(APP_DIR, "faqs.json")
faqs = load_faqs(FAQS_PATH)
embedder = Embedder()
corpus = build_corpus(faqs)
faq_emb = embedder.encode(corpus)
bot_index = SearchIndex(faq_emb)

# ---- OpenAI setup ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ON = False
client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        OPENAI_ON = True
    except Exception:
        OPENAI_ON = False

def _best_match(user_q: str):
    q_vec = embedder.encode([user_q])[0]
    idxs, scores = bot_index.query(q_vec, top_k=TOP_K)
    top_idx, top_score = idxs[0], float(scores[0])
    return faqs[top_idx], top_score, idxs, scores

@api_view(['POST'])
def ask(request):
    user_q = (request.data.get("q") or request.data.get("q") or "").strip()
    if not user_q:
        return JsonResponse({"answer": "Please enter a question."})

    faq, score, idxs, scores = _best_match(user_q)

    # If confident match → preset answer
    if score >= CONFIDENCE_THRESHOLD:
        return JsonResponse(
            {"answer": f"{faq.a}\n\n— (Policy-Bear AI)"}
        )

    # If GPT not configured
    if not OPENAI_ON:
        return JsonResponse({
            "answer": "AI fallback is not configured. Set OPENAI_API_KEY in your .env and restart the server."
        })

    # GPT fallback with FAQ grounding
    context = []
    for i, s in zip(idxs, scores):
        context.append(f"Q: {faqs[i].q}\nA: {faqs[i].a}\n(confidence {float(s):.2f})")
    ground = "\n\n".join(context)
    system = (
        f"You are {BOT_NAME}. {BOT_TONE} "
        "Prefer the FAQ context where relevant. If unsure, ask a brief clarifying question."
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"User question: {user_q}\n\nFAQ context:\n{ground}"},
            ],
        )
        answer = resp.choices[0].message.content.strip()
        return JsonResponse({"answer": answer + "\n\n— (Policy-Bear AI)"})
    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({
            "answer": f"AI fallback error: {e}. Check model name, billing/quota, or network proxy."
        })


def health(request):
    return JsonResponse({"openai_ready": OPENAI_ON})

def diag(request):
    # Simple status check
    return JsonResponse({"openai_ready": OPENAI_ON, "has_key": bool(os.getenv("OPENAI_API_KEY"))})

def gpt_echo(request):
    # Direct GPT call (bypasses FAQ logic) to confirm Django->OpenAI works
    if not OPENAI_ON:
        return JsonResponse({"answer": "No OPENAI_API_KEY loaded."})
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a health check."},
                {"role": "user", "content": "Reply with the word READY only."}
            ],
        )
        return JsonResponse({"answer": resp.choices[0].message.content.strip(), "ok": True})
    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({"answer": f"GPT error: {e}", "ok": False})

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
                if 'molina' in str(r['issuer_name'].lower()):
                    FinalResult=r
                    return Response(FinalResult)
                if str(Offer) in str(r['name']):
                    bar=r
                    bar['carrier']=str(Offer)
                    Get_Filtered_Data.append(bar)
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
    try:
        all_carriers_by_name = {carrier.carrier: carrier for carrier in Carrier.objects.all()}
        all_states_by_name = {state.state: state for state in State.objects.all()}
    except Exception as e:
        return Response({"error": f"Failed to pre-load Carrier or State data: {e}"}, status=500)

    for i in Get_Filtered_Data:
        try:
            carrier_obj = all_carriers_by_name.get(i.get('carrier'))
            state_obj = all_states_by_name.get(i.get('state'))
            GetConfirmation=Our_Partner_And_Location.objects.get(Carrier=carrier_obj,State=state_obj)
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
        items_to_remove = ['id','name',"pediatric_ehb_premium","aptc_eligible_premium","metal_level","state","issuer_name","deductibles"]
        for item_key in items_to_remove:
            if item_key in FinalResult:
                FinalResult.pop(item_key)
        return Response(FinalResult)
    else:
        items_to_remove = ['id','name',"pediatric_ehb_premium","aptc_eligible_premium","metal_level","state","issuer_name","deductibles"]
        for item_key in items_to_remove:
            if item_key in Result[0]:
                Result[0].pop(item_key)
        return Response(Result[0])
