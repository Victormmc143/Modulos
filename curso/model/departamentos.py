from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import re


class DepartamentoModel(models.Model):
    _name = 'departamento'
    _description = 'Crud De Departamento'
    _rec_name = 'nombre_dep'


    codigo_dep = fields.Char(
        string='Codigo Departamento',
        required=True,
        size=2
    )
    nombre_dep = fields.Char(
        string='Nombre Departamento',
        required=True)

    mun_dep_id = fields.One2many(
        comodel_name='municipio',
        inverse_name='departamento_id',
        string='Listado De Municipio Paciente'
    )


    @api.constrains('codigo_dep')
    def validate_cod_dep(self):
        if self.codigo_dep:
            match = re.match('^[0-9][0-9]$', self.codigo_dep)
            if match is None:
                raise UserError(_('El Codigo Departamento No Es Validado'))

    _sql_constraints = [('departamento_unique',
                         'unique(codigo_dep)',
                         'El Codigo Departamento Debe Ser Unico')]




