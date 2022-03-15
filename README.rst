.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/k8s-annotations-exporter.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/k8s-annotations-exporter
    .. image:: https://readthedocs.org/projects/k8s-annotations-exporter/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://k8s-annotations-exporter.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/k8s-annotations-exporter/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/k8s-annotations-exporter
    .. image:: https://img.shields.io/pypi/v/k8s-annotations-exporter.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/k8s-annotations-exporter/
    .. image:: https://img.shields.io/conda/vn/conda-forge/k8s-annotations-exporter.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/k8s-annotations-exporter
    .. image:: https://pepy.tech/badge/k8s-annotations-exporter/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/k8s-annotations-exporter
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/k8s-annotations-exporter

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

========================
k8s-annotations-exporter
========================


    Export k8s resource annotations as Prometheus metric labels

Installation
************

Install directly from the `main` branch:

``pip install https://github.com/4n4nd/k8s-annotations-exporter/zipball/main``


CLI help
********

After installing the package,
you should be able to run this tool by executing ``k8s_annotations_exporter``.

Output for ``k8s_annotations_exporter --help``:

::

    usage: k8s_annotations_exporter [-h] [--version] [--kube-config-file KUBE_CONFIG_FILE] [--metrics-refresh-interval METRICS_REFRESH_INTERVAL]
                                    [--http-server-port HTTP_SERVER_PORT] [--resource-api-version RESOURCE_API_VERSION] [--resource-kind RESOURCE_KIND] [-v] [-vv]

    Exporter to export Kubernetes resource annotations as Prometheus metrics

    options:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    --kube-config-file KUBE_CONFIG_FILE
                            Kube config file location. If no argument provided, the config will be loaded from default location.
    --metrics-refresh-interval METRICS_REFRESH_INTERVAL
                            Metric data refresh interval in seconds
    --http-server-port HTTP_SERVER_PORT
                            Port number to start the metrics HTTP server. Default: 8000
    --resource-api-version RESOURCE_API_VERSION
                            Kubernetes resource API version. Default: v1
    --resource-kind RESOURCE_KIND
                            Kubernetes resource kind. Default: Namespace
    -v, --verbose         set loglevel to INFO
    -vv, --very-verbose   set loglevel to DEBUG


.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd k8s-annotations-exporter
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.1.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
