from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import connections, OperationalError


def execute_query(query: str, many=True):
    try:
        cursor = connections['default'].cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]
        return rows if many else rows[0] if len(rows) > 0 else None
    except OperationalError:
        raise Exception('Erro ao executar consulta')


def send_channel_message(group: str, content: dict):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group, {
        'type': 'group.message',
        'content': content
    })
