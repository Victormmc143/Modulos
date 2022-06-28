from odoo import fields, models, api, _
from odoo.exceptions import UserError


class IngresosModel(models.Model):
    _name = 'ingresos'
    _description = 'Ingresos de pacientes'
    _rec_name = 'codigo_ingreso'

    codigo_ingreso = fields.Char(
        string='Codigo del Ingreso',
        readonly=True,

    )
    fecha_ingreso = fields.Datetime(
        string='Fecha de ingreso',
        readonly=True,
        default=fields.Datetime.now()
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

    producto_ids = fields.One2many(
        comodel_name='ingreso.detalle',
        inverse_name='ingreso_id',
        string='Listado De Examenes'
    )

    nom_paciente = fields.Char(
        comodel_name='paciente',
        compute="_compute_nompac"
    )
    tarifa = fields.Many2one(
        comodel_name='tarifa',
        compute="_compute_tarifa",
        readonly=True,
    )
    tarifa_id = fields.Integer(
        readonly=True,
    )

    totalpagar = fields.Float(
        string='Total A Pagar',
        readonly=True,
        type='monetary',
        compute="_compute_total"
    )

    d_cargar = fields.Selection(
        string='Desea cargar documento ?',
        selection=[('1', 'Si'),
                   ('0', 'No')],
        required=True,
        default='0',
    )

    doc_file = fields.Binary(
        string='Cargar Documento',
        help='Cargar un documento en caso que lo requiera para el ingreso',
        attachment=True,
        store=True

    )

    @api.onchange('producto_ids', 'id_eps')
    def _compute_total(self):
        for record in self:
            record.totalpagar = 0
            if record.producto_ids:
                for produtc1 in record.producto_ids:
                    record.totalpagar = record.totalpagar+(produtc1.valor*produtc1.cantidad)

    @api.onchange('id_paciente')
    def _compute_nompac(self):
        for record in self:
            record.nom_paciente = record.env['paciente'].search([('id', '=', record.id_paciente.id)])['nom_completo']

    @api.onchange('id_eps')
    def _compute_tarifa(self):
        for record in self:
            if record.tarifa_id:
                record.tarifa = record.env['tarifa'].search([('id', '=', record.tarifa_id)])
            else:
                record.tarifa = record.env['tarifa'].search([('id', '=', record.id_eps.tarifa_id.id)])
                record.tarifa_id = record.env['tarifa'].search([('id', '=', record.id_eps.tarifa_id.id)])['id']

    @api.model
    def create(self, vals):
        ingreso_id = super(IngresosModel, self).create(vals)
        ingreso_id.codigo_ingreso = self.env['ir.sequence'].next_by_code('curso.ingreso.sequence')
        return ingreso_id

    @api.onchange('id_eps', 'producto_ids')
    def onchange_method(self):
        for record in self:
            if record.id_eps:
                tarifa_ids = record.id_eps.tarifa_id.examenes_ids
                for produtc in record.producto_ids:
                    productos_tarifas = tarifa_ids.filtered(lambda x: x.examenes_id.id == produtc.examenes_id.id)
                    if productos_tarifas:
                        produtc.valor = productos_tarifas.var_examen
                    else:
                        produtc.valor = 0

    @api.constrains('id_paciente')
    def _validate_detalle_ingreso(self):
        for record in self:
            tel = record.env['ingreso.detalle'].search_count([
                ('ingreso_id', '=', record.id)
            ])
            if tel == 0:
                raise UserError(_("No Se Puede Guardar El Ingreso Sin Escoger Un Examen"))


class IngresoDetallemodel(models.Model):
    _name = 'ingreso.detalle'
    _description = 'Listado De Examenes'

    examenes_id = fields.Many2one(
        comodel_name='examenes',
        string='Examen',
        required=True
    )
    cantidad = fields.Integer(
        string='cantidad Del Examen',
        required=True,
    )
    valor = fields.Float(
        string='Valor Del Examen',
        required=True,
        type='monetary'
    )
    total = fields.Float(
        string='Total Del Examen',
        readonly=True,
        type='monetary',
        compute="_compute_valor"
    )

    ingreso_id = fields.Many2one(
        comodel_name='ingresos',
        string='Ingresos'
    )

    @api.constrains('valor')
    def _validate_valor_examen(self):
        for record in self:
            if record.valor <= 0.0:
                raise UserError(_("El Valor Del Examen Debe Ser Mayor A 0"))

    @api.constrains('cantidad')
    def _validate_cantidad_examen(self):
        for record in self:
            if record.cantidad <= 0.0:
                raise UserError(_("La cantidad Debe Ser Mayor A 0"))

    @api.depends('valor', 'cantidad')
    def _compute_valor(self):
        for record in self:
            record.total = record.valor * record.cantidad

    _sql_constraints = [('ingreso_detalle_unique',
                         'unique(examenes_id,ingreso_id)',
                         'El Examen no se puede escoger dos veces')]
