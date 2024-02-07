from setuptools import setup, find_packages

setup(name='ropeat',
        version='v0.0.0',
<<<<<<< HEAD
        packages=find_packages())
=======
        packages=find_packages(),
        package_data={'ropeat/models': ['*.pkl']},
        include_package_data=True)
>>>>>>> 0e7c526 (first commit new branch fixing model push issues due to large file size)
