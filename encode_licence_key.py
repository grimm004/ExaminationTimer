# Encode Licence Key
# 06/06/2015 | All rights Reserved
# @version: 0.5
# @author Max Grimmett, 10.3

import hashlib

# Pre-define encoded string variable
md5sum = None


class EncodeKey:
    def __init__(self, reg_code):
        # Define global variable md5out
        global md5sum
        # Make and store md5 code
        md5 = hashlib.md5()
        md5.update(bytes(reg_code, 'utf-8'))
        md5sum = md5.hexdigest()


# Return the pre-defined md5out variable if function called
def get_encoded_licence_key():
    return str(md5sum)

# Run test code if the module is directly run
if __name__ == '__main__':
    licence_code = b"Code"

    EncodeKey(licence_code)
    print(get_encoded_licence_key())
