from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from blog.models import Post, Comment, Tag


class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='author', email='author@example.com', password='StrongPass123!'
        )

    def test_post_slug_auto_generated(self):
        post = Post.objects.create(
            author=self.user, title='My First Post', body='Text', status='published'
        )
        self.assertIsNotNone(post.slug)
        self.assertNotEqual(post.slug, '')

    def test_post_str(self):
        post = Post.objects.create(
            author=self.user, title='Test Post', body='Text', status='published'
        )
        self.assertEqual(str(post), 'Test Post')

    def test_comment_count(self):
        post = Post.objects.create(
            author=self.user, title='Post With Comments', body='Text', status='published'
        )
        Comment.objects.create(post=post, author=self.user, body='Comment 1')
        Comment.objects.create(post=post, author=self.user, body='Comment 2')
        self.assertEqual(post.get_comment_count(), 2)


class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='author', email='author@example.com', password='StrongPass123!'
        )
        self.post = Post.objects.create(
            author=self.user, title='Test Post Title', body='Post body text', status='published'
        )

    def test_post_list_loads(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Title')

    def test_draft_not_visible_in_list(self):
        Post.objects.create(
            author=self.user, title='Draft Post', body='Text', status='draft'
        )
        response = self.client.get(reverse('blog:post_list'))
        self.assertNotContains(response, 'Draft Post')

    def test_post_detail_loads(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Title')

    def test_create_post_requires_login(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_post_when_logged_in(self):
        self.client.login(username='author@example.com', password='StrongPass123!')
        self.client.post(reverse('blog:post_create'), {
            'title': 'New Latin Post',
            'body': 'Body of new post',
            'status': 'published',
        })
        self.assertEqual(Post.objects.filter(title='New Latin Post').count(), 1)

    def test_only_author_can_edit(self):
        CustomUser.objects.create_user(
            username='other', email='other@example.com', password='StrongPass123!'
        )
        self.client.login(username='other@example.com', password='StrongPass123!')
        self.client.post(
            reverse('blog:post_edit', kwargs={'pk': self.post.pk}),
            {'title': 'Changed Title', 'body': 'Text', 'status': 'published'}
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Test Post Title')


class CommentTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='user', email='user@example.com', password='StrongPass123!'
        )
        self.post = Post.objects.create(
            author=self.user, title='Post For Comments', body='Text', status='published'
        )

    def test_comment_requires_login(self):
        url = self.post.get_absolute_url()
        self.client.post(url, {'body': 'A comment'})
        self.assertEqual(Comment.objects.count(), 0)

    def test_logged_in_user_can_comment(self):
        self.client.login(username='user@example.com', password='StrongPass123!')
        url = self.post.get_absolute_url()
        self.client.post(url, {'body': 'My comment'})
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().body, 'My comment')


class TagTest(TestCase):
    def test_tag_slug_auto_generated(self):
        tag = Tag.objects.create(name='Django Framework')
        self.assertEqual(tag.slug, 'django-framework')

    def test_posts_by_tag_view(self):
        client = Client()
        user = CustomUser.objects.create_user(
            username='u', email='u@e.com', password='StrongPass123!'
        )
        tag = Tag.objects.create(name='Python')
        post = Post.objects.create(
            author=user, title='Python Post', body='Text', status='published'
        )
        post.tags.add(tag)
        response = client.get(reverse('blog:posts_by_tag', kwargs={'tag_slug': tag.slug}))
        self.assertEqual(response.status_code, 200)
