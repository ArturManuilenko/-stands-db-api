from api_utils.access import PermissionRegistry

permissions = PermissionRegistry('ul_iot_account_notification_service', 15000, 16000)

# comment because of necessary send email on public api pii password reset
PERMISSION__NFK_MK_MESSAGE_EMAIL = permissions.add('NFK_MK_MESSAGE_EMAIL', 1, 'send message to user', 'email_send')
PERMISSION__NFK_GET_LOGS_LIST = permissions.add('NFK_GET_LOGS_LIST', 2, 'get logs list', 'email_send_log')
PERMISSION__NFK_GET_LOG = permissions.add('NFK_GET_LOG', 3, 'get log by id', 'email_send_log')
PERMISSION__NFK_GET_TEMPLATES_LIST = permissions.add('NFK_GET_TEMPLATES_LIST', 4, 'get templates list', 'template')
PERMISSION__NFK_GET_TEMPLATE = permissions.add('NFK_GET_TEMPLATE', 5, 'get template by id', 'template')
PERMISSION__NFK_MOD_TEMPLATE = permissions.add('NFK_MOD_TEMPLATE', 6, 'update template', 'template')
PERMISSION__NFK_DEL_TEMPLATE = permissions.add('NFK_DEL_TEMPLATE', 7, 'delete template', 'template')
PERMISSION__NFK_MK_TEMPLATE = permissions.add('NFK_MK_TEMPLATE', 8, 'create template', 'template')
