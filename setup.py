# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

from setuptools import find_packages, setup


run_requirements = [
    "black==22.6.0",
    "click==8.1.3",
    "defusedxml==0.7.1",
    "loguru==0.6.0",
    "mypy-extensions==0.4.3",
    "numpy==1.23.1",
    "odfpy==1.4.1",
    "pandas==1.4.3",
    "pathspec==0.9.0",
    "platformdirs==2.5.2",
    "psycopg==3.0.15",
    "psycopg2==2.9.3",
    "pydantic==1.9.1",
    "python-dateutil==2.8.2",
    "pytz==2022.1",
    "six==1.16.0",
    "tomli==2.0.1",
    "typing_extensions==4.3.0",
]

setup(
    name="Projeto Final FBD",
    version="1.0.0",
    author="Kevin de Santana Araujo",
    author_email="kevin_santana.araujo@hotmail.com",
    packages=find_packages(exclude=["docs", "tests"]),
    url="https://github.com/kevinsantana/projeto-final-fbd/",
    description="Projeto Final da Disciplina FBD",
    long_description="long_description",
    long_description_content_type="text",
    install_requires=run_requirements,
    python_requires=">=3.10.4",
)
