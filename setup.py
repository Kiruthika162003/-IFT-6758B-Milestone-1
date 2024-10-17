from setuptools import find_packages, setup

setup(
    name='ift6758_project',
    version='0.1.0',
    description='IFT 6758 Project: Milestone 1 - Data Wrangling and Exploratory Data Analysis on NHL Data',
    author='Kiruthika Subramani, Tikshan Kumar, Yizhan Li',
    author_email=(
        "kiruthika.subramani@umontreal.ca, "
        "tikshan.kumar.soobanah@umontreal.ca, "
        "yizhan.li@mail.mcgill.ca"
    ),
    url="https://github.com/your-github-repo",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.2",
        "seaborn>=0.11.2",
        "requests>=2.26.0",
        "opencv-python>=4.5.3.56",
        "tqdm>=4.61.0",
        "lxml>=4.6.3",
        "plotly>=5.1.0",
        "ipywidgets>=7.6.3",
        "ipykernel>=6.0.0",
        "jupyterlab>=3.0.0",
        "setuptools>=52.0.0",
        "scipy>=1.7.0",
        "rich>=10.0.0",
        "Pillow>=8.0.0",
        "nbformat",
        "jsonschema",
        "python-dotenv",
        "hockey-rink"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    entry_points={
        "console_scripts": [
            "nhl-data-tool=ift6758.main:main_function",
        ],
    },
)
