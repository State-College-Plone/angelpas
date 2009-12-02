from setuptools import setup, find_packages
import os

_product_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Products', 'AngelPas')
version = open(os.path.join(_product_folder, 'version.txt')).read().strip()
if version.endswith('dev'):
    version = version[:-3]

setup(
    name='Products.AngelPas',
    version=version,
    description="AngelPas lets you treat ANGEL-dwelling classes as Plone groups.",
    long_description=open(os.path.join(_product_folder, 'README.txt')).read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Zope2",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory"
    ],
    keywords='web zope plone authentication pas zope2',
    author='WebLion Group',
    author_email='support@weblion.psu.edu',
    url='http://plone.org/products/angelpas',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # Older versions of the following weren't eggified. Including them as requirements would preclude AngelPas's use with them, when in fact they work.
        # 'Products.CMFCore',
        # 'Products.PluggableAuthService',
        # 'Zope2'
    ],
    extras_require={
        # Older versions of Plone weren't eggified. Including them as requirements would preclude AngelPas's use with them, when in fact they work.
        # 'Plone': ['Plone>=3.1.3']  # Plone-savvy but also works with raw Zope 2
    },
    entry_points={}
)
