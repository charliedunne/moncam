"""Create password hash
"""

################################################################################
# IMPORTS
################################################################################

import hashlib
import os
import pickle


################################################################################
# GLOBALS
################################################################################

USER_PASS='/home/pi/moncam/webapp/private/pass_user'


################################################################################
# DEFINITIONS
################################################################################

def main():

    # Open the output file
    f_out = open(USER_PASS, 'wb')

    # Request the password to the user
    password = input("Type your password: ")

    # Hash it
    md5_pwd = hashlib.md5(password.encode('utf8')).hexdigest()

    # Stream the password and output to file
    pickle.dump(md5_pwd, f_out)

    # Close the file
    f_out.close()


################################################################################
# MAIN
################################################################################

if __name__ == '__main__':

    main()

