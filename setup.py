from setuptools import setup, find_packages

setup(
    name='momapa',
    version='0.2',
    description='Simple library to parse and use Minecraft manifests',
    author='oxodao',
    license='GPLv3',
    keywords=['Minecraft', 'Mojang', 'Manifest', 'Parser', 'Spectrum'],
    url='https://github.com/Spectrum-MC/momapa',
    packages=find_packages(),
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.2.0'],
    test_suite='tests',
)