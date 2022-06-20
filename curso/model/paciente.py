from odoo import fields, models, api


class PacienteModel(models.Model):
    _name = 'paciente'
    _description = 'Modelo para paciente'

    TipoDocumentos = fields.Selection(
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
    fechaNacimiento = fields.Date(
        string='Fecha Nacimiento',
        required=True)
    edad = fields.Integer(
        string='Edad',
        required=True
    )
    sex = fields.Selection(
        string='Sexo',
        selection=[('M', 'Masculino'),
                   ('F', 'Femenino')],
        required=True
    )
    detail_ids = fields.One2many(
        comodel_name='paciente.datos',
        inverse_name='paciente_id',
        string='Datos Adicional del paciente'
    )
    _sql_constraints = [('paciente_unique', 'unique(TipoDocumentos,documento)')]


class DatoAdicionalPaciente(models.Model):
    _name = 'paciente.datos'
    _description = 'Datos Adicional del paciente'

    datos = fields.Char(
        string='Datos',
        required=True)
    tipDato = fields.Selection(
        string='Tipo De Datos',
        selection=[('1', 'Telefono'),
                   ('2', 'Direccion')],
        required=True
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
    # Todos los campos que son de tipo relacional
    # debe terminar o debe tener como sufijo id o ids dependiendo del caso
    paciente_id = fields.Many2one(
        comodel_name='paciente',
        string='Paciente'
    )
