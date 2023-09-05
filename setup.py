import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='llmbox',
    version='0.3.1',
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
    python_requires='>=3.10',
    install_requires=[
        'anthropic',
        'openai'
    ],
    packages=setuptools.find_packages(),
    license='Apache License, Version 2.0',
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    keywords=[
        'artificial intelligence',
        'large language model',
        'llm',
        'machine learning',
        'nocode'
    ]
)
