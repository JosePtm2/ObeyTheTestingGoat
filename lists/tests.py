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
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='foo 1', list=correct_list)
        Item.objects.create(text='foo 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other 1', list=other_list)
        Item.objects.create(text='other 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'foo 1')
        self.assertContains(response, 'foo 2')

        self.assertNotContains(response, 'other 1')
        self.assertNotContains(response, 'other 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new/', data={'item_text': 'A new list Item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list Item')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new/',
                                    data={'item_text': 'A new list Item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):

    def test_can_save_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_listView(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


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
