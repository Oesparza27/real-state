# Copyright 2021, Ventacero
# License LGPL-3.0 or later (http:.gnu.org/licenses/lgpt.html)

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many(
            comodel_name="estate.property",
            inverse_name="seller_id",
            domain=[('state', 'not in', ['sold', 'canceled'])],

    )
