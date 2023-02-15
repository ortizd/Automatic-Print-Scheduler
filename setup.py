from cx_Freeze import setup, Executable

setup(name="Automatic Print",
      version="1.0",
      description="monitors a designated folder and promptly sends any new file to the printer",
      executables=[Executable("MainGUI.pyw")],
      options={"build_exe": {"include_files": ["config.json", "image.ico"]}})
