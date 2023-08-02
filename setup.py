from cx_Freeze import setup, Executable

setup(
        name = "Pixel Blitz",
        version = "0.1",
        description = "2D Shooting game.",
        options={"build_exe": {"packages":["pygame"],"include_files":["Assets", "Levels"], "build_exe": "E:/Pixel Blitz/Files"}},
        executables = [Executable("main.py", base = "Win32GUI"), Executable("WorldEvents.py"), Executable("JsonHandler.py"), Executable("Log.py"), Executable("LevelEditor.py", base = "Win32GUI")]
)