from distutils.core import setup

setup(
    name="cd_price_finder",
    version="0.1dev",
    packages=['cd_price_finder'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'cdpf_test=cd_price_finder.scripts:cdpf_test',
        ],
    }
)