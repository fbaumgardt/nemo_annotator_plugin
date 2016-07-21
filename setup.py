from setuptools import setup, find_packages

setup(
    name='nemo_annotator_plugin',
    version="0.0.1",
    packages=find_packages(exclude=["examples", "tests"]),
    url='https://github.com/fbaumgardt/nemo_annotator_plugin',
    license='GNU GPL',
    author='Frederik Baumgardt',
    author_email='baumgardt@informatik.uni-leipzig.de',
    description='Plugin for Capitains Nemo to load Perseids Annotator on passage page',
    test_suite="tests",
    install_requires=[
        "flask_nemo>=1.0.0b1"
    ],
    tests_require=[
        "capitains_nautilus>=0.0.5"
    ],
    include_package_data=True,
    zip_safe=False
)