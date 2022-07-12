import pytz
from django.test import TestCase, SimpleTestCase, Client
from django.contrib.auth import get_user
from django.utils import timezone
from django.urls import reverse
from .models import User, Account, PlantedTree, Tree
from datetime import datetime
import random



class SimpleTest(TestCase):
    
    def setUp(self):
        # Creating accounts
        self.account1 = Account.objects.create()
        self.account1.save()
        self.account2 = Account.objects.create()
        self.account2.save()
        
        # Create users
        self.user1 = User.objects.create_user(username='joseph', email='joseph@email.com',password='12345')        
        self.user1.save()
        self.user2 = User.objects.create_user(username='mary', email='mary@email.com',password='12345')
        self.user2.save()
        self.user3 = User.objects.create_user(username='sarah', email='sarah@email.com',password='12345')
        self.user3.save()
        
        # Adding users to accounts
        self.account1.user.add(self.user1)
        self.account2.user.add(self.user2)
        self.account1.user.add(self.user3)
        self.account2.user.add(self.user1)
        
        # Creating trees
        self.tree1 = Tree.objects.create(name='Amoreira', scientific_name='morus nigra')
        self.tree1.save()
        self.tree2 = Tree.objects.create(name='Sumaúma', scientific_name='ceiba pentandra')
        self.tree2.save()
        self.tree3 = Tree.objects.create(name='Embaúba', scientific_name='cecropia hololeuca')
        self.tree3.save()
        self.tree4 = Tree.objects.create(name='Caliandra', scientific_name='calliandra calothyrsus')
        self.tree4.save()
        
        dt_string = "11/07/2022 09:15:32"
        
        # Planting trees
        self.plantedtree_user1_1 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user1,
                                        tree=self.tree1,
                                        account=self.account1,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user1_1.save()
        
        self.plantedtree_user2_1 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user2,
                                        tree=self.tree2,
                                        account=self.account2,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user2_1.save()
        
        self.plantedtree_user1_2 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user1,
                                        tree=self.tree3,
                                        account=self.account2,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user1_2.save()
        
        self.plantedtree_user3_1 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user3,
                                        tree=self.tree4,
                                        account=self.account1,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user3_1.save()        
        
        self.plantedtree_user2_2 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user2,
                                        tree=self.tree3,
                                        account=self.account2,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user2_2.save()
        
        self.plantedtree_user3_2 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user3,
                                        tree=self.tree2,
                                        account=self.account1,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user3_2.save()
        
        self.plantedtree_user1_3 = PlantedTree.objects.create(
                                        age=0, 
                                        planted_at=datetime(2022, 7, 11, 12, 0, 0, 127325, tzinfo=pytz.UTC),
                                        user=self.user1,
                                        tree=self.tree4,
                                        account=self.account1,
                                        latitude=random.uniform(-5.8, -5.9),
                                        longitude=random.uniform(-35.20, -35.25)
                                    )
        self.plantedtree_user1_3.save()
        
        # client test
        self.client = Client()

    # Test trees planted list access of user
    def test_list_trees_user(self):
        self.client.login(username='sarah', password='12345')                
        response = self.client.get(reverse('tree_list'))
        self.assertEqual(response.status_code, 200)
        
    # Test trees planted list access of another user
    def test_access_tree_another_client(self):
        self.client.login(username='sarah', password='12345')
        response = self.client.get('/tree/3/detail')        
        self.assertEqual(response.status_code, 403)
        
    # Test of access to the list of trees planted in all accounts
    def test_access_list_account_user(self):
        self.client.login(username='joseph', password='12345')
        response = self.client.get(reverse('tree_list_account_users'))
        self.assertEqual(response.status_code, 200)