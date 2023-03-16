from setuptools import setup, find_packages

setup(
    name="assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "assistant=assistant.assistant:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    license="MIT",
    description="ChatGPT Console UI",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
)
