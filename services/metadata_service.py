from flask import current_app
from .repo_metadata_service import generate_metadata_from_github_repo
from io import StringIO, BytesIO
import csv


def fetch_metadata():
    """
    Fetch metadata from a GitHub repository specified in the current application's configuration.

    This function uses the `generate_metadata_from_github_repo` service to retrieve metadata
    for all files within the specified GitHub repository. It relies on configuration values
    for the repository owner (`GIT_OWNER`) and repository name (`GIT_REPO`).

    Returns:
        list: A collection of metadata dictionaries, where each dictionary contains metadata
        for a single file within the GitHub repository.
    """
    meta_data_collection = generate_metadata_from_github_repo(owner=current_app.config['GIT_OWNER'],
                                                              repo=current_app.config['GIT_REPO'])
    return meta_data_collection


def metadata_to_csv(metadata_list):
    """
    Convert a list of metadata dictionaries into a CSV format.

    This function takes a list of metadata dictionaries and converts them into a CSV file,
    which is then returned as a BytesIO object for easy handling and response in Flask. It checks
    the `SKIP_HEADER` configuration to determine if the CSV should include a header row.

    Parameters:
        metadata_list (list): A list of dictionaries, where each dictionary represents metadata
        for a single file and contains keys and values corresponding to metadata attributes.

    Returns:
        BytesIO: An in-memory file object containing the CSV data, encoded in UTF-8. This object
        can be directly used in Flask responses to serve a CSV file download.
    """
    output = StringIO()
    writer = csv.writer(output)

    # Write the header based on the first item's keys
    if current_app.config['SKIP_HEADER'] is False:
        writer.writerow(metadata_list[0].keys())

    for metadata in metadata_list:
        writer.writerow(metadata.values())

    mem = BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    output.close()

    return mem
