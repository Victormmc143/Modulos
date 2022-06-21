{
    'name': 'Modulos Curso odoo',
    'version': '1',
    'description': 'Modulo Curso odoo1',
    'category': 'Account',
    'author': 'VICTOR MERCADO',
    'license': 'AGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'view/consecutivos_view.xml',
        'view/paciente_view.xml',
        'view/departamento_view.xml',
        'view/municipio_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
