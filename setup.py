import io

from setuptools import find_packages, setup

setup(
    name='wagtail_lightadmin',
    version='0.11',
    description='A lighter admin for wagtail',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    keywords=['wagtail', 'admin', 'light'],
    author='Christine Ho (Leukeleu)',
    author_email='cho@leukeleu.nl',
    maintainer='Leukeleu',
    maintainer_email='info@leukeleu.nl',
    url='https://github.com/leukeleu/wagtail_lightadmin',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='MIT',
    install_requires=[
        'wagtail>=2.0',
    ],
    include_package_data=True,
    zip_safe=False
)
