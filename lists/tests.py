from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_needed(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='foo 1', list=list_)
        Item.objects.create(text='foo 2', list=list_)

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'foo 1')
        self.assertContains(response, 'foo 2')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new/', data={'item_text': 'A new list Item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list Item')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new/',
                                    data={'item_text': 'A new list Item'})
        self.assertRedirects(response, '/lists/the-only-list/')


class ListAndItemModelsTest(TestCase):

    def create_a_new_item(self, item_text, list_):
        item = Item()
        item.text = item_text
        item.list_ = list_
        item.save()

    def test_saving_and_retrieving_items(self):

        list_ = List()
        list_.save()

        Item.objects.create(text='The first list item', list=list_)
        Item.objects.create(text='The second', list=list_)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first = saved_items[0]
        second = saved_items[1]

        self.assertEqual(first.text, 'The first list item')
        self.assertEqual(first.list, list_)
        self.assertEqual(second.text, 'The second')
        self.assertEqual(second.list, list_)
