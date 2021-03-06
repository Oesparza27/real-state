# Copyright 2021, Ventacero
# License LGPL-3.0 or later (http:.gnu.org/licenses/lgpt.html)

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare
# se importa fields desde la carpeta odoo fields.py y models.py
# importar los mensage de error directamente desde la carpeta de Odoo


class EstateProperty(models.Model):
    _name = "estate.property"    # nombre tecnico
    _description = "Properties"  # nombre FUncional o Comun

    name = fields.Char(
        string="Nombre", 
        required=True,
        default="Unknown",
	    copy=False,
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
    selling_price = fields.Float(
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
        ondelete='restrict',
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

    # manyto many
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string="Tags",
        )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        )

# campos Calculados

    total_area = fields.Float(
        compute='_compute_total_area',
        string='*Area Total',
        )
    best_price = fields.Float(
        compute='_compute_best_price',
        string='*Best Price',
        )
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    validity = fields.Integer(
        default=7,
    )  

    def unlink(self):
        for rec in self:
            if rec.state not in ['new', 'calceled']:
                raise UserError('YOu can no delete this property')
        return super().unlink()



    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         return super().create(vals_list)
                
    #     return super().create(vals_list)
    """metodo que empieza con guion bajo es un metodo privado, que nos e puede 
    ejecutar desde el frontend.
    este es un decorador @es un 
    decorador un decorador es un metodo que se manda llamar antes o despeus 
    de definir el metodo, el depends se encarga de monitorear los campos que 
    se van a mandar, si hay un cambio siempre se van aa ejectuar cuando hay 
    cambio. hay un api onchange qque lo calcula esn frontend"""
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Property Already Exist!"),
        ('expected_price_positive', 'check(expected_price > 0)', "El precio esperado debe de ser mayo a cero"),
        ('selling_price_positive', 'check(selling_price > 0)', "El precio de venta debe de ser mayo a cero"),    
    ]

    # campos calculados inverse, el metodo inverso se calcula cuando se 
    # guarda el campos en la BD
   
    # DEBUG Import ipdb; ipdb.set_trace() Y import web_pdb; web_pdb.set_trace()
    # EL CAMPO STORE=TRUE LO ALMACENA EN LA BD 
    # Y CON ESO SE DEBERIA DE TARDAR MENOS
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            # import web_pdb; web_pdb.set_trace()
            rec.total_area = rec.living_area + rec.garden_area

    # el self son todos los registros de ese objeto
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            best_price = 0
            if rec.offer_ids:
                best_price = max(rec.offer_ids.mapped('price')) 
            rec.best_price = best_price

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.context_today(rec)
            rec.date_deadline = fields.Date.add(
                create_date, days=+rec.validity
            )

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - rec.create_date.date()).days

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.update({
                'garden_area': 10,
                'garden_orientation': 'north'
                })
        else:
            self.update({
                'garden_area': 0,
                'garden_orientation': 'north'
                })
        return{
            'warning': {
                'title': 'Test',
                'message': 'Este es un mensaje de Warning',
            }
        }

    # el metodo update solo actualiza en la BD y el metodo Write escribe en 
    # la BD

    def action_sold(self):
        for rec in self:
            if rec.state == 'canceled':
                raise UserError('No puedes vender una propiedad cancelada')
            rec.state = 'sold'

    def action_canceled(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError('No puedes cancelar una propiedad vendida')
            rec.state = 'canceled'
            # para un mensaje en un boton solamente es necesario usar un raise }
            # porque los warning se ejecutan en frontend

    # @api.constraint esta se utiliza para meterle contrains a nivel de codigo
    # para hacer comparacieones de floats usar float_comprare() float_is_zero()
    # cuando se comp
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            expected_price = rec.expected_price*0.90
            # import ipdb; ipdb.set_trace()

            if rec.selling_price and float_compare(
                    rec.selling_price, expected_price, precision_digits=2
                    ) == -1:
                raise UserError('El precio de venta no debe ser menor al 90%%'
                      'del precio esperado')

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"    # nombre tecnico
    _description = "Real Estate Property Offer"  # nombre FUncional o Comun
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),        
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        required=True,
        ondelete='cascade',
    )
    _sql_constraints = [
        ('price_positive', 'check(price > 0)', "Price Must be Positive!"),
    ]

    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        )

    def action_accept(self):
        for rec in self:
            """if any([x == 'accepted' for x in rec.property_id.offer_ids.mapped('status')]):
                raise UserError('Solo puedes aceptar una oferta')"""
            rec.property_id.write({
                'buyer_id': rec.partner_id.id,
                'selling_price': rec.price,
                })      
            rec.status = 'accepted'

    def action_refused(self):
        for rec in self:
            rec.status = 'refused'
                
    @api.model
    def create (self, vals):
        # import ipdb; ipdb.set_trace()
        estate_property = self.env['estate.property'].browse(vals.get('property_id'))
        max_offer = 0
        prices = estate_property.offer_ids.mapped('price')
        if prices:
            max_offer = max(prices)
        if vals.get('price') < max_offer:
            raise UserError('You can not accepted an offer that is lower than existings ones')
        estate_property.state = 'offer_received'
        return super().create(vals)
