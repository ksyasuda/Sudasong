import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sudasong", # Replace with your own username
    version="0.0.2",
    author="Kyle Yasuda (sudacode)",
    author_email="the.sudacode@gmail.com",
    description="Downloads a song and album and places it in the right place",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ksyasuda/sudasong",
    project_urls={
        "Bug Tracker": "https://github.com/ksyasuda/sudasong/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
