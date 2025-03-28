from setuptools import setup, find_packages

setup(
    name='log-viewer',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A log viewer application with a tree view for browsing log folders and files.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5',
        # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'log-viewer=main:main',  # Assuming main.py has a main function
        ],
    },
)