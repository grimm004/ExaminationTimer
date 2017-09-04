# Key Authentication File
# 06/06/2015 | All rights Reserved
# @version: 3.0
# @author Max Grimmett (10.3)

from os import remove, getenv, path, makedirs
from urllib.error import *
import urllib.request
import encode_string_general
import authenticator
import debug
import registry

is_debug = False
if debug.MASTER_DEBUG or debug.Authenticate_Key:
    is_debug = True
__DEBUG__ = is_debug

if __DEBUG__:
    print("AUTHENTICATE_KEY: Debugging is enabled.")

# Create directory and file strings
APP_DATA = getenv('APPDATA')
ROOT_DIR = '\\ExaminationTimer\\'
REG_DIR = "SOFTWARE\ExaminationTimer"
PRE_EXECUTED_FILE = 'user_data.lic'
REG_FILE_NAME = 'reg_key_data.xml'
LOGO_FILE_NAME = "logo.png"

DIR = str(APP_DATA + ROOT_DIR)
PRE_EXECUTED_FILE_DIR = str(DIR + PRE_EXECUTED_FILE)
REG_FILE_DIR = str(DIR + REG_FILE_NAME)
LOGO_FILE_DIR = str(DIR + LOGO_FILE_NAME)

if not path.exists(DIR):
    makedirs(DIR)

LOGO_BASE_URL = "http://i.imgur.com/"

# Variable that stores the information for the specific user
file_write_data = None


# Function that handles the getting and setting of the user data
def authenticate():
    global file_write_data

    # URL that the information is stored at
    reg_data_url = "http://pastebin.com/raw.php?i=PER0wCBM"

    try:
        # Request the URL, and retrieve the info on that page, in this case it is raw text, save it as reg_data.xml
        urllib.request.urlretrieve(reg_data_url, REG_FILE_DIR)
        reg_file_exits = True
    except HTTPError:
        authenticator.contact_error()
        reg_file_exits = False
    except URLError:
        authenticator.contact_error()
        reg_file_exits = False

    if reg_file_exits:
        # Get the authenticator to authenticate the entered reg key
        authenticator.authenticate()

    # Pre-define the index array (list) variable that will store data for the user
    match_data = [None, None, None, None, None]

    # If it returns False, remove the reg_data.xml file, then return False to the place in which it was run.
    if authenticator.get_match_data() is False:
        if reg_file_exits:
            remove(REG_FILE_DIR)
        return False
    # If get_match_data returns anything else, it should be user information
    else:
        # Extract the data from match_data_received from a tuple to a list, as it should be formatted
        match_data[0], match_data[1], match_data[2], match_data[3], match_data[4] = authenticator.get_match_data()

        # In index 4, the code for a logo should be stored, set logo_code to that URL
        logo_code = str(match_data[4])

        try:
            # Request and retrieve the logo from the url and store it as logo.png
            urllib.request.urlretrieve(str(LOGO_BASE_URL + logo_code + ".png"), LOGO_FILE_DIR)
        except HTTPError:
            authenticator.contact_error()
        except URLError:
            authenticator.contact_error()

        # Request a string to be encoded as an MD5 (Hex Digest), store it in encoded_result
        encode_string_general.EncodeString(match_data[3] +
                                           registry.get_reg_value(registry.HKEY_CURRENT_USER, REG_DIR, "reg_key"))

        encoded_result = str(encode_string_general.get_encoded_string_variable())

        # Set the file_write_data to a format of the data that has been retrieved, excluding the image url
        file_write_data = format("%s\n"
                                 "%s\n"
                                 "%s"
                                 % (encoded_result, match_data[1], match_data[2]))

        if reg_file_exits:
            # Remove the reg_info.xml file as there is no longer any need for it
            remove(REG_FILE_DIR)

        # Return true to the place in which this function was called (marking this as a successful validation)
        return True


def write_auth_data():
    # If the file_write_data variable was not still set to None (it has been changed by the authenticate function)
    if file_write_data is not None:
        # If the file path does not exist, create it
        if not path.exists(DIR):
            makedirs(DIR)
        # If the file does not exist, create it, if it does, open it for editing
        pre_authentication = open(PRE_EXECUTED_FILE_DIR, 'w')
        # Delete any content of the file
        pre_authentication.seek(0)
        pre_authentication.truncate()
        # Write the authentication data to the file
        pre_authentication.write(file_write_data)
        # Close the file for writing
        pre_authentication.close()
