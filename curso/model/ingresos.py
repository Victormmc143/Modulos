from odoo import fields, models, api


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



    @api.model
    def create(self, vals):
        ingreso_id = super(IngresosModel, self).create(vals)
        ingreso_id.codigo_ingreso = self.env['ir.sequence'].next_by_code('curso.ingreso.sequence')
        return ingreso_id

    @api.onchange('id_eps','producto_ids')
    def onchange_method(self):
        for record in self:
            if record.id_eps:
                tarifa_ids = record.id_eps.tarifa_id.examenes_ids
                for produtc in record.producto_ids:
                    productos_tarifas = tarifa_ids.filtered(lambda x:x.examenes_id.id==produtc.examenes_id.id)
                    if productos_tarifas:
                        produtc.valor = productos_tarifas.var_examen
                    else:
                        produtc.valor = 0


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
        required=True,
        type='monetary'
    )


    ingreso_id = fields.Many2one(
        comodel_name='ingresos',
        string='Ingresos'
    )

