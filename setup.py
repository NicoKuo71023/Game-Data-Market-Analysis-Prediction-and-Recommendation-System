from setuptools import setup, find_packages

setup(
    name='BDSE35_final_project',
    version='1.0',
    packages=find_packages(),  # 自動尋找模組
    install_requires=[  # 列出所有需要的依賴
        'pymysql',
        # 其他依賴...
    ],
)
