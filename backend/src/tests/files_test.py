import unittest
import os
import jwt
from app import app
from utilities import client_methods
from initialize_db import initialize_database
import json
from db import db
from datetime import datetime
import sqlalchemy.exc
import controllers.users
from utilities import file_methods


class TestClient(unittest.TestCase):
    def setUp(self):
        initialize_database()
        data = {"username": "pekka@mail.com", "password": "pekka123", "role": 1}
        app.test_client().post("/api/users", json=data)
        self.client_data = { "user_id": 1,
                        "company": "Testiyritys",
                        "email": "testi@gmail.com",
                        "phonenumber": "+358 123456789",
                        "bi_code": "1234567-8",
                        "deadlines": json.dumps([1731196800000, 1594876800000]),
                        "payperiod": "kuukausi"}
        self.updated_client_data = { "user_id": 1,
                        "company": "Testiyritys",
                        "email": "testi@gmail.com",
                        "phonenumber": "+358 123456788",
                        "bi_code": "1234567-8",
                        "deadlines": json.dumps([1731196800000, 1594876800000]),
                        "payperiod": "kuukausi"}
        token = jwt.encode({
            "username": "pekka@mail.com", "id": 1, "role": 1}, os.environ.get('SECRET_KEY'), algorithm='HS256')
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        self.file = {
            "id": 1,
            "owner": 1,
            "name": "test.pdf",
            "path": "test/path",
            "date": datetime.now()
        }
        self.odt = {
            "id": 1,
            "owner": 1,
            "path": "test/path",
            "date": datetime.now()
        }
        self.no_name_file = {
            "id": 1,
            "owner": 1,
            "name": "",
            "path": "test/path",
            "date": datetime.now()
        }

    def test_get_all_files_with_valid_token(self):
        with app.test_request_context():
            client_methods.add_client(self.client_data)
            db.session.commit()
            file_methods.add_file(self.file)
            response = app.test_client().get("/api/files", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()), 1)

    def test_upload_file_fails_with_invalid_file_type(self):
        with app.test_request_context():
            with self.assertRaises(sqlalchemy.exc.StatementError):
                file_methods.add_file(self.odt)
            response = app.test_client().post("/api/files", headers=self.headers)
            self.assertEqual(response.status_code, 400)

    def test_upload_file_fails_with_no_name(self):
        with app.test_request_context():
            with self.assertRaises(sqlalchemy.exc.StatementError):
                file_methods.add_file("")
            response = app.test_client().post("/api/files", headers=self.headers)
            self.assertEqual(response.status_code, 400)
