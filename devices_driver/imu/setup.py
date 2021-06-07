import setuptools

ignored_dependencies = []


def get_dependencies():
    with open("requirements.txt", "r") as fh:
        requirements = fh.read()
        requirements = requirements.split('\n')
        map(lambda r: r.strip(), requirements)
        requirements = [r for r in requirements if r not in ignored_dependencies]
        return requirements


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imu_measure",
    version="0.0.0",
    description="Measure data from IMU",
    long_description_content_type="text/markdown",
    url="https://github.com/Gamma-Software/CapsuleScripts",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    author="Valentin Rudloff",
    author_email="valentin.rudloff.perso@gmail.com",
    #python_requires=">=3.6",
    packages=setuptools.find_packages(),
    install_requires=get_dependencies(),
    zip_safe=False,
    include_package_data=True,
    project_urls={
        "Source Code": "https://github.com/Gamma-Software/CapsuleScripts",
    },
)
