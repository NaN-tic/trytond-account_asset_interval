# This file is part account_asset_interval module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
import datetime
from dateutil.relativedelta import relativedelta
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import doctest_setup, doctest_teardown
from trytond.tests.test_tryton import doctest_checker
from trytond.pool import Pool


class AccountAssetIntervalTestCase(ModuleTestCase):
    'Test Account Asset Interval module'
    module = 'account_asset_interval'

    @with_transaction()
    def test_interval(self):
        'Test interval'
        Asset = Pool().get('account.asset')

        today = datetime.date.today()

        asset = Asset()
        asset.start_date = today

        # interval 50
        asset.frequency_interval = 50
        asset.on_change_frequency_interval()
        self.assertEqual(asset.end_date, today + relativedelta(months=2))

        # interval 10
        asset.frequency_interval = 10
        asset.on_change_frequency_interval()
        self.assertEqual(asset.end_date, today + relativedelta(months=10))

        # start/end date
        asset = Asset()
        asset.start_date = today
        asset.end_date = today + relativedelta(months=10)
        interval = asset.on_change_with_frequency_interval()
        self.assertEqual(asset.on_change_with_frequency_interval(), 10)

        # TODO frequency year

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountAssetIntervalTestCase))
    return suite
