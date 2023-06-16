import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reyrey",
    version="0.0.3",
    author="Otto Hanski",
    author_email="otto.hanski@gmail.com",
    description="Library for simulating ABCD matrix optical systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OtHanski/reyrey",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    include_package_data = True
)
