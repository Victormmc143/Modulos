from odoo import fields, models, api, _
from odoo.exceptions import UserError
import re


class TarifaModel(models.Model):
    _name = 'tarifa'
    _description = 'Crud De tarifa'
    _rec_name = 'nombre_tarifa'

    codigo_tarifa = fields.Char(
        string='Codigo Tarifa',
        required=True,
        size=3
    )
    nombre_tarifa = fields.Char(
        string='Nombre Tarifa',
        required=True)
    @api.constrains('codigo_tarifa')
    def _validate_cant_exa(self):
        mjs = ""
        if self.codigo_tarifa:
            match = re.match('^[0-9][0-9]{1}[0-9]$', self.codigo_tarifa)
            if match is None:
                mjs = 'El Codigo de la tarifa No Es Validado'+"\n"
        for record in self:
            tel = record.env['tarifa.examenes'].search_count([
                ('tarifa_id', '=', record.id)
            ])
            if tel == 0:
                mjs = mjs + "Por Favor Escoja Un Examen En la Tarifa"
                raise UserError(_(mjs))

    examenes_ids = fields.One2many(
        comodel_name='tarifa.examenes',
        inverse_name='tarifa_id',
        string='Listado de examenes'
    )

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

    @api.constrains('var_examen')
    def _validate_var_examen(self):

        for record in self:
            if record.var_examen <= 0.0:
                raise UserError(_("El Valor Del Examen Debe Ser Mayor A 0"))

    @api.depends('examenes_id')
    def _compute_cod_examen(self):
        for record in self:
            record.cod_examen = record.examenes_id.codigo_examen



    _sql_constraints = [('tarifa_examenes_unique',
                         'unique(examenes_id,tarifa_id)',
                         'No se puede tener registro duplicado bajo el mismo examen')]
