import unittest
from appointment import app

class AppointmentTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_booking_success(self):
        response = self.client.post("/book", json={
            "car_plate": "XYZ123",
            "date": "2025-10-28",
            "time": "10:00",
            "service_ids": [1],
            "notes": "Routine check"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["status"], "success")