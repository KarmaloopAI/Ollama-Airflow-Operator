from setuptools import setup, find_packages

setup(
    name='airflow-ollama',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'apache-airflow>=2.0.0',
    ],
    author='Abi Chatterjee',
    author_email='your.email@example.com',
    description='Airflow operator for managing Ollama and ngrok',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KarmaloopAI/Ollama-Airflow-Operator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
