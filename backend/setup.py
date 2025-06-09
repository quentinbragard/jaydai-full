from setuptools import setup, find_packages

setup(
    name='archimind_backend',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'archimind_backend = main:main',
        ],
    },
    author='Quentin Bragard',
    author_email='quentin@jayd.ai',
    description='Archimind FastAPI backend app.',
    url='https://github.com/quentinbragard/archimind-backend',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
) 