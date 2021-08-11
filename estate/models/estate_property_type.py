# Copyright 2021, Ventacero							ctrl shit +p init base
# License LGPL-3.0 or later (http:.gnu.org/licenses/lgpt.html)

from odoo import fields, models
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
