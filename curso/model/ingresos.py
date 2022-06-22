from odoo import fields, models, api


class IngresosModel(models.Model):
    _name = 'ingresos'
    _description = 'Ingresos de pacientes'
    _rec_name = 'codigo_ingreso'

    codigo_ingreso = fields.Char(
        string='Codigo del Ingreso',
        readonly=True,
        size=7
    )
    fecha_ingreso = fields.DateTime(
        string='Fecha de ingreso',
        readonly=True,
        default=fields.Date.today()
    )
    id_paciente = fields.Many2one(
        comodel_name='paciente',
        string='Paciente',
        required=True
    )
    id_eps = fields.Many2one(
        comodel_name='eps',
        string='EPS',
        required=True
    )

    def create(self,vals):
        ingreso_id = super(IngresosModel, self).create(vals)
        ingreso_id.codigo_ingreso = self.env['ir.sequence'].next_by_code('curso.ingreso.sequence')
        return ingreso_id
