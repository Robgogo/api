from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json

from .models import Song
from .serializers import SongsSerializer
# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Song.objects.create(title=title, artist=artist)
            

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def setUp(self):
        # add test data

        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        self.create_song("like glue", "sean paul")
        self.create_song("simple song", "konshens")
        self.create_song("love is wicked", "brick and lace")
        self.create_song("jam rock", "damien marley")


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """

        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Song.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AuthLoginUserTest(BaseViewTest):

    """
    Test for auth/login path
    """

    def test_login_user_with_valid_credentials(self):

        response = self.login_a_user("test_user","testing")

        self.assertIn("token",response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)