from setuptools import setup
import re


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('anime_relations_py/__init__.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name="anime-relations-py",
    author='Tyler',
    url="https://github.com/tylergibbs2/anime-relations-py",
    project_urls={
        "Documentation": "https://github.com/tylergibbs2/anime-relations-py/blob/master/README.md",
        "Issue tracker": "https://github.com/tylergibbs2/anime-relations-py/issues",
    },
    version=version,
    license='MIT',
    description="A parser for anime-relations. So you don't have to.",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
