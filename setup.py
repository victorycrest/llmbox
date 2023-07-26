import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read()

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='llmbox',
    version=version,
    author='Victory Crest',
    author_email='victorycrest1602@gmail.com',
    description='LLMs at your service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/victorycrest/llmbox',
    project_urls={
        'Source': 'https://github.com/victorycrest/llmbox',
        'Tracker': 'https://github.com/victorycrest/llmbox/issues'
    },
    python_requires='>=3.8',
    install_requires=[
        'anthropic'
    ],
    packages=setuptools.find_packages(),
    license='Apache License, Version 2.0',
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'artificial intelligence',
        'large language model',
        'llm',
        'machine learning',
        'nocode'
    ]
)
