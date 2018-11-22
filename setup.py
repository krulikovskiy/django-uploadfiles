from setuptools import setup
import os


def get_packages(package):
    return [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name="django-uploadfiles",
    version=__import__("uploadfiles").__version__,
    description="Мульти аплоад файлес",
    long_description=open('README.rst').read(),
    author="Krulikovskiy Nikita",
    author_email="it@krulikovskiy.com",
    url="https://github.com/krulikovskiy/django-uploadfiles",
    packages=get_packages('uploadfiles'),
    package_data=get_package_data('uploadfiles'),
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
