from app_orders.models import OrderItem


def is_payment_valid(card_number: str) -> bool:
    return len(card_number) <= 8 and int(card_number) % 2 == 0


def check_amount(items: list[OrderItem]) -> list[str]:
    errors = []
    for item in items:
        if item.product.count < item.quantity:
            errors.append(f"not enough {item.product.title}")

    return errors


def reduce_product_quantity(items: list[OrderItem]) -> None:
    for item in items:
        item.product.count -= item.quantity
        item.product.save()
