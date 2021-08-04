# Copyright 2021, Ventacero
# License LGPL-3.0 or later (http:.gnu.org/licenses/lgpt.html)

from odoo import fields, models
# se importa fields desde la carpeta odoo fields.py y models.py


class EstateProperty(models.Model):
    _name = "estate.property"    # nombre tecnico
    _description = "Properties"  # nombre FUncional o Comun

    name = fields.Char(
        string="Nombre", 
        required=True,
        default="Unknown",
    )  
    # definir variable name con nombre por default
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(
            fields.Date.today(), months=+3) 
    )
    expected_price = fields.Float(required=True)
    Selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedroms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        # aqui se definen los nombres tecnicos y funcionales de la seleccion.
    )
    active = fields.Boolean(
        default=True,
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Offer Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
        copy=False,
    )     

    # Many2One de muchos a uno por ejemplo un vendedor o un comprador a los 
    # registros dados de alta
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        )
    # campos relacional por estandar siempre termina en _id
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False,
        )
    # Res.partner es el modelo generico que usa Odoo siempre sera asi. Clientes 
    # o Partner que no pertenezcan al sistema usu usuario cuando se crea en 
    # automatico se debe de crear una partner 
    seller_id = fields.Many2one(
        comodel_name='res.users',
        default=lambda self: self.env.user,
        string='Vendedor o Salesman',
        )
    # res.users es esl vendedor que es el usuario del sistema
    # self.env.user son las variables de entorno que tiene el sistema fecha, 
    # usuarios etc.
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string="Tags",
        )
