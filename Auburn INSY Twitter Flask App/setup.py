
import os
import sys
import datetime
import requests.certs

from cx_Freeze import setup, Executable

# This is ugly. I don't even know why I wrote it this way.
def files_under_dir(dir_name):
    file_list = []
    for root, dirs, files in os.walk(dir_name):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list


includefiles = []
for directory in ('static', 'templates'):
    includefiles.extend(files_under_dir(directory))

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = None

dt = datetime.datetime.now()

main_executable = Executable("MainApp.py", base=base)
setup(name="Mainapp",
      version="0.1." + dt.strftime('%m%d.%H%m'),
      description="Example Twitter App",
      options={
          'build_exe': {
              'packages': ['jinja2.ext',
                           'os',
						   'twython','re','textblob','flask','ssl','cryptography', 'pyopenssl', 'ndg-httpsclient','pyasn1'],
              'include_files': includefiles,
              'include_msvcr': True}},
      executables=[main_executable], requires=['flask', 'wtforms'])