from collections import Counter
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from .models import Order
import requests
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import Client, Country, TravelPackage, Climate, PromoCode
from django import forms

logger = logging.getLogger(__name__)


class SearchForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Chose country")
    season = forms.ChoiceField(choices=Climate.SEASON_CHOICES, widget=forms.Select(attrs={'readonly': 'readonly'}))
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tour_duration = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'duration'}))
    num_people = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'people amount'}), )


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        print("POST req")
        if form.is_valid():
            print("Valid form")
            country_id = form.cleaned_data['country'].id
            season = form.cleaned_data['season']
            departure_date = form.cleaned_data['departure_date']
            tour_duration = form.cleaned_data['tour_duration']
            num_people = form.cleaned_data['num_people']

            return redirect(reverse(
                'search') + f'?country_id={country_id}&season={season}&departure_date={departure_date}&tour_duration={tour_duration}&num_people={num_people}')
    form = SearchForm()
    orders = Order.objects.all()
    countries = [order.package.country.name for order in orders]
    country_counts = Counter(countries)
    country_labels = list(country_counts.keys())
    country_data = list(country_counts.values())

    return render(request, 'index.html', {'form': form, 'country_labels': country_labels,
                                          'country_data': country_data})


def search(request):
    if request.method == 'GET':
        # Логирование начала обработки запроса
        logger.info('Search request received')

        star_rating = request.GET.get('star_rating')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort_order = request.GET.get('sort_order')
        country_id = request.session.get('country_id')

        if star_rating or min_price or max_price or sort_order:
            # Логирование обработки формы
            logger.debug('Processing form data')

            packages = TravelPackage.objects.all()
            if country_id:
                packages = TravelPackage.objects.filter(country_id=country_id)
            if star_rating:
                packages = packages.filter(hotel__rating__gte=star_rating)

            if min_price:
                packages = packages.filter(intermediate_price__gte=min_price)

            if max_price:
                packages = packages.filter(intermediate_price__lte=max_price)

            if sort_order == 'asc':
                packages = packages.order_by('intermediate_price')
            elif sort_order == 'desc':
                packages = packages.order_by('-intermediate_price')

            return render(request, 'search.html', {'packages': packages})
        else:
            # Логирование обработки страницы
            logger.debug('Processing page')

            country_id = request.GET.get('country_id')

            season = request.GET.get('season')
            departure_date = request.GET.get('departure_date')
            tour_duration = request.GET.get('tour_duration')
            num_people = request.GET.get('num_people')
            request.session['country_id'] = country_id
            request.session['season'] = season
            request.session['departure_date'] = departure_date
            request.session['num_people'] = num_people

            packages = TravelPackage.objects.filter(country_id=country_id)

            return render(request, 'search.html', {
                'packages': packages,
                'country_id': country_id,
                'season': season,
                'departure_date': departure_date,
                'tour_duration': tour_duration,
                'num_people': num_people
            })
    return render(request, 'search.html', {'packages': []})


# Create your views here.


def signup(request):
    if request.method == 'POST':
        print("Форма была отправлена!")
        form = SignUpForm(request.POST)

        if form.is_valid():
            print("Форма валидная!")
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data.get('email', ''),
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
            )
            client = Client(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                birth_date=form.cleaned_data['date_of_birth'],
                belarus_phone_number=form.cleaned_data['phone_number']
            )

            client.save()
            login(request, user)
            return redirect('/')
        else:

            for field in form:
                if field.errors:
                    print(f"Ошибка в поле '{field.label}': {field.errors}")
    else:

        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class SearchDetailView(DetailView):
    model = TravelPackage
    template_name = 'search_detail.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        season = self.request.session.get('season')
        num_people = self.request.session.get('num_people')
        departure_date = self.request.session.get('departure_date')
        package = self.get_object()

        dr = package.duration_days
        sp = package.hotel.standard_room_price
        ip = package.intermediate_price
        fp = (dr * sp + ip) * int(num_people)

        context['package_id'] = package.id
        context['season'] = season
        context['num_people'] = num_people
        context['departure_date'] = departure_date
        context['final_price'] = fp

        self.request.session['final_price'] = str(fp)
        self.request.session['package_id'] = package.id
        return context

    def post(self, request, *args, **kwargs):
        package_id = self.request.session.get('package_id')
        season = self.request.session.get('season')
        num_people = self.request.session.get('num_people')
        departure_date = self.request.session.get('departure_date')
        final_price = self.request.session.get('final_price')

        package = TravelPackage.objects.get(pk=package_id)
        promo_codes = request.user.client.promo_codes.filter(active=True)
        if promo_codes.exists():
            pr = promo_codes[0]
            order = Order.objects.create(
                package=package,
                departure_date=departure_date,
                client=request.user.client,
                final_price=final_price,
                promo_code=pr,
                amount=num_people
            )
            logger.info(f"Order created: {order}")
        else:
            order = Order.objects.create(
                package=package,
                departure_date=departure_date,
                client=request.user.client,
                final_price=final_price, amount=num_people)
            logger.info(f"Order created(no promo): {order}")
            # Очищаем данные из сессии
            del self.request.session['package_id']
            del self.request.session['season']
            del self.request.session['num_people']
            del self.request.session['departure_date']
            del self.request.session['final_price']
        return HttpResponseRedirect(reverse('profile'))


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                promo_code = PromoCode.objects.get(code=code, active=True)
                client = get_object_or_404(Client, user=request.user)
                client.promo_codes.add(promo_code)
                return redirect('profile')
            except PromoCode.DoesNotExist:
                form.add_error('code', 'Invalid promo code')
    else:
        form = PromoCodeForm()
    user = request.user
    client = get_object_or_404(Client, user=user)
    logger.info(f"User accessed profile: {client.last_name}")
    orders = Order.objects.filter(client=client)

    ip_address = get_client_ip(request)
    country_name = get_country_info(ip_address)

    context = {
        'client': client,
        'orders': orders,
        'ip': ip_address,
        'country': country_name,
        'promo_codes': client.promo_codes.all(),
        'form': form
    }

    return render(request, 'profile.html', context)


def get_client_ip(request):
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Проверяем на ошибки HTTP
        ip_data = response.json()
        ip_address = ip_data['ip']
        return ip_address
    except requests.RequestException as e:
        logger.error(f"Error occurred: {e}")
        return None


def get_country_info(ip_address):
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        response.raise_for_status()
        country_data = response.json()
        country_name = country_data['country_name']
        return country_name
    except requests.RequestException as e:
        logger.error(f"Error occurred: {e}")
        return None


class PromoCodeForm(forms.Form):
    code = forms.CharField(max_length=50, label='Promo Code')
