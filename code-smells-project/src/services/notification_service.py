import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("NotificationService")

def notify_order_created(pedido_id, usuario_id):
    # T-06: Extract business logic/side effects from controllers
    logger.info(f"ENVIANDO EMAIL: Pedido {pedido_id} criado para usuario {usuario_id}")
    logger.info(f"ENVIANDO SMS: Seu pedido foi recebido!")
    logger.info(f"ENVIANDO PUSH: Novo pedido recebido pelo sistema")

def notify_order_status_update(pedido_id, status):
    if status == "aprovado":
        logger.info(f"NOTIFICAÇÃO: Pedido {pedido_id} foi aprovado! Preparar envio.")
    elif status == "cancelado":
        logger.info(f"NOTIFICAÇÃO: Pedido {pedido_id} cancelado. Devolver estoque.")
