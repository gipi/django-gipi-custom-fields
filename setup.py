from setuptools import setup, find_packages

setup(
    name = "django-gipi-custom-fields",
    version = "0.1",
    url = '',
    license = 'BSD',
    description = "Simple custom fields",
    author = 'Gianluca Pacchiella',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
