from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import re


class MunicipioModel(models.Model):
    _name = 'municipio'
    _description = 'Crud De Municipio'
    _rec_name = 'nombre_mun'

    departamento_id = fields.Many2one(
        comodel_name='departamento',
        string='Departamento',
        required=True
    )

    codigo_mun = fields.Char(
        string='Codigo Municipio',
        required=True,
        size=3
    )
    nombre_mun = fields.Char(
        string='Nombre Municipio',
        required=True)


    @api.constrains('codigo_mun')
    def validate_cod_mun(self):
        if self.codigo_mun:
            match = re.match('^[0-9][0-9]{1}[0-9]$', self.codigo_mun)
            if match is None:
                raise UserError(_('El Codigo Municipio No Es Validado'))

    _sql_constraints = [('municipio_unique',
                         'unique(codigo_mun,departamento_id)',
                         'El Codigo Municipio Por Departamento Debe Ser Unico')]


