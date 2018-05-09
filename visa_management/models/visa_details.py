from odoo import api, fields, models
from odoo.modules.module import get_module_resource
from odoo import tools


class employees(models.Model):
    _name = 'employees.details'
    _description = 'employees details'
    _inherit = 'hr.employee'

    @api.model
    def _default_image(self):
        image_path = get_module_resource( 'hr', 'static/src/img', 'default_image.png' )
        return tools.image_resize_image_big( open( image_path, 'rb' ).read().encode( 'base64' ) )

    name_related = fields.Char( related='resource_id.name', string="Resource Name", readonly=True, store=True )
    country_id = fields.Many2one( 'res.country', string='Nationality (Country)' )
    birthday = fields.Date( 'Date of Birth', groups='hr.group_hr_user' )
    ssnid = fields.Char( 'SSN No', help='Social Security Number', groups='hr.group_hr_user' )
    sinid = fields.Char( 'SIN No', help='Social Insurance Number', groups='hr.group_hr_user' )
    identification_id = fields.Char( string='Identification No', groups='hr.group_hr_user' )
    gender = fields.Selection( [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups='hr.group_hr_user' )
    marital = fields.Selection( [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups='hr.group_hr_user' )
    department_id = fields.Many2one( 'hr.department', string='Department' )
    address_id = fields.Many2one( 'res.partner', string='Working Address' )
    address_home_id = fields.Many2one( 'res.partner', string='Home Address' )
    bank_account_id = fields.Many2one( 'res.partner.bank', string='Bank Account Number',
                                       domain="[('partner_id', '=', address_home_id)]",
                                       help='Employee bank salary account', groups='hr.group_hr_user' )
    work_phone = fields.Char( 'Work Phone' )
    mobile_phone = fields.Char( 'Work Mobile' )
    work_email = fields.Char( 'Work Email' )
    work_location = fields.Char( 'Work Location' )
    notes = fields.Text( 'Notes' )
    parent_id = fields.Many2one( 'hr.employee', string='Manager' )
    category_ids = fields.Many2many( 'hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id',
                                     string='Tags' )
    child_ids = fields.One2many( 'hr.employee', 'parent_id', string='Subordinates' )
    resource_id = fields.Many2one( 'resource.resource', string='Resource',
                                   ondelete='cascade', required=True, auto_join=True )
    coach_id = fields.Many2one( 'hr.employee', string='Coach' )
    job_id = fields.Many2one( 'hr.job', string='Job Title' )
    passport_id = fields.Char( 'Passport No', groups='hr.group_hr_user' )
    color = fields.Integer( 'Color Index', default=0 )
    city = fields.Char( related='address_id.city' )
    login = fields.Char( related='user_id.login', readonly=True )
    last_login = fields.Datetime( related='user_id.login_date', string='Latest Connection', readonly=True )

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary( "Photo", default=_default_image, attachment=True,
                           help="This field holds the image used as photo for the employee, limited to 1024x1024px." )
    image_medium = fields.Binary( "Medium-sized photo", attachment=True,
                                  help="Medium-sized photo of the employee. It is automatically "
                                       "resized as a 128x128px image, with aspect ratio preserved. "
                                       "Use this field in form views or some kanban views." )
    image_small = fields.Binary( "Small-sized photo", attachment=True,
                                 help="Small-sized photo of the employee. It is automatically "
                                      "resized as a 64x64px image, with aspect ratio preserved. "
                                      "Use this field anywhere a small image is required." )
