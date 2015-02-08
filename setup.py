from setuptools import setup, find_packages

setup(
    name="2lazy2rest",
    version="0.1.0",
    author="Fabien Devaux",
    author_email="fdev31@gmail.com",
    license="MIT",
    platform="all",
    description="Effortless generation of PDF, HTML & ODT documents from RST (ReStructuredText)",
    long_description=open('README.rst', encoding='utf-8').read(),
    scripts=['mkrst'],
    packages=find_packages(),
    package_data={
            'mkrst_themes': [
                'default/html/*.css',
                'default/html/*.html',
                'default/pdf/*.style',
                'default/odt/*.odt'
                ],
        },
    include_package_data=True,
    url='https://github.com/fdev31/2lazy2rest',
    zip_safe=False,
    keywords=[],
    install_requires=[
            'docutils >= 0.12',
        ],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
