# -*- coding: utf-8 -*-
# from odoo import http


# class GalihBa(http.Controller):
#     @http.route('/galih__ba/galih__ba', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/galih__ba/galih__ba/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('galih__ba.listing', {
#             'root': '/galih__ba/galih__ba',
#             'objects': http.request.env['galih__ba.galih__ba'].search([]),
#         })

#     @http.route('/galih__ba/galih__ba/objects/<model("galih__ba.galih__ba"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('galih__ba.object', {
#             'object': obj
#         })

