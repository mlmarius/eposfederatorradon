# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='eposfederator.federators.radon',  # Required
    version='0.0.1',  # Required
    description='Epos Federation for the Radon APIs',  # Required
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={'eposfederator.federators': 'radon = eposfederator.federators.radon'},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
    package_data={'eposfederator.federators.radon': ['settings.yml']}
)
