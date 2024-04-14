import requests
import unittest

class TestBannerAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:8000"  # Update with your API base URL
    user = {"token": "2"}
    admin = {"token": "1"}
    banner: int = 34
    data = {
            "tag_ids": [99],
            "feature_id": 1,
            "content": {"title": "Test Title", "text": "Test Text", "url": "test_url"},
            "is_active": True
        }

    def test_create_banner(self):
        url = f"{self.base_url}/banner?token={self.admin['token']}"
        response = requests.post(url, json=self.data)
        self.banner = response.json()['banner_id']
        self.assertEqual(response.status_code, 201)
        # Extract and validate the created banner_id from the response

    def test_get_user_banner(self):
        url = f"{self.base_url}/user_banner?token={self.admin['token']}"
        params = {"tag_id": self.data["tag_ids"][0], "feature_id": self.data['feature_id'], "use_last_revision": False}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed for the response content

    def test_get_all_banners(self):
        url = f"{self.base_url}/banner?token={self.admin['token']}"
        params = {"feature_id": 1, "tag_id": 1, "limit": 10, "offset": 0}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed for the response content

    def test_update_banner(self):
        banner_id = self.banner  # Update with an existing banner ID
        url = f"{self.base_url}/banner/{banner_id}?token={self.admin['token']}"
        print(self.banner)
        self.data = {"content": {"title": "Updated Title", "text": "Updated Text", "url": "updated_url"}}
        response = requests.patch(url, json=self.data)
        self.assertEqual(response.status_code, 200)
        # Validate the updated banner content if needed

    def test_delete_banner(self):
        banner_id = self.banner  # Update with an existing banner ID
        url = f"{self.base_url}/banner/{banner_id}?token={self.admin['token']}"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)
        # Ensure the banner is deleted

if __name__ == "__main__":
    unittest.main()
