# !-*-coding:utf-8-*-

import handlers


routes = []
routes.extend(handlers.add_comment.route)
routes.extend(handlers.get_new_pic.route)
routes.extend(handlers.index.route)
routes.extend(handlers.like.route)
routes.extend(handlers.load_more.route)
routes.extend(handlers.login.route)
routes.extend(handlers.logout.route)
routes.extend(handlers.new_pic_notify.route)
routes.extend(handlers.register.route)
routes.extend(handlers.upload_avatar.route)
routes.extend(handlers.upload_file.route)
routes.append((r"/(.*)", handlers.error.ErrorHandler))
