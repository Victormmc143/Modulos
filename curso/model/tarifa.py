from odoo import fields, models, api, _
from odoo.odoo.exceptions import UserError
import re


class TarifaModel(models.Model):
    _name = 'tarifa'
    _description = 'Crud De tarifa'
    _rec_name = 'nombre_tarifa'

    codigo_tarifa = fields.Char(
        string='Codigo Tarifa',
        required=True,
        size=7
    )
    nombre_tarifa = fields.Char(
        string='Nombre Tarifa',
        required=True)

    valor_tarifa = fields.Float(
        string='Valor Tarifa',
        type='monetary',
        options='',
        required=True)

    examenes_ids = fields.One2many(
        comodel_name='tarifa.examenes',
        inverse_name='paciente_id',
        string='Listado De Telefono Paciente'
    )

    @api.constrains('codigo_tarifa')
    def validate_cod_tarifa(self):
        if self.codigo_tarifa:
            match = re.match('^[0-9][0-9]{1}[0-9]$', self.codigo_tarifa)
            if match is None:
                raise UserError(_('El Codigo de la tarifa No Es Validado'))

    _sql_constraints = [('tarifa_unique',
                         'unique(codigo_tarifa',
                         'El Codigo Tarifa Debe Ser Unico')]


class ExamenesTarifa(models.Model):
    _name = 'tarifa.examenes'
    _description = 'Listado De examenes'

    num_telefono = fields.Char(
        string='Numero de Telefono',
        required=True,
    )
    tel_principal = fields.Selection(
        string='Telefono Principal',
        selection=[
            ('1', 'SI'),
            ('2', 'NO')
        ],
        required=True
    )
