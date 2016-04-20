from setuptools import setup

setup(name='stanford_corenlp_python_wrapper',
      version='0.1',
      description='A python wrapper for Stanford CoreNLP',
      url='http://github.com/askmyhat/stanford-corenlp-python-wrapper',
      author='Askhat Nuriddinov',
      author_email='askhat@askhat.ru',
      license='MIT',
      packages=['stanford_corenlp_python_wrapper'],
      install_requires=[
          'pexpect',
      ],
      zip_safe=False)
