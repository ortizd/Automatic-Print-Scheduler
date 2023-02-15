# from cx_Freeze import setup, Executable

# setup(name="Automatic Print",
#       version="1.0",
#       description="monitors a designated folder and promptly sends any new file to the printer",
#       executables=[Executable("MainGUI.pyw")],
#       options={"build_exe": {"include_files": ["config.json", "printer.ico"]}})
from cx_Freeze import setup, Executable

exe = Executable(
    script="MainGUI.pyw",
    base="Win32GUI",
    targetName="AutomaticPrint.exe",
    icon="printer.ico"
)

setup(
    name="Automatic Print",
    version="1.1",
    description="monitors a designated folder and promptly sends any new file to the printer",
    executables=[exe],
    options={
        "build_exe": {
            "include_files": ["config.json", "printer.ico"],
            "packages": ["os"],
            "include_msvcr": True,
        }
    }
)
