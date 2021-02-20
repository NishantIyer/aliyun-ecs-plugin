#NishantIyer
from setuptools import setup, find_packages

with open("VERSION", "r") as f:
    VERSION = f.read().strip()
    f.close()

setup(
    name="plugin-alibaba-cloud-ecs",
    version=VERSION,
    description="Alibaba Cloud ECS inventory collector",
    long_description="",
    url="https://www.spaceone.dev/",
    author="MEGAZONE SpaceONE Team",
    author_email="admin@spaceone.dev",
    license="Apache License 2.0",
    packages=find_packages(),
    install_requires=["spaceone-core", "spaceone-api", "spaceone-tester", "schematics"],
    zip_safe=False,
)
