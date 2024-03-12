from flask import Blueprint, jsonify, send_file
from services.metadata_service import fetch_metadata, metadata_to_csv

metadata_blueprint = Blueprint('metadata', __name__)


@metadata_blueprint.route('/metadata')
def metadata_collection():
    """
    Endpoint to retrieve a collection of metadata.

    This route handles the GET request to fetch and return a JSON representation
    of metadata. It utilizes the `fetch_metadata` service to obtain the metadata
    from a predefined source (e.g., a database or a directory of files).

    Returns:
        A Flask JSON response containing an array of metadata objects. Each object
        in the array represents metadata for a single entity, with key-value pairs
        corresponding to metadata attributes.
    """
    metadata = fetch_metadata()
    return jsonify(metadata)


@metadata_blueprint.route('/metadata/download')
def download_metadata():
    """
    Endpoint to download metadata as a CSV file.

    This route handles the GET request to fetch metadata and then convert it into
    a CSV format for download. It leverages the `fetch_metadata` service to obtain
    the metadata and the `metadata_to_csv` service to convert the metadata into a
    CSV format stored in a temporary file-like object.

    Returns:
        A Flask response that prompts the user to download the metadata in CSV format.
        The `Content-Type` is set to 'text/csv', and the content disposition is configured
        to prompt for download with a predefined filename ('interview.csv').
    """
    metadata = fetch_metadata()
    csv_file = metadata_to_csv(metadata)
    return send_file(
        csv_file,
        mimetype="text/csv",
        as_attachment=True,
        download_name='interview.csv'
    )
