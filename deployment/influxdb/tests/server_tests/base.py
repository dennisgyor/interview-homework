# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from influxdb.tests import using_pypy
from influxdb.tests.server_tests.influxdb_instance import InfluxDbInstance

from influxdb.client import InfluxDBClient

if not using_pypy:
    from influxdb.dataframe_client import DataFrameClient


def _setup_influxdb_server(inst):
    inst.influxd_inst = InfluxDbInstance(
        inst.influxdb_template_conf,
        udp_enabled=getattr(inst, 'influxdb_udp_enabled', False),
    )

    inst.cli = InfluxDBClient('localhost',
                              inst.influxd_inst.http_port,
                              'root',
                              '',
                              database='db')
    if not using_pypy:
        inst.cliDF = DataFrameClient('localhost',
                                     inst.influxd_inst.http_port,
                                     'root',
                                     '',
                                     database='db')


def _teardown_influxdb_server(inst):
    remove_tree = sys.exc_info() == (None, None, None)
    inst.influxd_inst.close(remove_tree=remove_tree)


class SingleTestCaseWithServerMixin(object):
    """ A mixin for unittest.TestCase to start an influxdb server instance
    in a temporary directory **for each test function/case**
    """

    # 'influxdb_template_conf' attribute must be set
    # on the TestCase class or instance.

    setUp = _setup_influxdb_server
    tearDown = _teardown_influxdb_server


class ManyTestCasesWithServerMixin(object):
    """ Same than SingleTestCaseWithServerMixin
    but creates a single instance for the whole class.
    Also pre-creates a fresh database: 'db'.
    """

    # 'influxdb_template_conf' attribute must be set on the class itself !

    @classmethod
    def setUpClass(cls):
        _setup_influxdb_server(cls)

    def setUp(self):
        self.cli.create_database('db')

    @classmethod
    def tearDownClass(cls):
        _teardown_influxdb_server(cls)

    def tearDown(self):
        self.cli.drop_database('db')