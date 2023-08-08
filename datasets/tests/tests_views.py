from django.test import TestCase, Client
from django.urls import reverse
from datasets.models import User, Dataset, ModificationRequest, Collection

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="test@gmail.com", password='testpassword')
        self.dataset = Dataset.objects.create(id=1, dataset_name='Test Dataset')
        self.collection = Collection.objects.create(name='Test Collection', user=self.user)

    def test_user_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasets/login.html')

    def test_user_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasets/register.html')

    def test_user_logout(self):
        self.client.login(email='test@gmail.com', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_datasets(self):
        response = self.client.get(reverse('datasets'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasets/datasets.html')

    def test_searchpage_view(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasets/searchpage.html')

    def test_search_results_view(self):
        query = "test query"
        response = self.client.get(reverse('search_results'), {'q': query})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasets/search_results.html')
        self.assertEqual(response.context['query'], query)

    def test_collection(self):
        response = self.client.get(reverse('collection', args=[self.collection.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasets/collection.html')

    # def test_create_collection(self):   
    #     self.client.login(email='test@gmail.com', password='testpassword')
    #     response = self.client.get(reverse('create_collection'))
    #     self.assertEqual(response.status_code, 302)  # Redirect to collections
    #     response = self.client.post(reverse('create_collection'), {'name': 'Test Collection 2'})
    #     self.assertEqual(response.status_code, 302)  # Redirect to collections
    #     self.assertTrue(Collection.objects.filter(name='Test Collection 2').exists())
