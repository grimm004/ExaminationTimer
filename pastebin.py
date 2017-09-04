# Pastebin API in Python (for use in other applications), by Max Grimmett
# The old one supported by Pastebin was for Python 2, this one supports urllib in Python 3
# @version: 1.5
# Support for more Pastebin Raw API uses coming soon!
from urllib import request, parse

# Define variables
BASE_API_USER_URL = 'http://pastebin.com/api/api_login.php'
BASE_API_URL = 'http://pastebin.com/api/api_post.php'

PUBLIC = 0
UNLISTED = 0
PRIVATE = 0


# Handle encoding and requesting, and returning information to functions that require it
def make_request(base_url, supplied_info):
    data = parse.urlencode(supplied_info)
    data = data.encode('utf-8')
    req = request.Request(base_url, data)
    response = request.urlopen(req)
    response_bytes = response.read()
    return response_bytes


def paste(api_dev_key, text_to_paste, api_paste_name=None, api_user_key=None, api_paste_private='1'):
    # Put the information supplied into a dictionary variable
    info = {'api_dev_key': api_dev_key,
            'api_paste_private': api_paste_private,
            'api_option': 'paste',
            'api_paste_code': text_to_paste}

    # If an API user key is supplied, then add it to the info dictionary
    if api_user_key is not (None or ''):
        info['api_user_key'] = api_user_key

    # If a paste name is supplied, add it to the info dictionary
    if api_paste_name is not (None or ''):
        info['api_paste_name'] = api_paste_name

    # Make the request with the standard API url and the info
    response_value = make_request(BASE_API_URL, info)

    # Return what is given back by the request
    return response_value.decode("utf-8")


def delete_paste(api_dev_key, api_user_key, api_paste_key):
    # Put the information supplied into a dictionary variable
    info = {'api_dev_key': api_dev_key,
            'api_user_key': api_user_key,
            'api_paste_key': api_paste_key,
            'api_option': 'delete'}

    # Make the request with the standard API url and the info
    response_value = make_request(BASE_API_URL, info)

    # Return what is given back by the request
    return response_value.decode("utf-8")


def get_user_key(api_dev_key, api_user_name, api_user_password):
    info = {'api_dev_key': api_dev_key,
            'api_user_name': api_user_name,
            'api_user_password': api_user_password}

    # Make the request with the user API request url and the info
    response_value = make_request(BASE_API_USER_URL, info)

    # Return what is given back by the request
    return response_value.decode("utf-8")


def get_paste_code(url):
    # Set the code variable to the 8 letters or digits on the end of the URL
    code = url[-8:]
    # Return the code
    return code