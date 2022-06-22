from odoo import fields, models, api, _
from odoo.odoo.exceptions import UserError
import re


class EpsModel(models.Model):
    _name = 'eps'
    _description = 'Crud De eps'
    _rec_name = 'nombre_eps'

    codigo_eps = fields.Char(
        string='Codigo EPS',
        required=True,
        size=7
    )
    nombre_eps = fields.Char(
        string='Nombre EPS',
        required=True
    )
    tarifa_id = fields.Many2one(
        comodel_name='tarifa',
        string='Tarifa Asociada',
        required=True
    )

    @api.constrains('codigo_eps')
    def validate_cod_eps(self):
        if self.codigo_eps:
            match = re.match('^[0-9][0-9]{1}[0-9]$', self.codigo_eps)
            if match is None:
                raise UserError(_('El Codigo Eps No Es Validado'))

    _sql_constraints = [('eps_unique',
                         'unique(codigo_eps',
                         'El Codigo EPS Debe Ser Unico')]