

from odoo import fields, models, api


class PacienteModel(models.Model):
    _name = 'paciente'
    _description = 'Modelo para paciente'

    name = fields.Char(
        string='Name',
        required=True)
    fechaNacimiento = fields.Date(
        string='Fecha Nacimiento',
        required=True)
    edad = fields.Integer(
        string='Edad'
    )
    sex = fields.Selection(
        string='Sexo',
        selection=[('M', 'Masculino'),
                   ('F', 'Femenino') ],
        required=True
    )
    detail_idstel = fields.One2many(
        comodel_name='paciente.telefono',
        inverse_name='paciente_id',
        string='Telefono del paciente'
    )
    detail_idsdir = fields.One2many(
        comodel_name='paciente.direccion',
        inverse_name='paciente_id',
        string='Direccion del paciente'
    )



class TelefonoPaciente(models.Model):
    _name = 'paciente.telefono'
    _description = 'Telefono del paciente'

    detalleTel = fields.Char(
        string='Telefono',
        required=True)
    tipTel = fields.Selection(
        string='Tipo Telefono',
        selection=[('Principal', 'Principal'),
                   ('Otros', 'Otros')],
        required=True
    )
    # Todos los campos que son de tipo relacional
    # debe terminar o debe tener como sufijo id o ids dependiendo del caso
    paciente_id = fields.Many2one(
        comodel_name='paciente',
        string='Paciente'
    )
class DireccionPaciente(models.Model):
    _name = 'paciente.direccion'
    _description = 'Direccion del paciente'

    detalleDir = fields.Char(
        string='Direccion',
        required=True)
    tipDir = fields.Selection(
        string='Tipo Direccion',
        selection=[('Principal', 'Principal'),
                   ('Otros', 'Otros')],
        required=True
    )
    # Todos los campos que son de tipo relacional
    # debe terminar o debe tener como sufijo id o ids dependiendo del caso
    paciente_id = fields.Many2one(
        comodel_name='paciente',
        string='Paciente'
    )

