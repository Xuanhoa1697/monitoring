import logging
import odoo
import subprocess
import odoo.modules.registry
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from datetime import datetime, timedelta
_logger = logging.getLogger(__name__)
repository_path = 'D:\Web\TWGeology\TWMonitoring\monitoring'


class EnApp(http.Controller):
    @http.route('/web/api/v1/mobile_monitoring_authenticate', type='json', auth="none")
    def monitoring_authenticate(self, db, login, password, base_location=None):
        message = 'Success'
        code = 200
        session_id = ''
        uid = False
        display_name = ''
        company = ''
        user_id = False
        job_name = ''
        is_admin = False
        try:
            if not http.db_filter([db]):
                message = 'Access Denied'
            uid = request.session.authenticate(request.db, request.params['login'], request.params['password'])
            if uid and uid != request.session.uid:
                message = 'Access Denied'
                code = 500
            if uid:
                request.session.db = db
                registry = odoo.modules.registry.Registry(db)
                with registry.cursor() as cr:
                    env = odoo.api.Environment(cr, request.session.uid, request.session.context)
                    session_info = env['ir.http'].session_info()
                    display_name = env.user.sudo().name
                    company = env.company.sudo().display_name
                    user_id = env.user.sudo().id
                    job_name = env.user.partner_id.function
                    if session_info:
                        session_id = request.session.sid
                        is_admin = True
        except odoo.exceptions.AccessDenied as e:
            message = 'Access Denied'
            code = 500

        return {
            'code': code,
            'msg': message,
            'user': {
                'session_id': session_id,
                'display_name': display_name,
                'company': company,
                'images': '/web/image?model=res.users&id=%s&field=image_128' % user_id,
                'user_id': user_id,
                'job_name': job_name,
                'is_admin': is_admin
            }
        }

    @http.route('/web/api/v1/mobile_get_construction_with_user',  type='json', auth="public")
    def mobile_get_construct_with_user(self, user_id):
        result = {
            'code': 200,
            'massage': 'Success'
        }
        data = []
        try:
            if user_id:
                construction_ids = request.env['monitoring.sites'].sudo().read_group(
                    domain=[('user_ids', 'in', user_id)],
                    fields=['construction_id'], groupby=['construction_id']
                )
                print(construction_ids)
                for construction in construction_ids:
                    ct_id = construction.get('construction_id')
                    construction_id = request.env['construction.monitoring'].sudo().browse(ct_id[0])
                    url = f'http://118.70.118.186:8069/web/content?model=construction.monitoring&id={construction_id.id}&field=image&filename_field=name'
                    data.append({
                        'id': construction_id.id,
                        'name': construction_id.name,
                        'address': construction_id.construction_address,
                        'image': url,
                    })
                result.update({
                    'data': data
                })
        except ValueError as e:
            result['code'] = 500
            result['massage'] = 'Access Denied'
        return result

    @http.route('/web/api/v1/mobile_get_sites',  type='json', auth="public")
    def mobile_get_sites(self, construct_id, user_id=False):
        result = {
            'code': 200,
            'massage': 'Success'
        }
        try:
            if construct_id:
                site_ids = request.env['monitoring.sites'].sudo().\
                    search_read([('construction_id', '=', construct_id),\
                                 ('user_ids', 'in', user_id)], ['id', 'name'])
                result.update({
                    'data': site_ids
                })
        except ValueError as e:
            result['code'] = 500
            result['massage'] = 'Access Denied'
        return result

    @http.route('/web/api/v1/mobile_get_devices',  type='json', auth="public")
    def mobile_get_devices(self, site_id, type_id):
        result = {
            'code': 200,
            'massage': 'Success'
        }
        current_date = datetime.now()
        formatted_date = (current_date + timedelta(hours=7)).strftime('%Y-%m-%d')
        data = []
        try:
            if site_id:
                devices_ids = request.env['monitoring.devices'].sudo().search([('site_id', '=', site_id), ('type_id', '=', type_id)])
                if devices_ids:
                    for item in devices_ids:
                        is_submit = request.env['monitoring.data'].sudo().search(
                            [('date', '=', formatted_date), ('device_id', '=', item.id)])
                        data.append({
                            'id': item.id,
                            'name': item.name,
                            'description': item.description,
                            'is_submit': bool(is_submit),
                            'type_device': item.type_id.code,
                            'site_id': site_id
                        })

        except ValueError as e:
            result['code'] = 500
            result['massage'] = 'Access Denied'
        result.update({
            'data': data
        })
        return result

    @http.route('/web/api/v1/mobile_get_devices_type',  type='json', auth="public")
    def mobile_get_devices_type(self, site_id):
        result = {
            'code': 200,
            'massage': 'Success'
        }
        current_date = datetime.now()
        formatted_date = (current_date + timedelta(hours=7)).strftime('%Y-%m-%d')
        data = []
        try:
            if site_id:
                devices_ids = request.env['monitoring.devices'].sudo().read_group(
                    domain=[('site_id', '=', site_id)],
                    fields=['id', 'name', 'type_id'], groupby=['type_id']
                )
                for item in devices_ids:
                    type_id = item.get('type_id')
                    type_data = request.env['monitoring.type'].sudo().browse(type_id[0])
                    data_done = request.env['monitoring.data'].sudo().search([('code', '=', type_data.code), ('date', '=', formatted_date), ('site_id', '=', site_id)])
                    data.append({
                        'id': type_id,
                        'count': item['type_id_count'],
                        'name': type_data.name,
                        'done': len(data_done),
                        'wait': item['type_id_count'] - len(data_done)
                    })

        except ValueError as e:
            result['code'] = 500
            result['massage'] = 'Access Denied'
        result.update({
            'data': data
        })
        return result

    @http.route('/web/api/v1/sync_main', type='json', auth="public")
    def git_pull(self):
        try:
            subprocess.check_call(['git', 'pull'], cwd=repository_path)
            return 'Success'
        except subprocess.CalledProcessError as e:
            return 'Error'

    @http.route('/web/api/v1/mobile_request_data',  type='json', auth="public")
    def mobile_request_data(self, device_id):
        result = {
            'code': 200,
            'massage': 'Success'
        }
        current_date = datetime.now()
        formatted_date = (current_date + timedelta(hours=7)).strftime('%Y-%m-%d')
        data = {}
        last_data = {}
        try:
            if device_id:
                data_ids = request.env['monitoring.data'].sudo().search(
                    [('date', '=', formatted_date), ('device_id', '=', device_id)])
                device_ids = request.env['monitoring.devices'].sudo().browse(device_id)
                nearest_record = request.env['monitoring.data'].sudo().\
                    search([('device_id', '=', device_id), ('id', 'not in', data_ids.ids)], order='date desc', limit=1)
                print(nearest_record)
                if device_ids.type_id.code == 'PZ':
                    data = {
                        'r': data_ids.data_ids[-1].piezo_r if data_ids.data_ids else 0,
                        't': data_ids.data_ids[-1].piezo_t if data_ids.data_ids else 0,
                        'casa': data_ids.data_ids[-1].casa if data_ids.data_ids else 0,
                    }
                    last_data = {
                        'r': nearest_record.data_ids[-1].piezo_r if nearest_record.data_ids else 0,
                        't': nearest_record.data_ids[-1].piezo_t if nearest_record.data_ids else 0,
                        'casa': nearest_record.data_ids[-1].casa if nearest_record.data_ids else 0,
                    }
                elif device_ids.type_id.code in ['EX', 'CM']:
                    data = {
                        'r': data_ids.data_ids[-1].ex_cm_r if data_ids.data_ids else 0,
                        't': data_ids.data_ids[-1].ex_cm_t if data_ids.data_ids else 0,
                    }
                    last_data = {
                        'r': nearest_record.data_ids[-1].ex_cm_r if nearest_record.data_ids else 0,
                        't': nearest_record.data_ids[-1].ex_cm_t if nearest_record.data_ids else 0,
                    }
                elif device_ids.type_id.code in ['CG']:
                    data = {
                        'r': data_ids.data_ids[-1].cg_r if data_ids.data_ids else 0,
                    }
                    last_data = {
                        'r': nearest_record.data_ids[-1].cg_r if nearest_record.data_ids else 0,
                    }
                elif device_ids.type_id.code in ['MPX']:
                    data = {
                        'n1': data_ids.data_ids[-1].n1 if data_ids.data_ids else 0,
                        'n2': data_ids.data_ids[-1].n2 if data_ids.data_ids else 0,
                        'n3': data_ids.data_ids[-1].n3 if data_ids.data_ids else 0,
                        'n4': data_ids.data_ids[-1].n4 if data_ids.data_ids else 0,
                    }
                    last_data = {
                        'n1': nearest_record.data_ids[-1].n1 if nearest_record.data_ids else 0,
                        'n2': nearest_record.data_ids[-1].n2 if nearest_record.data_ids else 0,
                        'n3': nearest_record.data_ids[-1].n3 if nearest_record.data_ids else 0,
                        'n4': nearest_record.data_ids[-1].n4 if nearest_record.data_ids else 0,
                    }
                elif device_ids.type_id.code in ['TP']:
                    data = {
                        'A_0': data_ids.data_ids[-1].TP_A_0 if data_ids.data_ids else 0,
                        'A_180': data_ids.data_ids[-1].TP_A_180 if data_ids.data_ids else 0,
                    }
                    last_data = {
                        'A_0': nearest_record.data_ids[-1].TP_A_0 if nearest_record.data_ids else 0,
                        'A_180': nearest_record.data_ids[-1].TP_A_180 if nearest_record.data_ids else 0,
                    }
                elif device_ids.type_id.code in ['SP']:
                    data = {
                        'casa': data_ids.data_ids[-1].casa if data_ids.data_ids else 0,
                    }
                    last_data = {
                        'casa': nearest_record.data_ids[-1].casa if nearest_record.data_ids else 0,
                    }
                data.update({
                    'description': data_ids.data_ids[-1].note if data_ids.data_ids else ''
                })
        except ValueError as e:
            result['code'] = 500
            result['massage'] = 'Access Denied'
        result.update({
            'data': data,
            'last_data': last_data
        })
        return result

    @http.route('/web/api/v1/mobile_sync_data',  type='json', auth="public")
    def mobile_sync_data(self, latitude, longitude, device_id, user_id, dataset):
        result = {
            'code': 200,
            'massage': 'Success'
        }
        current_date = datetime.now()
        formatted_date = (current_date + timedelta(hours=7)).strftime('%Y-%m-%d')
        data_env = request.env['monitoring.data'].sudo()
        device_env = request.env['monitoring.devices'].sudo()
        detail_env = request.env['monitoring.data.detail'].sudo()
        try:
            data_id = data_env.search([('device_id', '=', device_id), ('date', '=', formatted_date)])
            device = device_env.browse(device_id)
            if not data_id:
                data_id = data_env.create({
                    'name': device.name,
                    'site_id': device.site_id.id,
                    'device_id': device_id,
                    'construction_id': device.site_id.construction_id.id,
                    'user_id': user_id,
                    'date':  formatted_date,
                })
            data = {
                'data_id': data_id.id,
                'user_id': user_id
            }
            if device.type_id.code == 'PZ':
                data.update({
                    'piezo_r': dataset['r'],
                    'piezo_t': dataset['t'],
                    'casa': dataset['casa'],
                })
            elif device.type_id.code in ['EX', 'CM']:
                data.update({
                    'ex_cm_r': dataset['r'],
                    'ex_cm_t': dataset['t']
                })
            elif device.type_id.code in ['CG']:
                data.update({
                    'cg_r': dataset['r']
                })
            elif device.type_id.code in ['MPX']:
                data.update({
                    'n1': dataset['n1'],
                    'n2': dataset['n2'],
                    'n3': dataset['n3'],
                    'n4': dataset['n4'],
                })
            elif device.type_id.code in ['TP']:
                data.update({
                    'TP_A_0': dataset['A_0'],
                    'TP_A_180': dataset['A_180'],
                })
            elif device.type_id.code in ['SP']:
                data.update({
                    'casa': dataset['casa']
                })
            data.update({
                'note':  dataset['description'],
                'latitude': str(latitude),
                'longitude': str(longitude),
                'last_update': current_date,
            })
            datas_ids = detail_env.create(data)
            if data_id.device_id:
                compute = request.env['monitoring.compute'].sudo().search([('device_ids', 'in', data_id.device_id.id)])
                if compute and compute.code:
                    try:
                        for line in datas_ids:
                            line.update({
                                'result': float(eval(compute.code.format(line=line)))
                            })
                    except ValueError as e:
                        pass
                        print(e)
            if device.site_id.path:
                data_id.convert_to_csv(datas_ids)
        except ValueError as e:
            print(e)
            result['code'] = 500
            result['massage'] = 'Access Denied'
        return result


