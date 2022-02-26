# currently, hosted on python anywhere
import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

location_dict = {
    "name": "{my city}}", # use your city
    "lat": "my lat", # use your lat
    "lon": "my lon", # use your lon
    "country": "US",
    "state": "Alabama"
}
exclude_params = "current,minutely,daily"
api_key = "e70cd8252b2ad2789fe5be2a8ed05c8f"
one_call_api_url = f"https://api.openweathermap.org/data/2.5/onecall?" \
                   f"lat={location_dict['lat']}&lon={location_dict['lon']}&" \
                   f"&exclude={exclude_params}&appid={api_key}"
account_sid = "ACa3a2cb4610d5fce5099ff9f41d93850e"
auth_token = "efbd90529c12beb08c85fe2d5ca9242e"

response = requests.get(one_call_api_url)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour in weather_data["hourly"][:12]:
    code = hour["weather"][0]["id"]
    if code < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's gonna rain man, get a umbrella.",
        from_='+18456835697',
        to='+1{my phone number}}' # use your phone number
    )

    print(message.status)
