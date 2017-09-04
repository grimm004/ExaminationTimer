# Encode General String
# 06/06/2015 | All rights Reserved
# @version: 0.5
# @author Max Grimmett, 10.3

import hashlib

# Pre-define encoded string variable
md5out = None


class EncodeString:
    def __init__(self, string_variable):
        # Define global variable md5out
        global md5out
        # Make and store md5 code
        md5 = hashlib.md5()
        md5.update(bytes(string_variable, 'utf-8'))
        md5out = md5.hexdigest()


# Return the pre-defined md5out variable if function called
def get_encoded_string_variable():
    return str(md5out)

# Run test code if the module is directly run
if __name__ == '__main__':
    string_var = b"Test String"

    EncodeString(string_var)
    print(get_encoded_string_variable())
