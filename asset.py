# This file is part account_asset_interval module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import datetime
from dateutil.relativedelta import relativedelta
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Asset']


class Asset:
    __metaclass__ = PoolMeta
    __name__ = 'account.asset'
    purchase_value = fields.Numeric('Purchase Value',
        digits=(16, Eval('currency_digits', 2)), states={
            'readonly': (Eval('lines', [0]) | (Eval('state') != 'draft')),
            },
        depends=['currency_digits', 'state'])
    frequency_interval = fields.Integer('Frequency Interval',
        states={
            'readonly': (Eval('lines', [0]) | (Eval('state') != 'draft')),
            'invisible': ~(Eval('frequency') == 'interval'),
            'required': (Eval('frequency') == 'interval'),
            },
        depends=['state', 'frequency'],
        help='This interval will be calculate the End Date')

    @classmethod
    def __setup__(cls):
        super(Asset, cls).__setup__()
        interval = ('interval', 'Interval')
        if interval not in cls.frequency.selection:
            cls.frequency.selection.append(interval)

    @staticmethod
    def default_frequency():
        return 'interval'

    @fields.depends('value', 'purchase_value')
    def on_change_value(self):
        if not self.purchase_value:
            self.purchase_value = self.value

    @fields.depends('frequency_interval', 'start_date')
    def on_change_frequency_interval(self):
        # calculate end date from start date and interval
        if not self.start_date:
            self.start_date = datetime.date.today()

        # TODO frequency year

        if self.frequency_interval:
            self.end_date = self.start_date + relativedelta(months=
                (100 / self.frequency_interval))

    @fields.depends('start_date', 'end_date')
    def on_change_with_frequency_interval(self):
        # calculate interval between start and end date

        # TODO frequency year

        if self.start_date and self.end_date:
            months = relativedelta(self.end_date, self.start_date).months
            if months > 1:
                return (100 / months)
            return 100
