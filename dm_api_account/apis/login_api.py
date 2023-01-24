import allure
import requests
from utilities.rest_client import RestClient


class LoginApi:
    def __init__(self, host: str = 'http://localhost:5051', headers: dict = None):
        self.host = host
        self.client = RestClient(host=host, headers=headers)

    def set_headers(self, headers):
        self.client.session.headers = headers

    @allure.step('Авторизация пользователя')
    def post_v1_account_login(self, login_credentials: dict, **kwargs: dict) -> requests.Response:
        """
        Authenticate via credentials
        :param login_credentials:
        :return:
        """
        response = self.client.post(
            path='/v1/account/login',
            json=login_credentials,
            **kwargs,
        )
        return response

    @allure.step('Разлогин пользователя')
    def delete_v1_account_login(self, **kwargs: dict) -> requests.Response:
        """
        Logout as current user
        :return:
        """
        response = self.client.delete(
            path='/v1/account/login',
            **kwargs,
        )
        return response

    @allure.step('Разлогин пользователя отовсюду')
    def delete_v1_account_login_all(self, **kwargs: dict) -> requests.Response:
        """
        Logout from every device
        :return:
        """
        response = self.client.delete(
            path='/v1/account/login/all',
            **kwargs,
        )
        return response
