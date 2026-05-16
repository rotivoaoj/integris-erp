from datetime import datetime


def moeda(valor):
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def data_hora_brasileira(valor):
    if valor is None:
        return ""

    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M:%S")

    if isinstance(valor, str):
        for fmt in (
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
        ):
            try:
                dt = datetime.strptime(valor, fmt)
                if "%H" in fmt:
                    return dt.strftime("%d/%m/%Y %H:%M:%S")
                return dt.strftime("%d/%m/%Y")
            except ValueError:
                continue

    return valor


def data_brasileira(valor):
    formatted = data_hora_brasileira(valor)
    return formatted.split(" ")[0] if formatted else formatted
