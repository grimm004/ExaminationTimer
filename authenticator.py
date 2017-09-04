# Authentication Manager
# 06/06/2015 | All rights Reserved
# @version: 4.0
# @author Max Grimmett (10.3)

from xml.dom import minidom
from os import remove
import encode_licence_key
from urllib import request
from urllib.error import HTTPError
from os import getenv
import pastebin
import registry
import ctypes
import debug

is_debug = False
if debug.MASTER_DEBUG or debug.Authenticator:
    is_debug = True
__DEBUG__ = is_debug

if __DEBUG__:
    print("AUTHENTICATOR: Debugging is enabled.")

"""
from xml.etree import ElementTree

# create XML
root = ElementTree.Element('root')
root.append(ElementTree.Element('child'))
# another child with text
child = ElementTree.Element('child')
child.text = 'some text'
root.append(child)

# pretty string
s = ElementTree.tostring(root)
print(s)
"""

if __DEBUG__:
    print("AUTHENTICATOR: Getting Reg Key")
REG_DIR = "SOFTWARE\ExaminationTimer"
# Variable that stores the entered reg key in reg.txt
licence_code = registry.get_reg_value(registry.HKEY_CURRENT_USER, REG_DIR, "reg_key")

if __DEBUG__:
    print("AUTHENTICATOR: Defining Variables...")
if __DEBUG__:
    print("AUTHENTICATOR: Encoding Reg Key...")
# MD5 encode the entered licence key
encode_licence_key.EncodeKey(licence_code)

# Set the encoded key as a variable for later comparison
encrypted_code = str(encode_licence_key.get_encoded_licence_key())
# Pre define user-specific variables
holder_name_short = None
holder_name_long = None
holder_licence_type = None
holder_logo_url = None

# Variables that store if the key has passed or not
key_pass_one = False
key_pass_two = False

# Create directory and file strings
APP_DATA = getenv('APPDATA')
ROOT_DIR = '\\ExaminationTimer\\'
REG_KEY_FILE_NAME = 'reg_key_data.xml'
REG_USER_DATA_FILE_NAME = 'reg_user_data.xml'

DIR = str(APP_DATA + ROOT_DIR)
REG_KEY_FILE_DIR = str(DIR + REG_KEY_FILE_NAME)
REG_USER_DATA_FILE_DIR = str(DIR + REG_USER_DATA_FILE_NAME)
if __DEBUG__:
    print("AUTHENTICATOR: Done!")


def contact_error(error_type=0):
    if __DEBUG__:
        print("AUTHENTICATOR: Error called with code %d" % error_type)
    if error_type == 0:
        message_box = ctypes.windll.user32.MessageBoxW
        message_box(None, "There was a problem while contacting the servers for user information.\n"
                          "Please check connection to http://pastebin.com and try again.\n"
                          "If the problem persists please contact grimm004@gmail.com",
                    "Authentication Error", 0)
    elif error_type == 1:
        message_box = ctypes.windll.user32.MessageBoxW
        message_box(None, "There was no data found for this key, either it has already been used, "
                          "or it is incorrect. For assistance please contact grimm00@gmail.com",
                    "Authentication Error", 0)


def authenticate():
    global holder_name_short, holder_name_long, holder_licence_type, holder_logo_url, key_pass_one, key_pass_two
    try:
        if __DEBUG__:
            print("AUTHENTICATOR: Opening XML Document")
        # Open the xml file that stores the licence urls
        xml_doc = minidom.parse(REG_KEY_FILE_DIR)

        if __DEBUG__:
            print("AUTHENTICATOR: Getting amount of licence holders")
        # Get the amount of licence holders variable
        amount_of_licence_holders = int(xml_doc.getElementsByTagName("amount_of_licence_holders")[0].firstChild.data)

        if __DEBUG__:
            print("AUTHENTICATOR: Opening licence_holders elements")
        # Enter the licence holders tag section of the file
        licence_holders = xml_doc.getElementsByTagName("licence_holders")[0]

        if __DEBUG__:
            print("AUTHENTICATOR:")
        # Cycle through the licence holders
        for x in range(amount_of_licence_holders):
            # Enter the licence holder index for the index that the loop is at
            licence_holder = licence_holders.getElementsByTagName("licence_holder")[x]
            # Load in the encrypted real key value as a string
            licence_holder_str = str(licence_holder.getElementsByTagName("key_value")[0].firstChild.data)
            # Check if the encrypted real key (licence_holder_str) is in the encrypted entered key (encrypted_code)
            if licence_holder_str in encrypted_code:
                # Mark as having passed stage one
                key_pass_one = True

                # Get the specific url for the licence holder's information
                reg_data_url = str(licence_holder.getElementsByTagName("holder_url")[0].firstChild.data)

                paste_key = pastebin.get_paste_code(reg_data_url)

                try:
                    # Try request the URL, and retrieve the info on that page, in this case it is raw text
                    request.urlretrieve(reg_data_url, REG_USER_DATA_FILE_DIR)
                    # Mark as having passed stage two
                    key_pass_two = True
                except HTTPError:
                    # If paste is unreachable, mark as having not passed stage two
                    key_pass_two = False

                    contact_error(1)

                if key_pass_two:
                    # Open the xml file that stores the licence data
                    xml_user_doc = minidom.parse(REG_USER_DATA_FILE_DIR)

                    # Enter the licence holders tag section of the file
                    user_licence_holder = xml_user_doc.getElementsByTagName("licence_holder")[0]

                    # Extract all the necessary variables for the specific user
                    holder_name_short = str(user_licence_holder.getElementsByTagName("holder_name_short")[0]
                                            .firstChild.data)
                    holder_name_long = str(user_licence_holder.getElementsByTagName("holder_name_long")[0]
                                           .firstChild.data)
                    holder_licence_type = str(user_licence_holder.getElementsByTagName("holder_licence_type")[0]
                                              .firstChild.data)
                    holder_logo_url = str(user_licence_holder.getElementsByTagName("holder_logo")[0]
                                          .firstChild.data)

                    if __DEBUG__:
                        print("AUTHENTICATOR: Deleting private data paste.")
                    # Delete the user info xml file from pastebin.com
                    pastebin.delete_paste('25d7dfb34518d7f91d31eff4be1d12b8',
                                          '958fa0629dd8cc2e23725161f9c0620b',
                                          paste_key)

                    # Delete the local user info xml file
                    remove(REG_USER_DATA_FILE_DIR)
    except FileNotFoundError:
        pass


def get_match_data():
    if key_pass_one and key_pass_two:
        return True, holder_name_short, holder_name_long, holder_licence_type, holder_logo_url
    else:
        return False
