import requests


class CrunchyrollAPI:
    def __init__(self):
        self.__url = 'https://www.crunchyroll.com/'
        # self.__cookie = self.__get_cookie()
        # print(self.__cookie)
        self.__token = self.__get_token()
        print('token is...')
        print(self.__token)

    def __get_cookie(self):
        response = requests.post(
            url=f'{self.__url}cdn-cgi/challenge-platform/h/b/jsd/r/0.02975517902764514:1749313068:3o6hhPPPJF6MinhGQcse9M4jLa_eNI9CIdVcnjXdmJg/94c1ca224dc69af7'
        )
        if response.status_code == 200:
            cookies = ''
            for cookie in response.cookies:
                cookies = f'{cookie.name}={cookie.value}; {cookies}'

            return cookies
        else:
            print(f"Error: {response.status_code}")
            return None

    def __get_token(self):

        response = requests.post(
            url=f'{self.__url}auth/v1/token',
            headers={
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.5',
                'Alt-Used': 'www.crunchyroll.com',
                'Authorization': 'Basic Y3Jfd2ViOg==',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'ETP-Anonymous-Id': '450f9dfb-a85f-43b1-a9b7-6031a44ccf52',
                # 'Cookie':self.__cookie,
                'Host': 'www.crunchyroll.com',
                'Origin': 'https://www.crunchyroll.com',
                'Referer': 'https://www.crunchyroll.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0',
            },
            data='grant_type=client_id'
        )

        if response.status_code == 200:
            return response.json().get('access_token')  # Extrae el token del JSON
        else:
            print(f"Error: {response.status_code}")
            return None


if __name__ == '__main__':
    api = CrunchyrollAPI()
