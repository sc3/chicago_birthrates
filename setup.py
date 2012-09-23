from distutils.core import setup

setup(
    name='Chicago Birthrates',
    version='0.1',
    author=u'David Eads',
    author_email='davideads@gmail.com',
    packages=['chicago_birthrates'],
    url='https://github.com/sc3/chicago_birthrates',
    license='GPLv3, see LICENSE.md',
    description= 'Chicago birth rates, 1999-2009.'
    long_description=open('README.md').read(),
    zip_safe=False,
)

