from setuptools import setup, find_packages

# import subprocess
# version = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
# # Normalise version string to be compliant with PEP 440:
# if version[0] == 'v': version = version[1:]
# version = version.replace('-', '+', 1)
# version = version.replace('-', '.')
version = 'v0.0.1'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='povray',
    version=version,
    license='GNU General Public License v3.0',

    author='Joshua Robinson',
    author_email='joshuarrr@protonmail.com',

    url='https://github.com/tranqui/povray.git',
    description='Scripts to generate povray input scripts ready for 3d rendering via ray-tracing',
    long_description=long_description,
    long_description_content_type="text/markdown",

    python_requires='>=3',
    ext_modules=[],
    install_requires=['numpy', 'scipy'],
    #package_dir={'': 'src'},
    packages=find_packages(),
 )
