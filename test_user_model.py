"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask_bcrypt import Bcrypt


from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()

bcrypt = Bcrypt()
PASSWORD = bcrypt.generate_password_hash("password", rounds=5).decode("utf-8")



class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)


    # def test_is_following(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as sess:
    #             sess["curr_user"] = self.u1_id
    #         resp = client.post(
    #             f"/users/follow/{self.u2_id}",
    #             data={
    #                 'id':"2"
    #             }
    #         )
    #         print("RESPONSE DATA", resp.data)
    #         print("!!!!!!SESSION", sess)
    #         print("U1!!!!", sess["curr_user"])

    #         u2 = User.query.get(self.u2_id)

    #         self.u1.following.append(u2)

    #         db.session.commit()
    #         self.assertEqual(resp.status_code, 302)
    #         self.assertEqual(sess["curr_user"].is_following(u2), True)

