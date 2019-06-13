import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aec',
    version='0.1.3',
    scripts=['aec'],
    author="Joao Gilberto Magalhaes",
    author_email="joao@byjg.com.br",
    description="ActiveMQ Easy Config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byjg/activemq-easy-config",
    packages=setuptools.find_packages(),
    install_requires=open("requirements.txt", 'r').readlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
