"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = k8s_annotations_exporter.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import time

from kubernetes import client, config, dynamic, watch
from prometheus_client import REGISTRY, start_http_server
from prometheus_client.core import InfoMetricFamily

from k8s_annotations_exporter import __version__

__author__ = "Anand Sanmukhani"
__copyright__ = "Anand Sanmukhani"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

MAX_METRIC_LABEL_VALUE_LENGTH = 100


class CustomCollector:
    def __init__(self, metric_family=None) -> None:
        self.metric_family = metric_family

    def collect(self):
        return [self.metric_family]

    def update(self, metric_family) -> None:
        self.metric_family = metric_family


def fetch_metric_data(k8s_config, search_params):
    metric_data = []

    # Creating a dynamic k8s client
    k8s_client = dynamic.DynamicClient(
        client.api_client.ApiClient(configuration=k8s_config)
    )
    watcher = watch.Watch()

    for e in k8s_client.resources.get(**search_params).watch(
        timeout=5, watcher=watcher
    ):
        resource_metric = {}
        if not e["object"].metadata.annotations:
            continue
        resource_metric["api_version"] = e["object"].apiVersion
        resource_metric["kind"] = e["object"].kind
        resource_metric["name"] = e["object"].metadata.name

        for key, value in e["object"].metadata.annotations:
            resource_metric["annotation_" + key] = value

        metric_data.append(resource_metric)

    # Gracefully stop the stream watcher
    watcher.stop()

    return metric_data


def update_metric(metric_collector, metric_data):
    metric_collector.update(
        InfoMetricFamily(
            "k8s_resource_annotations", "Annotations set in a k8s resource"
        )
    )

    if not metric_data:
        _logger.debug("No resources found")

    for metric in metric_data:
        metric_collector.metric_family.add_metric(metric.keys(), metric)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="""Exporter to export Kubernetes resource annotations
                    as Prometheus metrics"""
    )
    parser.add_argument(
        "--version",
        action="version",
        version="k8s-annotations-exporter {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "--kube-config-file",
        help="""Kube config file location. If no argument provided,
                the config will be loaded from default location.""",
    )
    parser.add_argument(
        "--metrics-refresh-interval",
        help="Metric data refresh interval in seconds",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--http-server-port",
        help="Port number to start the metrics HTTP server. Default: 8000",
        type=int,
        default=8000,
    )
    parser.add_argument(
        "--resource-api-version",
        help="Kubernetes resource API version. Default: v1",
        type=str,
        default="v1",
    )
    parser.add_argument(
        "--resource-kind",
        help="Kubernetes resource kind. Default: Namespace",
        type=str,
        default="Namespace",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    k8s_config = config.load_kube_config(config_file=args.kube_config_file)

    search_params = {
        "api_version": args.resource_api_version,
        "kind": args.resource_kind,
    }
    _logger.info("Kubernetes resource search parameters: {0}".format(search_params))

    metric_collector = CustomCollector(
        InfoMetricFamily(
            "k8s_resource_annotations", "Annotations set in a k8s resource"
        )
    )

    start_http_server(args.http_server_port)
    _logger.info("HTTP server started at port: {0}".format(args.http_server_port))

    REGISTRY.register(metric_collector)

    _logger.info(
        "Metrics will be refreshed every {0} seconds".format(
            args.metrics_refresh_interval
        )
    )
    while True:
        update_metric(metric_collector, fetch_metric_data(k8s_config, search_params))
        REGISTRY.collect()
        _logger.debug("Metrics page updated.")
        time.sleep(args.metrics_refresh_interval)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m k8s_annotations_exporter.export -v
    #
    run()
