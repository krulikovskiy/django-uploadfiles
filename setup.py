from setuptools import setup, find_packages

setup(
    name="django-uploadfiles",
    version=__import__("uploadfiles").__version__,
    description="Мульти аплоад файлес",
    long_description=open('README.rst').read(),
    author="Krulikovskiy Nikita",
    author_email="it@krulikovskiy.com",
    url="https://github.com/krulikovskiy/django-uploadfiles",
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    license='BSD',
    install_requires=[
        'django>=2.0',
    ],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
