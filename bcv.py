import requests
import urllib3
from bs4 import BeautifulSoup

# Desactivar advertencias de SSL ya que la página del BCV suele presentar problemas de certificados intermedios
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BCV:
    URL = "https://www.bcv.org.ve/"

    def get_amount_bcv(self) -> str:
        """
        Realiza web scraping a https://www.bcv.org.ve/, obtiene el valor dentro de id="dolar"
        y retorna el monto con los primeros 2 dígitos decimales (ejemplo: '887,30').
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(self.URL, headers=headers, verify=False, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        dolar_div = soup.find("div", id="dolar")
        if not dolar_div:
            raise ValueError("No se encontró el elemento con id='dolar' en la página del BCV.")

        strong_tag = dolar_div.find("strong")
        if not strong_tag:
            raise ValueError("No se encontró la etiqueta <strong> con el valor del dólar.")

        raw_value = strong_tag.get_text(strip=True)

        # Tomar solo los primeros 2 dígitos decimales (ejemplo: 887,30200000 -> 887,30)
        if "," in raw_value:
            integer_part, decimal_part = raw_value.split(",", 1)
            return f"{integer_part},{decimal_part[:2]}"
        elif "." in raw_value:
            integer_part, decimal_part = raw_value.split(".", 1)
            return f"{integer_part},{decimal_part[:2]}"

        return raw_value


# Objeto 'bcv' listo para ser importado y utilizado
bcv = BCV()
