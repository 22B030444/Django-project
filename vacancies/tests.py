from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Group

from employers.models import EmployerProfile
from vacancies.models import Vacancy
from company.models import Company

class VacancyTests(APITestCase):
    def setUp(self):
        self.admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.employer_group, _ = Group.objects.get_or_create(name="Employer")
        self.hunter_group, _ = Group.objects.get_or_create(name="Hunter")

        self.admin_user = User.objects.create_superuser(username="admin", password="password")
        self.employer_user = User.objects.create_user(username="employer", password="password")

        self.hunter_user = User.objects.create_user(username="hunter", password="password")

        self.company = Company.objects.create(name="Test Company", description="A test company.")
        self.employer_profile = EmployerProfile.objects.create(
            user=self.employer_user,
            company=self.company,
            is_verified=True
        )

        self.admin_user.groups.add(self.admin_group)
        self.employer_user.groups.add(self.employer_group)
        self.hunter_user.groups.add(self.hunter_group)

        self.vacancy = Vacancy.objects.create(
            title="New Vacancy",
            description="A test vacancy description.",
            company=self.company,
            posted_by=self.employer_user,
            salary=50000,
        )

    def test_unauthenticated_user_can_view_vacancies(self):
        url = reverse("vacancy_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)

    def test_authenticated_user_can_view_vacancies(self):
        self.client.force_authenticate(user=self.hunter_user)
        url = reverse("vacancy_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)

    def test_employer_can_create_vacancy(self):
        self.client.force_authenticate(user=self.employer_user)
        url = reverse("vacancy_create")
        data = {
            "title": "New Vacancy",
            "description": "Description for new vacancy",
            "company": self.company.id,
            "salary": 60000,
        }
        print(f'COMPANY IDIDIDI{self.company.id}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vacancy.objects.count(), 2)
        self.assertEqual(Vacancy.objects.last().title, "New Vacancy")

    def test_non_employer_cannot_create_vacancy(self):
        self.client.force_authenticate(user=self.hunter_user)
        url = reverse("vacancy_create")
        data = {
            "title": "Unauthorized Vacancy",
            "description": "Should not be created",
            "company": self.company.id,
            "salary": 40000,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employer_can_update_own_vacancy(self):
        self.client.force_authenticate(user=self.employer_user)
        url = reverse("vacancy_edit", kwargs={"pk": self.vacancy.id})
        data = {"title": "Updated Vacancy Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vacancy.refresh_from_db()
        self.assertEqual(self.vacancy.title, "Updated Vacancy Title")

    def test_employer_cannot_update_others_vacancy(self):
        other_employer = User.objects.create_user(username="other_employer", password="password")
        other_employer.groups.add(self.employer_group)
        self.client.force_authenticate(user=other_employer)
        url = reverse("vacancy_edit", kwargs={"pk": self.vacancy.id})
        data = {"title": "Hacked Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_vacancy(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("vacancy_edit", kwargs={"pk": self.vacancy.id})
        data = {"title": "Admin Updated Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vacancy.refresh_from_db()
        self.assertEqual(self.vacancy.title, "Admin Updated Title")

    def test_employer_can_delete_own_vacancy(self):
        self.client.force_authenticate(user=self.employer_user)
        url = reverse("vacancy_delete", kwargs={"pk": self.vacancy.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vacancy.objects.count(), 0)

    def test_employer_cannot_delete_others_vacancy(self):
        other_employer = User.objects.create_user(username="other_employer", password="password")
        other_employer.groups.add(self.employer_group)
        self.client.force_authenticate(user=other_employer)
        url = reverse("vacancy_delete", kwargs={"pk": self.vacancy.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_vacancy(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("vacancy_delete", kwargs={"pk": self.vacancy.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vacancy.objects.count(), 0)
