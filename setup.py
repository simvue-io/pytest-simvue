from setuptools import setup
import codecs

setup(
    name="pytest-simvue",
    description=(
        "pytest-simvue allows you to upload pytest runs to Simvue"
    ),
    long_description=codecs.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    version="0.1.0",
    url="",
    project_urls={
        "Issue Tracker": "",
    },
    license="MIT",
    author="",
    author_email="",
    py_modules=["pytest_simvue"],
    entry_points={"pytest11": ["simvue = pytest_simvue.plugin"]},
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["pytest>=6.2.0", "termcolor>=2.1.0", "packaging>=21.3", "simvue @ git+ssh://git@github.com/simvue-io/client@dev#egg=simvue"],
    extras_require={
        "dev": []
    },
    classifiers=[
        "Framework :: Pytest",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
    ],
)