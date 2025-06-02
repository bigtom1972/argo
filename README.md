#  argo

Argo is a project by implementing agents to achieve goals

## References 

* https://github.com/yanshengjia/ml-road/blob/master/resources/Artificial%20Intelligence%20-%20A%20Modern%20Approach%20(3rd%20Edition).pdf    (About agent)
* https://python.langchain.com/docs/introduction/    (Agent Framework)


## Environment Setup

### uv 

UV is an extremely fast Python package and project manager, written in Rust. It is designed to be a drop-in replacement for pip and venv, with a focus on speed and simplicity. It is also compatible with the Python Package Index (PyPI) and can be used to install packages from PyPI or from local directories.

#### Installation

To install UV, you can use the following command:

```
pip install uv
```

#### Usage
##### Create a new project

You can create a new Python project using the uv init command:
```
uv init argo
cd argo
```
Alternatively, you can initialize a project in the working (existing) directory:

```
cd argo
uv init
```

uv will create the following files:
```
.
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

##### Project structure

A project consists of a few important parts that work together and allow uv to manage your project. In addition to the files created by uv init, uv will create a virtual environment and uv.lock file in the root of your project the first time you run a project command, i.e., uv run, uv sync, or uv lock.

A complete listing would look like:
```
.
├── .venv
│   ├── bin
│   ├── lib
│   └── pyvenv.cfg
├── .python-version
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock
```

##### pyproject.tmol

The pyproject.toml contains metadata about your project

```
pyproject.tmol
```
---
```
[project]
name = "hello-world"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
dependencies = []
```
You'll use this file to specify dependencies, as well as details about the project such as its description or license. You can edit this file manually, or use commands like uv add and uv remove to manage your project from the terminal.

[Python packaging](https://packaging.python.org/en/latest/overview/)


##### uv project environment

When working on a project with uv, uv will create a virtual environment as needed. While some uv commands will create a temporary environment (e.g., uv run --isolated), uv also manages a persistent environment with the project and its dependencies in a .venv directory in the root of your project.

To run a command in the project environment, use uv run. Alternatively the project environment can be activated as normal for a virtual environment.

When uv run is invoked, it will create the project environment if it does not exist yet or ensure it is up-to-date if it exists. The project environment can also be explicitly created with uv sync.

Locking is the process of resolving your project's dependencies into a lockfile. Syncing is the process of installing a subset of packages from the lockfile into the project environment..

```
uv run --locked ...  #Disable automatic locking 
uv run --no-sync ...  #Disable automatic syncing
uv run --isolated ...  #Run in a temporary environment
uv run --frozen ...  #To use the lockfile without checking if it is up-to-date
uv lock ...  #While the lockfile is created automatically, you can also create it manually
uv sync ...  #While the environment is synced automatically, it may also be explicitly synced.

```

#### Example


## Take project langmanus as reference on how to design and implement an agent framework and application.

The LangManus project, hosted at https://github.com/Darwin-lfl/langmanus, is an open-source, community-driven AI automation framework designed to integrate large language models (LLMs) with specialized tools for tasks such as web search, web crawling, and Python code execution.



