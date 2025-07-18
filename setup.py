from setuptools import setup, find_packages

setup(
    name="pwm",
    version="1.0.0",
    description ="A terminal password manager.",

    packages=find_packages(),
        entry_points={            
        'console_scripts': [
            'pwm = pwm.main:main'
        ],
    }, 

    author="hawar",
    author_email="iaramkhzri@gmail.com",

)