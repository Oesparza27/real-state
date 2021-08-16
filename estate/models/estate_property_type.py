# Copyright 2021, Ventacero							ctrl shit +p init base
# License LGPL-3.0 or later (http:.gnu.org/licenses/lgpt.html)

from odoo import api, fields, models
# se importa fields desde la carpeta odoo fields.py y models.py


class EstatePropertytype(models.Model):
    _name = "estate.property.type"    # nombre tecnico
    _description = "Real State Properties Type"  # nombre Funcional o Comun
    _order="sequence"

    name = fields.Char(
        string="Nombre", 
        required=True,
        default="Unknown",
    )
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
        )
    sequence = fields.Integer(
        default=10,
    )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name="property_type_id"
    )
    offer_count= fields.Integer(
        compute='_computer_offer_count',
        )

    @api.depends("offer_ids")
    def _computer_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
