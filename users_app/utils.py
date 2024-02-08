import requests
from datetime import datetime
import vk_api
from JobHub.settings import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET
from JobHub.utils.fields import formate_phone


def get_user_data(request, code=None, payload=None):
    my_domain = request.build_absolute_uri('/')[:-1]
    redirect_uri = f'{my_domain}/api/users/vk-login/callback'
    access_token = None
    vk_user_id = None

    try:
        print("Start get_user_data function")
        print("Received code:", code)
        print("Received payload:", payload)

        if code:
            print("Code found, fetching access token...")
            response = requests.get('https://oauth.vk.com/access_token', params={
                'client_id': SOCIAL_AUTH_VK_OAUTH2_KEY,
                'client_secret': SOCIAL_AUTH_VK_OAUTH2_SECRET,
                'redirect_uri': redirect_uri,
                'code': code
            })

            data = response.json()
            print("Access token response data:", data)
            access_token = data.get('access_token')
            vk_user_id = data.get('user_id')
            print("Access token:", access_token)
            print("VK user ID:", vk_user_id)

        elif payload:
            print("Payload found, extracting access token and VK user ID...")
            token = payload.get('token')
            uuid = payload.get('uuid')
            response = requests.get('https://api.vk.com/method/auth.exchangeSilentAuthToken', params={
                'token': token,
                'access_token': SOCIAL_AUTH_VK_OAUTH2_SECRET,
                'uuid': uuid,
            })
            data = response.json()

            print('data', data)

            access_token = payload.get('token')
            vk_user_id = payload.get('user', {}).get('id')
            print("Access token:", access_token)
            print("VK user ID:", vk_user_id)

        if access_token and vk_user_id:
            print("Fetching user info from VK API...")
            vk_session = vk_api.VkApi(token=access_token)
            vk = vk_session.get_api()
            user_info = vk.users.get(user_ids=vk_user_id, fields='first_name,last_name,bdate,contacts,domain,photo_200')
            print("VK user info:", user_info)

            if user_info:
                user_data = user_info[0]
                domain = user_data.get('domain')
                photo = user_data.get('photo_200')
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                birth_date = datetime.strptime(user_data.get('bdate'), '%d.%m.%Y').strftime(
                    '%Y-%m-%d') if user_data.get('bdate') else None
                phone_number = formate_phone(user_data.get('mobile_phone'))
                email = f'{vk_user_id}@mail.com'

                print("Extracted user data:", domain, photo, email, first_name, last_name, birth_date, phone_number)
                return vk_user_id, domain, photo, email, first_name, last_name, birth_date, phone_number
            else:
                print("No user info received from VK API")
                return None

    except Exception as e:
        print(f"Error occurred: {e}")

    print("Function execution completed")
    return None

