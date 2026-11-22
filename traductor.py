"""Simulador de traducción de direcciones virtuales de 32 bits."""

import re

TAM_PAGINA = 4096
DIRECCION_MAXIMA = 0xFFFFFFFF
TABLA_PAGINAS = {0: 2, 1: 5, 2: 9, 0x12F: 0x9DE9}


def leer_entero(texto):
    """Lee un entero decimal o hexadecimal con el prefijo 0x."""
    texto = texto.strip()
    if not re.fullmatch(r"(?:[0-9]+|0[xX][0-9a-fA-F]+)", texto):
        raise ValueError("Usa números decimales o hexadecimales con 0x.")
    base = 16 if texto.lower().startswith("0x") else 10
    return int(texto, base)


def separar_direccion(texto):
    """Obtiene la página virtual y el desplazamiento desde ambos formatos."""
    if len(texto) > 100:
        raise ValueError("La entrada supera los 100 caracteres.")
    if texto.startswith("(") and texto.endswith(")"):
        partes = texto[1:-1].split(",")
        if len(partes) != 2:
            raise ValueError("El par debe tener la forma (página, desplazamiento).")
        pagina, desplazamiento = map(leer_entero, partes)
        if pagina > DIRECCION_MAXIMA // TAM_PAGINA:
            raise ValueError("La página virtual excede el espacio de 32 bits.")
        if desplazamiento >= TAM_PAGINA:
            raise ValueError("El desplazamiento debe estar entre 0 y 4095.")
        return pagina, desplazamiento

    direccion = leer_entero(texto)
    if direccion > DIRECCION_MAXIMA:
        raise ValueError("La dirección virtual excede el espacio de 32 bits.")
    return divmod(direccion, TAM_PAGINA)


def main():
    print("Conversión de direcciones virtuales a físicas")
    print("Escribe (página, desplazamiento) o una dirección completa.")
    print("Usa decimal o hexadecimal con 0x. Teclea salir para terminar.")
    print("Página → marco: 0 → 2, 1 → 5, 2 → 9 y 0x12F → 0x9DE9.")
    while True:
        try:
            entrada = input("\nEntrada > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if entrada.lower() == "salir":
            break

        try:
            pagina, desplazamiento = separar_direccion(entrada)
        except ValueError as error:
            print(f"Error: {error}")
            continue

        marco = TABLA_PAGINAS.get(pagina)
        if marco is None:
            print(f"Error: la página {pagina} (0x{pagina:X}) no tiene marco asignado.")
            continue
        base = marco * TAM_PAGINA
        fisica = base + desplazamiento
        print(f"Página: {pagina} (0x{pagina:X})")
        print(f"Desplazamiento: {desplazamiento} (0x{desplazamiento:X})")
        print(f"Marco: {marco} (0x{marco:X})")
        print(f"Base física: 0x{base:08X}")
        print(f"Dirección física: {fisica} (0x{fisica:08X})")


if __name__ == "__main__":
    main()
