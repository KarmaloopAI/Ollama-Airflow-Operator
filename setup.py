from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='airflow-ollama',
    version='0.11.0',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'apache-airflow>=2.0.0',
        'requests>=2.25.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'flake8>=3.9',
        ],
    },
    author='Abi Chatterjee',
    author_email='abhishek.chatterjee@live.com',
    description='Airflow operator for managing Ollama and ngrok',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KarmaloopAI/Ollama-Airflow-Operator',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    keywords='airflow ollama ngrok operator',
)
