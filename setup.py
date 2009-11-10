from setuptools import setup, find_packages
import os

version = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Products', 'AngelPas', 'version.txt')).read().strip()
if version.endswith('dev'):
    version = version[:-3]

setup(
    name='Products.AngelPas',
    version=version,
    description="AngelPas lets you treat ANGEL-dwelling classes as Plone groups.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    url='http://weblion.psu.edu/svn/weblion/weblion/AngelPas',
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