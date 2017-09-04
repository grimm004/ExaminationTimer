import sys
from cx_Freeze import setup, Executable

build_exe_options = {"include_files":
                     ["icon.ico",
                      "logo_default.png",
                      "YMS.wav",
                      "5MR.wav",
                      "EOE.wav"],
                     "icon":
                     "icon.ico"}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Examination Timer",
      version="6.00",
      description="Countdown timer for use during examinations.",
      author='Max Grimmett',
      author_email='grimm004@gmail.com',
      options={"build_exe": build_exe_options},
      executables=[Executable("ExaminationTimer.py", base=base)])
