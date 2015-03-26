from setuptools import setup, find_packages

dependencies = ['Flask']


setup(
    name = "s0_graph",
    version = "0.01",
    author = "afroisalreadyinu",
    install_requires = dependencies,
    packages=find_packages(),
    zip_safe=False,
)
