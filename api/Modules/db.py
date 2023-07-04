from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json 
import random
import time

class Authenticate:
    def __init__(self, uri):
        self.uri = uri
        self.client = MongoClient(self.uri,server_api=ServerApi('1'))
        # try:
        self.client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        # except Exception as e:
        #     print(e)

    def handle_authentication(self, event, email):
        user = event['user']
        firebase_token = event['firebase_token']
        # try:
        # Access a specific database
        db = self.client['hirebot']
        # Access a specific collection
        collection = db['hirebot_user']
        collection.insert_one(event)
        identifier=email
        # identifier = self.generate_unique_identifier() # we will get this from front_end
        # self.store_identifier_in_secure_location(identifier)

        self.store_firebase_token(identifier, firebase_token)

        return {
            'statusCode': 200,
            'body': json.dumps({'identifier': identifier})
        }
        # except Exception as e:
        #     print('Error handling authentication:', e)
        #     return {
        #         'statusCode': 500,
        #         'body': json.dumps({'error': 'Internal server error'})
        #     }
        # finally:
        #     self.client.close()

    # def generate_unique_identifier(self):
    #     # accept from frontend
    #     timestamp = int(time.time()*1000) 
    #     random_number = random.randint(1, 1000000)
    #     id_ = f'{timestamp}_{random_number}'
    #     return id_

    # def store_identifier_in_secure_location(self, identifier):
    #     # Store the identifier in a secure location
    #     pass

    def store_firebase_token(self, identifier, firebase_token):
        try:
            # Access a specific database
            db = self.client['hirebot']
            # Access a specific collection
            collection = db['hirebot_user']
            # filter = {'identifier': identifier}  # Apply your specific filter criteria here
            update = {'firebase_token': firebase_token,'email':identifier}  # Use $set to update the firebase_token field

            collection.insert_one(update)

            return {
                'statusCode': 200,
                'body': json.dumps({'success': True})
            }
        except Exception as e:
            print('Error storing Firebase token:', e)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Internal server error'})
            }
        finally:
            self.client.close()