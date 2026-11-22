import json
import re
import subprocess
import sys

RCN_JSON = "rcn_data.json"


def parsear_keys(texto_keys: str) -> dict:
    """
    Convierte cadenas tipo:
    --key kid1:key1 --key kid2:key2
    o líneas 'kid1:key1' en un diccionario {"kid1": "key1", ...}
    """
    pares = re.findall(r"([0-9a-fA-F]{32}):([0-9a-fA-F]{32})", texto_keys)
    return {kid.lower(): key.lower() for kid, key in pares}


def actualizar_canal(identificador: str, nueva_url: str | None, texto_keys: str | None):
    with open(RCN_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    objetivo = None
    for canal in data:
        if (
            canal["tvg_id"].lower() == identificador.lower()
            or canal["nombre"].lower() == identificador.lower()
        ):
            objetivo = canal
            break

    if not objetivo:
        raise ValueError(f"No se encontró el canal '{identificador}' en {RCN_JSON}")

    if nueva_url:
        objetivo["url"] = nueva_url.strip()

    if texto_keys is not None:
        nuevas_keys = parsear_keys(texto_keys)
        if nuevas_keys:
            objetivo["keys"] = nuevas_keys

    with open(RCN_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Actualizado {objetivo['nombre']} en {RCN_JSON} ({len(objetivo['keys'])} llaves).")


if __name__ == "__main__":
    # Uso rápido desde terminal:
    # python actualizar_json_rcn.py DeportesRCN.co "https://..." "--key aaa:bbb --key ccc:ddd"
    if len(sys.argv) < 3:
        print('Uso: python actualizar_json_rcn.py <tvg_id|nombre> "<nueva_url_o_vacío>" "<texto_keys_o_vacío>"')
        raise SystemExit(1)

    canal_id = sys.argv[1]
    url_arg = sys.argv[2] if sys.argv[2].strip() else None
    keys_arg = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3].strip() else None

    actualizar_canal(canal_id, url_arg, keys_arg)
    subprocess.run([sys.executable, "actualizar_rcn.py"], check=True)
