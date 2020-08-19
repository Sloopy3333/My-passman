from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

long_description = "Pypass a simple cli password manager with encryption"

setup(
    name="My_passman",
    version="0.0.5",
    author="Sampath HN",
    author_email="sampathhn3333@gmail.com",
    url="https://github.com/SampathHN/Pypass",
    description="command line password manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["passman = scripts.Pass_man:main"]},
    scripts=["scripts/Pass_man.py"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords="password manager",
    install_requires=requirements,
    zip_safe=False,
)

