import requests
from django.conf import settings
from django.shortcuts import render
from datetime import datetime, timedelta

def get_weather_icon(description):
    description = description.lower()
    
    # بارش‌ها
    if 'heavy rain' in description or 'باران شدید' in description:
        return 'fas fa-cloud-showers-heavy fa-2x text-primary', 'باران شدید'
    elif 'rain' in description or 'باران' in description:
        return 'fas fa-cloud-rain fa-2x text-info', 'بارانی'
    elif 'drizzle' in description or 'نمنم' in description:
        return 'fas fa-cloud-rain fa-2x text-info', 'نمنم بارون'
    elif 'shower' in description or 'رگبار' in description:
        return 'fas fa-cloud-showers-heavy fa-2x text-primary', 'رگباری'
    
    # برف و یخ
    elif 'snow' in description or 'برف' in description:
        return 'fas fa-snowflake fa-2x text-info', 'برفی'
    elif 'sleet' in description or 'برف و باران' in description:
        return 'fas fa-cloud-sleet fa-2x text-info', 'برف و باران'
    elif 'hail' in description or 'تگرگ' in description:
        return 'fas fa-cloud-hail-mixed fa-2x text-info', 'تگرگی'
    
    # طوفان و رعد و برق
    elif 'thunderstorm' in description or 'رعد و برق' in description:
        return 'fas fa-bolt fa-2x text-warning', 'رعد و برقی'
    elif 'storm' in description or 'طوفان' in description:
        return 'fas fa-hurricane fa-2x text-danger', 'طوفانی'
    
    # مه و غبار
    elif 'mist' in description or 'مه' in description:
        return 'fas fa-smog fa-2x text-secondary', 'مه‌آلود'
    elif 'fog' in description or 'مه غلیظ' in description:
        return 'fas fa-smog fa-2x text-secondary', 'مه غلیظ'
    elif 'haze' in description or 'غبار' in description:
        return 'fas fa-smog fa-2x text-warning', 'غبارآلود'
    
    # ابری
    elif 'scattered clouds' in description or 'ابرهای پراکنده' in description:
        return 'fas fa-cloud-sun fa-2x text-secondary', 'نیمه ابری'
    elif 'broken clouds' in description or 'ابرهای شکسته' in description:
        return 'fas fa-cloud fa-2x text-secondary', 'ابرهای شکسته'
    elif 'overcast' in description or 'ابرهای متراکم' in description:
        return 'fas fa-cloud fa-2x text-secondary', 'ابرهای متراکم'
    elif 'cloud' in description or 'ابری' in description:
        return 'fas fa-cloud fa-2x text-secondary', 'ابری'
    
    # صاف و آفتابی
    elif 'clear' in description or 'صاف' in description:
        return 'fas fa-sun fa-2x text-warning', 'آفتابی'
    elif 'partly cloudy' in description or 'نیمه ابری' in description:
        return 'fas fa-cloud-sun fa-2x text-warning', 'نیمه ابری'
    
    # دمای هوا
    elif 'hot' in description or 'گرم' in description:
        return 'fas fa-temperature-high fa-2x text-danger', 'گرم'
    elif 'cold' in description or 'سرد' in description:
        return 'fas fa-temperature-low fa-2x text-info', 'سرد'
    
    # باد
    elif 'wind' in description or 'باد' in description:
        return 'fas fa-wind fa-2x text-secondary', 'وزش باد'
    
    # حالت پیش‌فرض
    else:
        return 'fas fa-cloud fa-2x text-secondary', 'معمولی'

def get_relative_day(date_str):
    today = datetime.now().date()
    forecast_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    diff = (forecast_date - today).days
    
    # نام روزهای هفته به فارسی
    weekdays = {
        0: 'دوشنبه',
        1: 'سه‌شنبه',
        2: 'چهارشنبه',
        3: 'پنج‌شنبه',
        4: 'جمعه',
        5: 'شنبه',
        6: 'یک‌شنبه'
    }
    
    weekday_name = weekdays[forecast_date.weekday()]
    
    if diff == 0:
        return f'امروز ({weekday_name})'
    elif diff == 1:
        return f'فردا ({weekday_name})'
    elif diff == 2:
        return f'پس‌فردا ({weekday_name})'
    else:
        return f'{diff} روز بعد ({weekday_name})'

def index(request):
    city = request.GET.get('city', 'Tehran')
    api_key = settings.OPENWEATHER_API_KEY

    current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fa'
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=fa'

    current_response = requests.get(current_url)
    forecast_response = requests.get(forecast_url)

    if current_response.status_code == 200 and forecast_response.status_code == 200:
        current_data = current_response.json()
        forecast_data = forecast_response.json()

        description = current_data['weather'][0]['description']
        current_icon, current_description = get_weather_icon(description)

        forecast_list = []
        for item in forecast_data['list']:
            if "12:00:00" in item['dt_txt']:
                forecast_description = item['weather'][0]['description']
                icon, forecast_description = get_weather_icon(forecast_description)
                forecast_list.append({
                    'date': item['dt_txt'].split(' ')[0],
                    'temp': item['main']['temp'],
                    'description': forecast_description,
                    'icon': icon
                })

        context = {
            'city': current_data['name'],
            'temperature': current_data['main']['temp'],
            'description': current_description,
            'icon': current_icon,
            'forecast': forecast_list
        }

    else:
        context = {
            'error': 'شهر مورد نظر یافت نشد.'
        }

    return render(request, 'weather.html', context)

def weather_view(request):
    city = request.GET.get('city')
    if not city:
        return render(request, 'weather/weather.html', {})
        
    api_key = settings.WEATHER_API_KEY

    current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fa'
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=fa'

    try:
        current_response = requests.get(current_url)
        forecast_response = requests.get(forecast_url)

        if current_response.status_code != 200 or forecast_response.status_code != 200:
            return render(request, 'weather/weather.html', {
                'error': 'پیدا نشد',
                'searched_city': city
            })

        current_weather = current_response.json()
        forecast_data = forecast_response.json()

        forecast_list = forecast_data.get('list', [])
        daily_forecast = []

        for i in range(0, len(forecast_list), 8):  # هر ۸ داده، تقریبا یک روز است
            item = forecast_list[i]
            icon, description = get_weather_icon(item['weather'][0]['description'])
            date_str = item['dt_txt'].split(' ')[0]
            relative_day = get_relative_day(date_str)
            
            daily_forecast.append({
                'date': relative_day,
                'temp': int(round(item['main']['temp'])),  # گرد کردن به نزدیکترین عدد صحیح
                'description': description,
                'icon': icon
            })

        current_icon, current_description = get_weather_icon(current_weather.get('weather', [{}])[0].get('description'))

        context = {
            'city': city,
            'temp': int(round(current_weather.get('main', {}).get('temp', 0))),  # گرد کردن به نزدیکترین عدد صحیح
            'description': current_description,
            'icon': current_icon,
            'forecast': daily_forecast
        }

    except Exception as e:
        context = {
            'error': 'پیدا نشد',
            'searched_city': city
        }

    return render(request, 'weather/weather.html', context)

def handler404(request, exception):
    return render(request, 'weather/404.html', status=404)
