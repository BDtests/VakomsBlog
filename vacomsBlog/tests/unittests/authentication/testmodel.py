from authentication.models import CustomUser
from django.test import TestCase


class TestCustomUserModel(TestCase):

    def setUp(self):
        CustomUser(id=1,
                   first_name='Bohdan',
                   last_name='Dubas',
                   phone='123456789',
                   email='dubas.bogdan@gmail.com',
                   is_active=False).save()

        self.user = CustomUser.objects.get(id=1)

    def test_str(self):
        self.assertEqual(self.user.__str__(), 'dubas.bogdan@gmail.com')

    def test_get_by_id_positive(self):

        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.first_name, 'Bohdan')
        self.assertEqual(self.user.last_name, 'Dubas')
        self.assertEqual(self.user.phone, '123456789')
        self.assertEqual(self.user.email, 'dubas.bogdan@gmail.com')
        self.assertFalse(self.user.is_active)

    def test_get_by_id_negative(self):
        user = CustomUser.get_by_id(111)
        self.assertIsNone(user)

    def test_create(self):
        user = CustomUser.create(first_name='Helen',
                                 last_name='Demkiv',
                                 phone='987654321',
                                 email='helen@gmail.com',
                                 password='demkiv12345')

        self.assertEqual(user.first_name, 'Helen')
        self.assertEqual(user.last_name, 'Demkiv')
        self.assertEqual(user.phone, '987654321')
        self.assertEqual(user.email, 'helen@gmail.com')
        self.assertFalse(user.is_active)

    def test_get_by_email_positive(self):
        user = CustomUser.get_by_email('dubas.bogdan@gmail.com')

        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, 'Bohdan')
        self.assertEqual(user.last_name, 'Dubas')
        self.assertEqual(user.phone, '123456789')
        self.assertEqual(user.email, 'dubas.bogdan@gmail.com')
        self.assertFalse(user.is_active)

    def test_get_by_email_negative(self):
        user = CustomUser.get_by_email('fake.email@gmail.com')

        self.assertIsNone(user)

    def test_delete_by_user_id(self):
        CustomUser.delete_user_by_id(1)
        users=CustomUser.objects.all()

        self.assertEqual(len(users), 0)

    def test_activate(self):
        self.user.activate()

        self.assertTrue(self.user.is_active)

    def test_has_perm(self):
        self.assertTrue(self.user.has_perm(perm='perm'))

    def test_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms(app_label='label'))

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'dubas.bogdan@gmail.com')

    def test_set_admin_rights_positive(self):
        self.user.set_admin_rights(True)
        self.assertTrue(self.user.is_staff)

    def test_set_admin_rights_negative(self):
        self.user.set_admin_rights(False)
        self.assertFalse(self.user.is_staff)
