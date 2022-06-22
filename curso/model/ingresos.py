from odoo import fields, models, api


class IngresosModel(models.Model):
    _name = 'ingresos'
    _description = 'Ingresos de pacientes'
    _rec_name = 'nombre_tarifa'

    codigo_ingreso = fields.Char(
        string='Codigo del Ingreso',
        required=True,
        size=7
    )
