import requests
from typing import Union, List
import os

class SenderWpp:
    def __init__(self, api_key: str):
        self.account_namespace = "c2d81fe9_79c1_4a6e_a247_f71ef06c22d8"
        self.headers = {
            "Authorization": "Key {}".format(api_key),
            "content-type": "application/json",
        }

    def set_template(self, template: str):
        self.template = template

    def format_number(self, phone: str) -> str:
        if "," in phone:
            phone = phone.split(",")[0]

        if "+55" not in phone:
            phone = "+55{}".format(phone)

        return (
            phone.replace(" ", "")
            .replace(".", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

    def mount_text_parameters(self, parameters: List[str]) -> dict:
        text_msg_parameters = []

        for parameter in parameters:

            formatted_parameter = {
                "type": "text",
                "text": parameter,
            }

            text_msg_parameters.append(formatted_parameter)

        return text_msg_parameters

    def get_take_number_id(self, phone: str) -> Union[str, bool]:
        url = "https://http.msging.net/commands"

        payload = {
            "id": "a456-42665544000-0123e4567-e89b-12d3",
            "to": "postmaster@wa.gw.msging.net",
            "method": "get",
            "uri": "lime://wa.gw.msging.net/accounts/{}".format(phone),
        }

        resp = requests.post(url, headers=self.headers, json=payload)

        if resp.ok:
            resp = resp.json()

            if resp.get("resource"):
                return resp.get("resource").get("alternativeAccount")

        return False

    def text_msg_request(
        self,
        phone: str,
        take_number_id: str,
        template: str,
        message_parameters: List[dict],
    ) -> bool:
        url = "https://http.msging.net/messages"

        payload = {
            "id": 12345678,
            "to": take_number_id,
            "type": "application/json",
            "content": {
                "type": "template",
                "template": {
                    "namespace": self.account_namespace,
                    "name": template,
                    "language": {"code": "pt_BR", "policy": "deterministic"},
                    "components": [
                        {"type": "body", "parameters": message_parameters}
                    ],
                },
            },
        }

        resp = requests.request("POST", url, headers=self.headers, json=payload)

        if resp.ok:

            return True

        return False

    def send_text_msg(self, phone: str, message_parameters: List[str]) -> tuple[bool, str]: 
        phone = self.format_number(phone)

        take_number_id = self.get_take_number_id(phone)
        print(take_number_id)

        take_number_id = '5524992915706@wa.gw.msging.net'
        
        if not take_number_id:
            return False

        message_parameters = self.mount_text_parameters(message_parameters)

        return (
            self.text_msg_request(
                phone, take_number_id, self.template, message_parameters
            ),
            phone,
        )
        


def envia_wpp_evento(telefone, nome, codigo):
    
    codigo=str(codigo)
    
    telefone=str(telefone)
    nome=str(nome)
    
    nome=nome.split(' ')[0].capitalize()

    envio=0
    
    token = os.getenv("TOKEN_BLIP")
    
    sw = SenderWpp(token)
    sw.set_template("inscricao_evento_confirmacao_v1")
    
    enviado, telefone = sw.send_text_msg(telefone, [nome,codigo])
       
    print(enviado)
    print(telefone)
    
    if enviado==True:
        envio=1
        
    return envio     
        
def envia_wpp_texto(lista_mensagem_ajustada: List[str], telefone: str, template: str):
    token = os.getenv("TOKEN_BLIP")
    sw = SenderWpp(token)
    
    sw.set_template(template)
    return sw.send_text_msg(telefone,lista_mensagem_ajustada)
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

