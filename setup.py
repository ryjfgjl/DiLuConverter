from cx_Freeze import setup, Executable
import os
import sys

os.environ['TCL_LIBRARY']="F:\\Python37\\tcl\\tcl8.6"
os.environ['TK_LIBRARY']="F:\\Python37\\tcl\\tcl\\tk8.6"

# Dependencies are automatically detected, but it might need
# fine tuning.
base = None
# 判断Windows系统  
#if sys.platform == 'win32':  
#    base = 'Win32GUI'  
  
packages = ["os", "idna", "numpy", "pymysql", "pandas", "numpy", "pycrfsuite","chardet"]
  
for dbmodule in ['win32gui','win32api' ,'win32con' , 'cx_Freeze']:  
  
    try:  
  
        __import__(dbmodule)  
  
    except ImportError:  
  
        pass  
  
    else:  
        packages.append(dbmodule)  
  
  
options = {  
                'build_exe':   
                        {  
                             'includes': 'atexit'  
                             # 依赖的包  
                             ,"packages": packages  
                             # 额外添加的文件  
                             , 'include_files':['config.ini', "common", "excelimporter"]
                            }  
                  
                }  
  
executables = [  
                        Executable(  
                                        # 工程的 入口   
                                        'interface.py'
                                        , base=base  
                                        # 生成 的文件 名字  
                                        , targetName = 'Excel Importer.exe'
                                        # 生成的EXE的图标  
                                       , icon = 'excel.ico' #图标, 32*32px
                                        )  
                    ]  
  
setup(  
            # 产品名称  
           name='Excel Importer',
            # 版本号  
            version='2.0',
            # 产品说明  
            description='Excel Importer',
            options=options,  
            executables=executables  
      )  

