import pytest
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token


@pytest.fixture
def user(db):
    return User.objects.create_user('testuser', password='testpass123')


@pytest.fixture
def auth_headers(user):
    token = Token.objects.create(user=user)
    return {'HTTP_AUTHORIZATION': f'Bearer {token.key}'}


@pytest.fixture
def fire_group(db):
    return Group.objects.create(name='fire')


class TestLoginAPIView:
    @pytest.mark.django_db
    def test_request_login_success(self, client, user):
        res = client.post(
            '/api/login/',
            {'username': 'testuser', 'password': 'testpass123'},
        )
        assert res.status_code == 200
        assert 'token' in res.json()

    @pytest.mark.django_db
    def test_request_login_failed(self, client, user):
        res = client.post(
            '/api/login/',
            {'username': 'testuser', 'password': 'testpass124'},
        )
        assert res.status_code == 400


class TestGroupAddAPIView:
    @pytest.mark.django_db
    def test_request_group_add(self, client, user, auth_headers, fire_group):
        res = client.post('/api/group/fire/add/', **auth_headers)
        assert res.status_code == 204
        assert not res.content
        assert user.groups.filter(name='fire').count() == 1

    @pytest.mark.django_db
    def test_request_group_second_add(self, client, user, auth_headers, fire_group):
        client.post('/api/group/fire/add/', **auth_headers)
        res = client.post('/api/group/fire/add/', **auth_headers)
        assert res.status_code == 204
        assert user.groups.filter(name='fire').count() == 1

    @pytest.mark.django_db
    def test_request_group_error_type_add(self, client, user, auth_headers):
        res = client.post('/api/group/not-a-type/add/', **auth_headers)
        assert res.status_code == 400


class TestGroupRemoveAPIView:
    @pytest.mark.django_db
    def test_request_group_remove(self, client, user, auth_headers):
        user.groups.add(Group.objects.create(name='fire'))

        res = client.post('/api/group/fire/remove/', **auth_headers)
        assert res.status_code == 204
        assert not res.content
        assert user.groups.filter(name='fire').count() == 0

    @pytest.mark.django_db
    def test_request_group_second_remove(self, client, user, auth_headers):
        user.groups.add(Group.objects.create(name='fire'))

        client.post('/api/group/fire/remove/', **auth_headers)
        res = client.post('/api/group/fire/remove/', **auth_headers)
        assert res.status_code == 204
        assert user.groups.filter(name='fire').count() == 0

    @pytest.mark.django_db
    def test_request_group_error_type_remove(self, client, user, auth_headers):
        res = client.post('/api/group/not-a-type/remove/', **auth_headers)
        assert res.status_code == 400


class TestUserMeAPIView:
    @pytest.mark.django_db
    def test_request_user_me_anonymous_failed(self, client):
        res = client.get('/api/user/me/')
        assert res.status_code == 401

    @pytest.mark.django_db
    def test_request_user_me_success(self, client, user, auth_headers, fire_group):
        user.groups.add(fire_group)

        res = client.get('/api/user/me/', **auth_headers)
        assert res.status_code == 200
        assert res.json() == {
            'id': user.id,
            'username': 'testuser',
            'email': '',
            'groups': ['fire'],
        }
