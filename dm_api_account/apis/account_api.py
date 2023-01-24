import json
import allure
import requests
from pydantic import ValidationError
from utilities.rest_client import RestClient
from dm_api_account.models import RegistrationModel, UserEnvelopeModel, ChangePasswordModel


class AccountApi:
    def __init__(self, host: str = 'http://localhost:5051', headers: dict = None):
        self.host = host
        self.session = requests.session()
        self.session.headers = headers
        self.client = RestClient(host=host, headers=headers)

    def post_v1_account(
            self,
            registration_model: RegistrationModel | dict,
            status_code=201,
            validate_request_body=True,
            **kwargs: dict
    ) -> requests.Response:
        registration_model = self.validate_model(
            model=registration_model,
            model_type=RegistrationModel,
            validate=validate_request_body
        )
        """
        Register new user
        :param registration_model:
        :return:
        """
        response = self.client.post(
            path='/v1/account',
            json=registration_model,
            **kwargs,
        )
        assert response.status_code == status_code, f'Статус код ответа должен быть {status_code}'
        return response

    @allure.step('Получение информации о пользователе')
    def get_v1_account(self, status_code=200, **kwargs: dict):
        """
        Get current user
        :return:
        """
        response = self.client.get(
            path='/v1/account',
            **kwargs,
        )
        assert response.status_code == status_code, \
            f"Статус код ответа должен быть 200, но он равен {response.status_code}"
        return response

    @staticmethod
    def validate_model(model, model_type=None, validate=False):
        if isinstance(model, dict) and validate is False:
            return model
        elif isinstance(model, dict) and model_type and validate is True:
            return model_type.parse_obj(model)
        elif isinstance(model, model_type) and validate:
            validate_model = model.json(
                by_alias=True,
                exclude_none=True
            )
            try:
                model_type.parse_raw(validate_model)
            except ValidationError as e:
                raise AssertionError(e.json())

            return json.loads(validate_model)
        elif isinstance(model, model_type) and validate is False:
            raise AssertionError(f"If using model type {model_type}, 'validate' should be True")
        else:
            raise AssertionError(f"Model should be type {model_type}")

    def put_v1_account_token(
            self,
            token: str,
            status_code=200,
            validate_response=True,
            full_response=False,
            **kwargs: dict
    ) -> requests.Response:
        """
        Activate registered user
        :param token: Activation token
        :return:
        """
        response = self.client.put(
            path=f'/v1/account/{token}',
            **kwargs,
        )
        assert response.status_code == status_code, f'Статус код ответа должен быть {status_code}'
        response_json = response.json()
        response_model = self.validate_model(
            model=response_json,
            model_type=UserEnvelopeModel,
            validate=validate_response
        )
        response = response if full_response else response_model
        return response

    def post_v1_account_password(self, reset_password_model: dict, **kwargs: dict) -> requests.Response:
        """
        Reset registered user password
        :param reset_password_model:
        :param headers: {'X-Dm-Auth-Token': auth token}
        :return:
        """
        response = self.client.post(
            path='/v1/account/password',
            json=reset_password_model,
            **kwargs,
        )
        return response

    def put_v1_account_password(self, change_password_model: ChangePasswordModel, **kwargs: dict) -> requests.Response:
        change_password_model = self._validate_model(
            model=change_password_model,
            model_type=ChangePasswordModel
        )
        """
        Change registered user password
        :param change_password_model:
        :return:
        """
        response = self.client.put(
            path='/v1/account/password',
            json=change_password_model,
            **kwargs,
        )
        return response

    def put_v1_account_email(self, change_email: dict, **kwargs: dict) -> requests.Response:
        """
        Change registered user email
        :param change_email:
        :return:
        """
        response = self.client.put(
            path='/v1/account/email',
            json=change_email,
            **kwargs,
        )
        return response
