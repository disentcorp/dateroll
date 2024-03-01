from setuptools import find_packages, setup

setup(
    name="dateroll",
    version="0.0.22",
    description="""dateroll makes working with dates less painful.""",
    author="Anthony Malizzio",
    author_email="anthony.malizzio@disent.com",
    license = "Apache Software License",
    url="https://github.com/disentcorp/dateroll",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        'Operating System :: Unix',
    ],
    packages=['dateroll','dateroll.ddh','dateroll.calendars','dateroll.duration','dateroll.parser','dateroll.schedule','dateroll.date'],
    include_package_data=True,
    package_data={
        'dateroll':['sampledata/*.csv','tests/*']
    },
    install_requires=["python-dateutil"],
    license_files = ('LICENSE',),
    python_requires=">=3.7",
    zip_safe=False
)
