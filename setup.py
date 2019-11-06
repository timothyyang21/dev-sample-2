import cx_Freeze

executables = [cx_Freeze.Executable("start_game.py")]

cx_Freeze.setup(
    name="Row Reduction Game",
    options={"build_exe": {"packages":["pygame", "math", "random"], 
                           "include_files":["constants.py", "Game.py"]}},
    executables = executables

    )