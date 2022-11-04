import cx_Freeze


# Meu comando para gerar o executável:
# C:\Users\Cliente\AppData\Local\Programs\Python\Python38\python setup.py build

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('main.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "Jogo Grupo 5",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['audio/', 'code/', 'graphics/']}},
    executables = executables
)