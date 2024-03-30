from .models import Book, SuperAdminUser, SuperAdminUserActivity, User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserLoginserializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserLogin(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserLoginserializer(data=data)
            print(serializer)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = User.objects.filter(email=email).first()
                print('user', user)
                if user and user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'data': serializer.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })

                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Invalid password',
                        'data': {}
                    })
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({
                'status': 400,
                'message': 'somethim went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)


def create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        email = request.POST.get('email')
        describe = request.POST.get('describe')
        obj = Book.objects.create(name=name, author=author, email=email, describe=describe)
        obj.save()
    return 'book created'


@csrf_exempt
class screate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        department = request.POST.get('describe')
        region = request.POST.get('region')
        zone = request.POST.get('zone')
        password = request.POST.get('password')
        obj = SuperAdminUser.objects.create(name=name, password=password, email=email, mobile=mobile,
                                            department=department, region=region,
                                            zone=zone)
        obj.save()

        return Response('super-admin created')


def sacreate(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        url_endpoint = request.POST.get('url_endpoint')
        obj = SuperAdminUserActivity.objects.create(mobile=mobile, url_endpoint=url_endpoint)
        obj.save()

    return 'sauper-admin log'


from .models import User, SuperAdminUserActivity, Book


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        serilizers = UserLoginserializer
        try:
            print(username, password)
            user = User.objects.get(username=username, password=password)
            print(user)
            if user.is_active:
                return JsonResponse({'status': 'success', 'data': serilizers.data})
            else:
                return JsonResponse({'status': 'fail', 'error': 'User is not active'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'error': 'Invalid username or password'})


@csrf_exempt
def get_data(request):
    serilizers = UserLoginserializer
    return serilizers.data


'''
from rest_framework_jwt.settings import api_settings


@csrf_exempt
def log(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
            if user.is_active:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                jwt_token = jwt_encode_handler(payload)
                return JsonResponse({'status': 'success', 'token': jwt_token})
            else:
                return JsonResponse({'status': 'fail', 'error': 'User is not active'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'error': 'Invalid email or password'})


    def get_energy_score(self, customer_obj):
        return 750

    def get_asset_type_count(self, customer_obj):
        asset_type = []
        asset = CustomerAsset.objects.filter(customer=customer_obj)
        for ast in asset:
            if ast.asset_type not in asset_type:
                asset_type.append(asset)
            else:
                pass
        return len(asset_type)

    def get_pnd_datum_order(self, customer_obj):
        try:
            pnd_datum_order = CustomerOrder.objects.filter(customer=customer_obj, status=CustomerOrderModeChoices.PLACED).count()
            return pnd_datum_order
        except:
            return 0

    def get_not_due_amount(self, customer_obj):
        if customer_obj.is_finserv_enabled:
            orders = PartnerOrder.objects.filter(proforma_invoice__customer=customer_obj,
                                                 status__in=[PartnerOrderStatusChoices.DELIVERED],
                                                 agreement__order__isnull=False,
                                                 proforma_invoice__payment__status__in=[PaymentStatusChoices.SUCCESS]
                                                 )
            not_due_amount = 0.0
            for order in orders:
                not_due_amount += float(order.proforma_invoice.grand_total_amount.amount)
            return not_due_amount
        else:
            return 0

    def get_available_amount(self, customer_obj):
        if customer_obj.is_finserv_enabled:
            orders = PartnerOrder.objects.filter(proforma_invoice__customer=customer_obj,
                                                 status__in=[PartnerOrderStatusChoices.DELIVERED],
                                                 agreement__order__isnull=False,
                                                 proforma_invoice__payment__status__in=[PaymentStatusChoices.PENDING,
                                                                                        PaymentStatusChoices.PART_PAYMENT_DONE]
                                                 )
            available_amount = 0.0
            for order in orders:
                available_amount += float(order.proforma_invoice.grand_total_amount.amount)
            return customer_obj.credit_limit - available_amount
        else:
            return 0

    def get_overdue_amount(self, customer_obj):
        today_datetime = datetime.datetime.now()
        today_date = str(today_datetime.date())
        if customer_obj.is_finserv_enabled:
            orders = PartnerOrder.objects.filter(proforma_invoice__customer=customer_obj,
                                                 status__in=[PartnerOrderStatusChoices.DELIVERED],
                                                 agreement__order__isnull=False,
                                                 agreement__due_date__lt=today_date + ' 00:00:01',
                                                 proforma_invoice__payment__status__in=[PaymentStatusChoices.PENDING,
                                                                                        PaymentStatusChoices.PART_PAYMENT_DONE]
                                                 )
            overdue_amount = 0.0
            for order in orders:
                overdue_amount += float(order.proforma_invoice.balance_amount.amount)

            return round(overdue_amount, 2)
        else:
            return 0

    def get_planted_tree(self, customer_obj):
        return 15

    def get_this_month_fuel_saved(self, customer_obj):
        return 50

    def get_saved_approximately(self, customer_obj):
        return 100

'''

from django.shortcuts import render, HttpResponse
from .form import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            return HttpResponse("Yay! you are human.")
        else:
            return HttpResponse("OOPS! Bot suspected.")

    else:
        form = ContactForm()

    return render(request, 'book/contact.html', {'form': form})


from captcha.fields import ReCaptchaField
from django import forms


@csrf_exempt
def verify_captcha(request):
    if request.method == 'POST':
        captcha_response = request.POST.get('captcha')

        captcha = ReCaptchaField()
        try:
            captcha.clean(captcha_response)
            return JsonResponse({'message': 'CAPTCHA verification successful'})
        except forms.ValidationError:
            return JsonResponse({'error': 'CAPTCHA validation failed'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


from Crypto.Cipher import Blowfish


def encrypt_message(request):
    cipher = Blowfish.new('K_5H0OzfMLk_FIcGQkg_H5W3WHNBRQWMoAmKCuEhNeY=', Blowfish.MODE_CBC)
    message = "this is a secrate msg"
    ciphertext = cipher.iv + cipher.encrypt(message.encode())
    return ciphertext


def decrypt_message(key, ciphertext):
    iv = ciphertext[:8]
    ciphertext = ciphertext[8:]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    message = cipher.decrypt(ciphertext).decode()
    return message


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.views.base import TokenView

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()


@method_decorator(csrf_exempt, name="dispatch")
class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get("grant_type") == "password":
                client_id = request.POST.get("client_id")
                client_secret = request.POST.get("client_secret")
                username = request.POST.get("username")
                user = User.objects.get(username=username)

                return super().post(request, *args, **kwargs)
            else:
                return JsonResponse({"error": "unsupported_grant_type"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "invalid_user"}, status=400)


from django.contrib.auth.decorators import login_required


@csrf_exempt
@login_required
def secure_data(request):
    return JsonResponse({'message': 'This is secure data. You are authenticated.'})


from django.contrib.auth import authenticate
from django.http import JsonResponse
from oauth2_provider.views.base import TokenView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TokenRequestSerializer


@api_view(['POST'])
def obtain_access_token(request):
    serializer = TokenRequestSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request=request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is not None:
            token_view = TokenView.as_view()
            request._request.POST = serializer.validated_data
            response = token_view(request._request)
            # Extract the data from the response
            data = response.data if hasattr(response, 'data') else {}
            return Response(data, status=response.status_code)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return Response(serializer.errors, status=400)


import csv
from django.http import HttpResponse


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["First row", "Foo", "Bar", "Baz"])
    writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])

    return response


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def some_view2(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(50, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
