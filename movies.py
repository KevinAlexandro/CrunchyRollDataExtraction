import requests
import json

def get_request(url, params=None, headers=None, body=None):
    """
    A generic function to make GET requests to a website.

    Args:
        url (str): The URL to send the GET request to
        params (dict, optional): URL parameters to include in the request
        headers (dict, optional): Headers to include in the request
        body (dict or str, optional): Request body to include in the request
            If dict, it will be converted to JSON

    Returns:
        requests.Response: The response from the server

    Example:
        response = get_request(
            url="https://api.example.com/data",
            params={"page": 1, "limit": 10},
            headers={"Authorization": "Bearer token123"},
            body={"query": "search_term"}
        )
    """
    # Prepare headers
    request_headers = headers or {}

    # Prepare body if provided
    if body:
        if isinstance(body, dict):
            # If body is a dictionary, convert to JSON and set content type
            request_headers['Content-Type'] = request_headers.get('Content-Type', 'application/json')
            request_body = json.dumps(body)
        else:
            # If body is already a string, use it as is
            request_body = body
    else:
        request_body = None

    # Make the GET request
    response = requests.get(
        url=url,
        params=params,
        headers=request_headers,
        data=request_body
    )

    # Check if the request was successful
    response.raise_for_status()

    return response
