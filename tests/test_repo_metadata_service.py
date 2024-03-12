import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from services.repo_metadata_service import generate_metadata_from_github_repo
import requests


class TestRepoMetadataService(unittest.TestCase):

    @patch('services.repo_metadata_service.requests.get')
    def test_generate_metadata_from_github_repo(self, mock_get):
        # Setup mock response for GitHub API directory listing
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = [
            {"type": "file", "name": "sample_file_0.txt", "download_url": "http://example.github.com/sample_file_0.txt"}
            # Add more mocked files or directories as needed
        ]
        # Setup mock response for file content
        mock_file_response = MagicMock()
        mock_file_response.text = "Hello World!\nThis is a test file."
        mock_file_response.raise_for_status = MagicMock()

        # Configure the side_effect of mock_get to handle different responses
        mock_get.side_effect = [mock_api_response, mock_file_response,
                                mock_api_response]  # Adjust based on your test scenario

        expected_metadata = [{
            'file_name': 'sample_file_0.txt',
            'hex_digest': unittest.mock.ANY,  # Since the value is dynamic, we use ANY
            'file_size': unittest.mock.ANY,
            # You can calculate this based on mock_file_response.text if you want a specific value
            'word_count': 6,
            'unique_words': 6,
            'date': datetime.now().strftime("%Y-%m-%d")  # This should match the format used in your service
        }]

        # Call the function under test
        metadata_collection = generate_metadata_from_github_repo(owner='mock_owner', repo='mock_repo')

        # Assertions to verify the expected outcomes
        self.assertIsInstance(metadata_collection, list)
        self.assertEqual(len(metadata_collection), 1)

    @patch('services.repo_metadata_service.requests.get')
    def test_generate_metadata_from_github_repo_http_error(self, mock_get):
        # Simulate an HTTP error when fetching repository contents
        mock_get.side_effect = requests.exceptions.HTTPError("Error 404: Not Found")

        # Call the function under test
        metadata_collection = generate_metadata_from_github_repo(owner='mock_owner', repo='mock_repo')

        # Verify that the function handles the exception and returns an empty list
        self.assertIsInstance(metadata_collection, list)
        self.assertEqual(len(metadata_collection), 0)

    @patch('services.repo_metadata_service.requests.get')
    def test_generate_metadata_from_github_repo_connection_error(self, mock_get):
        # Setup mock response for GitHub API directory listing
        mock_api_response = MagicMock()
        mock_api_response.json.return_value = [
            {"type": "file", "name": "sample_file_0.txt", "download_url": "http://example.github.com/sample_file_0.txt"}
        ]
        mock_api_response.raise_for_status = MagicMock()

        # Simulate a connection error only on the second call (when trying to fetch the file content)
        mock_get.side_effect = [mock_api_response, requests.exceptions.ConnectionError("Error: Connection failed")]

        # Call the function under test
        metadata_collection = generate_metadata_from_github_repo(owner='mock_owner', repo='mock_repo')

        # Since the directory listing was successful, the behavior of the function in response to the
        # ConnectionError can be checked here. Depending on how you handle exceptions, this might mean
        # checking for a partially filled list, an empty list, or logging output.
        # For the purpose of this example, let's assume we expect an empty list if any part fails:
        self.assertIsInstance(metadata_collection, list)
        self.assertEqual(len(metadata_collection), 0)  # Assuming the function returns an empty list on error


if __name__ == '__main__':
    unittest.main()
