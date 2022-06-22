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
        compute="_compute_tarifa")



    examenes_ids = fields.One2many(
        comodel_name='tarifa.examenes',
        inverse_name='tarifa_id',
        string='Listado de examenes'
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

    examenes_id = fields.Many2one(
        comodel_name='examenes',
        string='Examen',
        required=True
    )
    cod_examen = fields.Char(
        string='Codigo del examen',
        required=True,
        compute="_compute_cod_examen"
    )

    var_examen = fields.Float(
        string='Valor del examen',
        type='monetary',
        required=True,
    )

    tarifa_id = fields.Many2one(
        comodel_name='tarifa',
        string='Tarifa'
    )

    @api.depends('examenes_id')
    def _compute_cod_examen(self):
        for record in self:
            record.cod_examen = record.examenes_id.codigo_examen

    _sql_constraints = [('tarifa_examenes_unique',
                         'unique(examenes_id,tarifa_id)',
                         'No se puede tener registro duplicado bajo el mismo examen')]
