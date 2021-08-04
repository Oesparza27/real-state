# Copyright 2021, Ventacero
# License LGPL-3.0 or later (http:.gnu.org/licenses/lgpt.html)

from odoo import fields, models
# se importa fields desde la carpeta odoo fields.py y models.py


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"    # nombre tecnico
    _description = "Properties"  # nombre FUncional o Comun

    name = fields.Char(
        string="Nombre", 
        required=True,
        default="Unknown",
    )  
