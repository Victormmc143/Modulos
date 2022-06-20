from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ConsecutivoModel(models.Model):
    _name = 'consecutivo'
    _description = 'Curso odoo'
    # Secuencia de Odoo siempre debe venir de un ir sequence (secuencia de Odoo)
    name = fields.Char(
        string='Nombre',
        required=True)
    dirPto = fields.Char(
        string='Direccion De Consecutivo De Emision',
        required=True
    )
    fechaInicioPto = fields.Date(
        string='Fecha De Inicio De Consecutivo Emision',
        required=True)
    fechaFinalPto = fields.Date(
        string='Fecha De Final De Consecutivo Emision',
        required=True)
    sequence = fields.Char(
        string='Sequence',
        readonly=True)
    sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string='Sequence_id',
        required=True)
    detail_id = fields.One2many(
        comodel_name='consecutivo.detalle',
        inverse_name='consecutivo_id',
        string='Detalle Consecutivo'
    )
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True,
        default='draft')
         

    # FUNCION PARA ASIGNAR LA SECUENCIA EN MI REGISTRO DE CONSECUTIVO
    def asignar_secuencia(self):
        for record in self:
            if not record.sequence_id:
                raise UserError(_("Error no tiene secuencia asignada"))
            record.sequence = record.env['ir.sequence'].next_by_code(record.sequence_id.code)
            record.state = 'posted'


class Detalleconsecutivo(models.Model):
    _name = 'consecutivo.detalle'
    _description = 'Detalle del Consecutivo'


    tipDoc = fields.Selection(
        string='Tipo Consecutivo',
        selection=[
            ('1', 'Factura C'),
            ('2', 'Factura A')
        ],
        required=True,
        default='1'
    )
    numSecuencia = fields.Integer(
        string='Numero De Secuencia',
        required=True,
        default='1'
    )
    estado = fields.Selection(
        string='Estado',
        selection=[
            ('1', 'Activo'),
            ('2', 'Inactivo')
        ],
        required=True,
        default='1'
    )
    consecutivo_id = fields.Many2one(
        comodel_name='consecutivo',
        string='Consecutivo'
    )
