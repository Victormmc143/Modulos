from odoo import fields, models, api, _
from odoo.exceptions import UserError
import re
from . import tarifa


class EpsModel(models.Model):
    _name = 'eps'
    _description = 'Crud De eps'
    _rec_name = 'nombre_eps'


    codigo_eps = fields.Char(
        string='Codigo EPS',
        required=True,
        size=6
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

    examenes_ids1 = fields.One2many(
        comodel_name='tarifa.examenes',
        compute="_compute_ome"
    )

    @api.onchange('tarifa_id')
    def _compute_ome(self):
        for record in self:
            record.examenes_ids1 = record.env['tarifa.examenes'].search([('tarifa_id','=',record.tarifa_id.id)])






    @api.constrains('codigo_eps')
    def validate_cod_eps(self):
        if self.codigo_eps:
            match = re.match('^[A-Z][A-Z]{2}[0-9]{2}[0-9]$', self.codigo_eps)
            if match is None:
                raise UserError(_('El Codigo Eps No Es Validado'))

    _sql_constraints = [('eps_unique',
                         'unique(codigo_eps',
                         'El Codigo EPS Debe Ser Unico')]

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

