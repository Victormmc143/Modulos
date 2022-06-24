from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import re


class PacienteModel(models.Model):
    _name = 'paciente'
    _description = 'Modelo para paciente'
    _rec_name = 'doc_completo'

    tipo_documentos = fields.Selection(
        string='Tipo De Documentos',
        selection=[('CC', 'CEDULA'),
                   ('TI', 'TARJETA DE IDENTIDAD')],
        required=True,
    )
    documento = fields.Char(
        string='Documento',
        required=True)

    nom1 = fields.Char(
        string='Primer Nombre',
        required=True)
    nom2 = fields.Char(
        string='Segundo Nombre',
        required=True)
    ape1 = fields.Char(
        string='Primer Apellido',
        required=True)
    ape2 = fields.Char(
        string='Segundo Apeliido',
        required=True)
    fecha_nacimiento = fields.Date(
        string='Fecha Nacimiento',
        required=True)
    edad = fields.Integer(
        string='Edad',
        required=True,
        compute="_compute_edad"
    )
    sex = fields.Selection(
        string='Sexo',
        selection=[('M', 'Masculino'),
                   ('F', 'Femenino')],
        required=True
    )
    correo = fields.Char(
        string='Correo',
        required=True
    )
    doc_completo = fields.Char(
        compute="_compute_nombre_completo"
    )
    nom_completo = fields.Char(
        compute="_compute_nombre_completo"
    )
    telefono_ids = fields.One2many(
        comodel_name='paciente.telefono',
        inverse_name='paciente_id',
        string='Listado De Telefono Paciente'
    )
    direccion_ids = fields.One2many(
        comodel_name='paciente.direccion',
        inverse_name='paciente_id',
        string='Listado De Direccion Paciente'
    )
    departamento_id = fields.Many2one(
        comodel_name='departamento',
        string='Departamento',
        required=True
    )
    municipio_id = fields.Many2one(
        comodel_name='municipio',
        string='Municipio',
        required=True,
        domain="[('departamento_id', '=' ,departamento_id)]"
    )


    # @api.constrains('tipodocumentos','documento')
    # def _validate_documento(self):
    #    for record in self:
    #        paciente_ids = record.env['paciente'].search_count([
    #            ('tipodocumentos','=',record.tipodocumentos),
    #            ('documento', '=', record.documento),
    #            ('id','!=',record.id)
    #        ])
    #        if paciente_ids:
    #            raise UserError(_("No se puede tener registro duplicado bajo el mismo tipo de documento y documento"))
    _sql_constraints = [('paciente_unique',
                         'unique(tipo_documentos,documento)',
                         'No se puede tener registro duplicado bajo el mismo tipo de documento y documento')]

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for record in self:
            fecha_actual = fields.Date.today()
            fecha_nacimiento = record.fecha_nacimiento
            edad = relativedelta(fecha_actual, fecha_nacimiento).years
            record.edad = edad

    @api.constrains('documento')
    def _compute_nombre_completo(self):
        for record in self:
            nombre = record.nom1+' '+record.nom2+' '+record.ape1+' '+record.ape2
            record.nom_completo = nombre
            record.doc_completo = record.tipo_documentos+'-'+record.documento


    @api.constrains('correo')
    def validate_mail(self):
        if self.correo:
            match = re.match('^[_a-z]+[0-9-]*(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.correo)
            if match == None:
                raise UserError(_('Correo no valido'))

    @api.constrains('tipo_documentos')
    def _validate_tel_dir(self):
        for record in self:
            tel = record.env['paciente.telefono'].search_count([
                ('paciente_id', '=', record.id),
                ('tel_principal', '=', '1')
            ])
            dir = record.env['paciente.direccion'].search_count([
                ('paciente_id', '=', record.id),
                ('dir_principal', '=', '1')
            ])
            mjs=""
            if tel == 0:
                mjs="Por Favor Digite Un Telefono Principal"+"\n"
            if dir == 0:
                mjs = mjs+"Por Favor Digite Una Direccion Principal\n"
            if mjs != "":
                raise UserError(_(mjs))


class TelefonoPaciente(models.Model):
    _name = 'paciente.telefono'
    _description = 'Listado De Telefono Paciente'
    _rec_name = 'num_telefono'

    num_telefono = fields.Char(
        string='Numero de Telefono',
        required=True,
    )
    tel_principal = fields.Selection(
        string='Telefono Principal',
        selection=[
            ('1', 'SI'),
            ('2', 'NO')
        ],
        required=True
    )

    @api.constrains('num_telefono')
    def validate_tel(self):
        if self.num_telefono:
            match = re.match('^[1-9][0-9]{4,10}[0-9]$', self.num_telefono)
            if match is None:
                raise UserError(_('El Telefono Digitado No Es Validado'))

    paciente_id = fields.Many2one(
        comodel_name='paciente',
        string='Paciente'
    )

    @api.constrains('num_telefono')
    def _validate_telefono_principal(self):
        for record in self:
            if record.tel_principal == '1':
                tel = record.env['paciente.telefono'].search_count([
                    ('id', '!=', record.id),
                    ('paciente_id', '=', record.paciente_id.id),
                    ('tel_principal', '=', '1')
                ])
                if tel:
                    raise UserError(_("El Paciente Solo Debe Tener Un Numero De Telefono Principal"))

class DireccionPaciente(models.Model):
    _name = 'paciente.direccion'
    _description = 'Listado De Direccion Paciente'

    bar = fields.Char(
        string='Barrio',
        required=True,
    )
    dir = fields.Char(
        string='Direccion',
        required=True,
    )

    dir_principal = fields.Selection(
        string='Direccion Principal',
        selection=[
            ('1', 'SI'),
            ('2', 'NO')
        ],
        required=True
    )
    paciente_id = fields.Many2one(
        comodel_name='paciente',
        string='Paciente'
    )
    @api.constrains('dir')
    def _validate_direccion_principal(self):
        for record in self:
            if record.dir_principal == '1':
                tel = record.env['paciente.direccion'].search_count([
                    ('id', '!=', record.id),
                    ('paciente_id', '=', record.paciente_id.id),
                    ('dir_principal', '=', '1')
                ])
                if tel:
                    raise UserError(_("El Paciente Solo Debe Tener Una Direccion Principal"))