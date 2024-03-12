import requests
import hashlib
from datetime import datetime


def generate_metadata_from_github_repo(owner, repo, path='', token=None):
    """
    Generate metadata for text files in a GitHub repository.

    :param owner: GitHub repository owner
    :param repo: Repository name
    :param path: Path within the repository to start (use '' for root)
    :param token: Personal access token for GitHub API (optional)
    :return: List of metadata dictionaries for each text file
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        items = response.json()
    except requests.exceptions.HTTPError as ex:
        print(f"Error fetching repository contents: {ex}")
        return []

    metadata_collection = []

    for item in items:
        try:
            if item['type'] == 'file' and item['name'].endswith('.txt'):
                file_response = requests.get(item['download_url'], headers=headers)
                file_response.raise_for_status()
                content = file_response.text
                hex_digest = hashlib.sha256(content.encode('utf-8')).hexdigest()
                file_size = len(content.encode('utf-8'))
                words = content.split()
                word_count = len(words)
                unique_words = len(set(words))
                metadata_collection.append({
                    "file_name": item['name'],
                    "hex_digest": hex_digest,
                    "file_size": file_size,
                    "word_count": word_count,
                    "unique_words": unique_words,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
        except requests.exceptions.HTTPError as ex:
            print(f"Error fetching file {item.get('name', 'unknown')}: {ex}")
        except Exception as e:
            print(f"Error processing file {item.get('name', 'unknown')}: {e}")

    return metadata_collection

