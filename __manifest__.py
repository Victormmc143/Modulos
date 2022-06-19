{
    'name': 'Modulos Curso odoo',
    'version': '1',
    'description': 'Modulo Curso odoo',
    'category': 'Account',
    'author': 'VICTOR MERCADO',
    'license': 'AGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'view/consecutivos_view.xml',
        'view/paciente_view.xml'
    ],
    'installable': True,
    'auto_install': False
}