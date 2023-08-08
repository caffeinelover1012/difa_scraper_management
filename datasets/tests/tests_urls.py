from django.test import SimpleTestCase
from django.urls import reverse, resolve
from datasets.views import (
    searchpage, datasets, dataset,
    create_modification_request, scrape_dataset,
    collections, collection,
    create_collection, user_login,
    register, about, modification_requests,
    view_changes, approve_request, reject_request,
    modify_modification_request, delete_modification_request,
    person_detail, research_team, leadership_team,
    scrape_all_view, workshop, partners,
    scraping_progress_view, search_results, user_logout,
)

class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, searchpage)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, searchpage)

    def test_datasets_url_resolves(self):
        url = reverse('datasets')
        self.assertEqual(resolve(url).func, datasets)

    def test_dataset_url_resolves(self):
        url = reverse('dataset', args=[1])
        self.assertEqual(resolve(url).func, dataset)

    def test_create_modification_request_url_resolves(self):
        url = reverse('create_modification_request',args=[1])
        self.assertEqual(resolve(url).func,create_modification_request)

    def test_scrape_dataset_url_resolves(self):
        url = reverse('scrape_dataset',args=[1])
        self.assertEqual(resolve(url).func,scrape_dataset)
    
    def test_collections_url_resolves(self):
        url = reverse('collections')
        self.assertEqual(resolve(url).func,collections)
    
    def test_collection_url_resolves(self):
        url = reverse('collection',args=[1])
        self.assertEqual(resolve(url).func,collection)

    def test_create_collection_url_resolves(self):
        url = reverse('create_collection')
        self.assertEqual(resolve(url).func,create_collection)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func,user_login)
    
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func,register)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func,about)

    def test_modification_requests_url_resolves(self):
        url = reverse('modification_requests')
        self.assertEqual(resolve(url).func,modification_requests)

    def test_view_changes_url_resolves(self):
        url = reverse('view_changes',args=[1])
        self.assertEqual(resolve(url).func,view_changes)

    def test_approve_request_url_resolves(self):
        url = reverse('approve_request',args=[1])
        self.assertEqual(resolve(url).func,approve_request)

    def test_reject_request_url_resolves(self):
        url = reverse('reject_request',args=[1])
        self.assertEqual(resolve(url).func,reject_request)

    def test_modify_modification_request_url_resolves(self):
        url = reverse('modify_modification_request',args=[1])
        self.assertEqual(resolve(url).func,modify_modification_request)

    def test_delete_modification_request_url_resolves(self):
        url = reverse('delete_modification_request',args=[1])
        self.assertEqual(resolve(url).func,delete_modification_request)

    def test_person_detail_url_resolves(self):
        url = reverse('person_detail',args=[1])
        self.assertEqual(resolve(url).func,person_detail)

    def test_research_team_url_resolves(self):
        url = reverse('research_team')
        self.assertEqual(resolve(url).func,research_team)

    def test_leadership_team_url_resolves(self):
        url = reverse('leadership_team')
        self.assertEqual(resolve(url).func,leadership_team)

    def test_scrape_all_url_resolves(self):
        url = reverse('scrape_all')
        self.assertEqual(resolve(url).func,scrape_all_view)

    def test_workshop_url_resolves(self):
        url = reverse('workshop')
        self.assertEqual(resolve(url).func,workshop)

    def test_partners_url_resolves(self):
        url = reverse('partners')
        self.assertEqual(resolve(url).func,partners)

    def test_scrape_progress_url_resolves(self):
        url = reverse('scrape_progress')
        self.assertEqual(resolve(url).func,scraping_progress_view)

    def test_search_results_url_resolves(self):
        url = reverse('search_results')
        self.assertEqual(resolve(url).func,search_results)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func,user_logout)

    