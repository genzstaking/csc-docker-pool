"""
    Setup file for csc-docker-pool.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup


def local_scheme(version):
    return ""


if __name__ == "__main__":
    try:
        setup(
            use_scm_version={
                "root": ".",
                "local_scheme": local_scheme
            },
            setup_requires=['setuptools_scm']
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
