import setuptools
import github_stats

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="github_stats",
        version=github_stats.__version__,
        author="dbeley",
        author_email="dbeley@protonmail.com",
        description="Extract statistics from github repos",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dbeley/github_stats",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "github_stats=github_stats.__main__:main"
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
            ],
        install_requires=[
            'PyGithub',
            ]
        )
