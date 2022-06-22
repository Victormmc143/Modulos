from odoo import fields, models, api, _
from odoo.odoo.exceptions import UserError
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

    @api.constrains('codigo_examen')
    def validate_cod_examen(self):
        if self.codigo_examen:
            match = re.match('^[0-9][0-9]{1}[0-9]$', self.codigo_examen)
            if match is None:
                raise UserError(_('El Codigo de la examen No Es Validado'))

    _sql_constraints = [('examen_unique',
                         'unique(codigo_examen',
                         'El Codigo Examen Debe Ser Unico')]