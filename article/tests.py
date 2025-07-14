from django.test import TestCase
from .models import ArticleInfo, ArticleTag
from account.models import MyUser
from django.utils import timezone
from django.urls import reverse

class ArticleModelTests(TestCase):

    def setUp(self):
        """
        Set up a user for testing purposes.
        This method is run before each test function.
        """
        self.user = MyUser.objects.create_user(username='testuser', password='testpassword123')

    def test_create_articleinfo(self):
        """
        Test that an ArticleInfo object can be created successfully.
        """
        article = ArticleInfo.objects.create(
            author=self.user,
            title='Test Article Title',
            content='This is the content of the test article.',
            created=timezone.now()
        )
        self.assertEqual(article.title, 'Test Article Title')
        self.assertEqual(article.author.username, 'testuser')
        self.assertEqual(str(article), f"title:{article.title},author:{article.author}")

    def test_create_articletag(self):
        """
        Test that an ArticleTag object can be created successfully.
        """
        tag = ArticleTag.objects.create(
            tag='Test Tag',
            user=self.user
        )
        self.assertEqual(tag.tag, 'Test Tag')
        self.assertEqual(tag.user.username, 'testuser')
        self.assertEqual(str(tag), 'Test Tag')


class ArticleViewTests(TestCase):

    def setUp(self):
        """
        Set up a user and some articles for view testing.
        """
        self.user = MyUser.objects.create_user(username='viewtestuser', password='testpassword123')
        self.article1 = ArticleInfo.objects.create(
            author=self.user,
            title='View Test Article 1',
            content='Content for view test 1.'
        )
        self.article2 = ArticleInfo.objects.create(
            author=self.user,
            title='View Test Article 2',
            content='Content for view test 2.'
        )

    def test_homepage_view(self):
        """
        Test the HomePageView for status code, template used, and content.
        """
        url = reverse('article:home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'View Test Article 1')
        self.assertContains(response, 'View Test Article 2')
