from setuptools import setup, find_packages

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Varsha gowda',
    author_email='varsha1787062@gmail.com',
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
