from odoo import fields, models, api, _
from odoo.exceptions import UserError
import re


class ExamenesModel(models.Model):
    _name = 'examenes'
    _description = 'Crud De examenes'
    _rec_name = 'nombre_examen'

    codigo_examen = fields.Char(
        string='Codigo Examen',
        required=True,
        size=10
    )
    nombre_examen = fields.Char(
        string='Nombre Examen',
        required=True)

    tarifa_id = fields.One2many(
        comodel_name='tarifa.examenes',
        inverse_name='examenes_id',
        string='Listado De Tarifa'
    )

    _sql_constraints = [('examen_unique',
                         'unique(codigo_examen',
                         'El Codigo Examen Debe Ser Unico')]