from setuptools import setup, find_packages

# https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications

setup(
    name="python-project-skeleton",
    version="0.1",

    description='''This is a template description for a new project.''',

    author='Oksana Korol',
    author_email='okorol@gmail.com',

    url='https://github.com/oxyko/python-project-skeleton',

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),


    packages=find_packages(exclude=['test*', 'Test*']),

    package_data={
        '': ['README.md', 'LICENSE'],
        'python-project-skeleton': ['config.yaml.sample']
      },


    scripts=['main.py'],

    entry_points={
          'console_scripts': [
              'python-project-skeleton = main:main',
          ],
      },

    install_requires=[
        'PyYAML==4.2b1',
      ],


)
