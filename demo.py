# from cbp.exception import HousingException
# from cbp.logger import logging
# import sys

# try:
#     logging.info("Logging is working and we are in try block")
#     raise Exception("This is trial Exception")
# except Exception as e:
#     # logging.INFO("loggin in Except block")
#     raise HousingException(e, sys) from e

# import gdown

# url = 'https://drive.google.com/file/d/13TMxd_l4MdDVY7BZnfXSrRqSTOe3t1c2/view?usp=share_link"'
# output = 'data.tgz'
# gdown.download(url, output, quiet=False)

import tarfile
with tarfile.open("data.tgz") as housing_tgz_file_obj:
    housing_tgz_file_obj.extractall(path="/")