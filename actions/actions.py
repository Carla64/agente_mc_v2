from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

############ Saludo inicial
class SolicitarNombre(Action):
    def name(self) -> Text:
        return "preguntar_nombre"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="¿Me podrías decir tu nombre?")
        return []

class ActionObtenerNombre(Action):
    def name(self) -> Text:
        return "obtener_nombre"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        nombre_usuario = None
        # Obtener todas las entidades en el último mensaje del usuario
        entidades = tracker.latest_message.get("entities")

        # Buscar la entidad 'nombre_usuario' en las entidades
        for entidad in entidades:
            if entidad["entity"] == "nombre_usuario":
                nombre_usuario = entidad["value"]
                break
        print(f"Nombre de usuario extraído: {nombre_usuario}")  # imprime el nombre de usuario

        # Resto del código...

        if nombre_usuario:
            dispatcher.utter_message(f"Hola {nombre_usuario}, soy tu agente virtual para atención de emergencia en caso de sismo.")
            dispatcher.utter_message("¿Estás solo o acompañado?")
            return [SlotSet("slot_nombre_usuario", nombre_usuario)]
        else:
            return []

class ActionEstadoAcompanamiento(Action):
    def name(self) -> Text:
        return "estado_acompanamiento_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = tracker.latest_message.get('text').lower()
        if "solo" in msg or "único" in msg or "nadie" in msg:
            estado = "solo"
        elif "acompañado" in msg or "juntos" in msg or "grupo" in msg or "personas" in msg:
            estado = "acompañado"
        else:
            estado = None

        if estado:
            ret = SlotSet("slot_tipo_persona", estado)
            dispatcher.utter_message(f"Entiendo, estás {estado}.")
            dispatcher.utter_message(f"Necesito confirmar tu estado. ¿Cómo lo describirías? ¿Grave o estable?")
            dispatcher.utter_message("Ten en cuenta que hay más personas que estamos atendiendo.")
            return [ret]
        else:
            dispatcher.utter_message("Lo siento, no entendí eso. ¿Podrías decirme si estás solo o acompañado?")
            return []

class ActionObtenerPrioridad(Action):
    def name(self) -> Text:
        return "obtener_prioridad_alta"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        msg = tracker.latest_message.get('text').lower()
        if "grave" in msg or "crítico" in msg:
            estado = "grave"
        elif "estable" in msg or "regular" in msg:
            estado = "estable"
        else:
            estado = None

        if estado:
            ret = SlotSet("slot_prioridad_alta", estado)
            dispatcher.utter_message(f"Entiendo, el estado del paciente es {estado}.")
            # Realiza las acciones necesarias en función del estado del paciente
            if estado == "grave":
                dispatcher.utter_message("Es importante que recibas atención médica de emergencia de inmediato.")
            elif estado == "estable":
                dispatcher.utter_message("Si notas que algo sucede, no olvides reportarlo")

            # Resto de la lógica de la acción
            dispatcher.utter_message("¿Me puedes proporcionar tu ubicacion?, menciona el edificio en el que te encuentras")
            return [ret]
        else:
            dispatcher.utter_message("Lo siento, no entendí eso. ¿Podrías describir el estado del paciente como grave o estable?")
            return []

############ Evaluación de la escena y riesgos del entorno

class IdentificarPeligrosEntorno(Action):
    def name(self) -> Text:
        return "identificar_peligros_entorno"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ubicacion = tracker.get_slot("slot_ubicacion")
        msg = tracker.latest_message.get('text').lower()
        if "edificio" in msg:
            ubicacion = "edificio"
        elif "biblioteca" in msg:
            ubicacion = "biblioteca"
        elif "cafeteria" in msg:
            ubicacion = "cafeteria"
        else:
            ubicacion = None

        if ubicacion:
            ret = SlotSet("slot_ubicacion", ubicacion)
            if "edificio" == ubicacion:
                # Identificar peligros en el edificio
                dispatcher.utter_message(text="En este edificio, se ha detectado una fuga de agua en el piso 2. Mantente alejado de esa área.")
            elif "biblioteca" in ubicacion:
                # Identificar peligros en la biblioteca
                dispatcher.utter_message(text="En la biblioteca, el primer piso se encuentra en remodelación. Se recomienda precaución al transitar por esa área.")
            elif "cafeteria" in ubicacion:
                # Identificar peligros en la cafetería
                dispatcher.utter_message(text="En la cafetería se ha reportado un problema eléctrico. Ten cuidado.")
            else:
                dispatcher.utter_message(text="No se encontró información de peligros en tu ubicación, pero mantente alerta.")
        else:
            dispatcher.utter_message(text="No se proporcionó la ubicación. Por favor, indica tu ubicación actual.")

        dispatcher.utter_message(text="Debido al evento, te realizare una evaluaicon rapida para determina tu estado, como es tu respiracion?.")
        return [ret]


############ Generar evaluaciones Primaria y Secundaria

class EvaluacionPrimaria(Action):
    def name(self) -> Text:
        return "evaluacion_primaria"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Ok, Iniciando evaluación Primaria.")
        dispatcher.utter_message(text="¿Como definirias tu respiracion?")
        return []

class Seguimiento(Action):
    def name(self) -> Text:
        return "seguimiento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Ok, para brindar seguimiento a mi atención...")
        return []

class SeleccionarPrioridadAlta(Action):
    def name(self) -> Text:
        return "seleccionar_prioridad_alta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Entiendo que tu estado es grave. Tu caso ha sido marcado como prioridad alta y la ayuda está en camino.")
        dispatcher.utter_message("Mientras llega la ayuda, es importante que intentes mantener la calma. Si puedes, trata de moverte a un lugar seguro y evita realizar esfuerzos físicos innecesarios.")
        dispatcher.utter_message("Recuerda que cada segundo cuenta. ")
        dispatcher.utter_message("Te comparto algunos consejos utiles a continuacion")
        dispatcher.utter_message("...")
        dispatcher.utter_message("...")
        dispatcher.utter_message("...")
        dispatcher.utter_message("Se le solicita al cuerpo de emergencia, reportar su llegada")
        dispatcher.utter_message("...")
        dispatcher.utter_message("...")
        dispatcher.utter_message("...")
        return []

############ Evaluación primaria (ABCDE)

class RecopilarEstadoRespiracion(Action):
    def name(self) -> Text:
        return "recopilar_estado_respiracion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        estado_respiracion = tracker.get_slot("slot_respiracion_estado")
        msg = tracker.latest_message.get('text').lower()
        if "bien" in msg or "bueno" in msg or "buena" in msg or "normal" in msg or "fuerte" in msg:
            estado_respiracion = "Bien"
        elif "mal" in msg or "mala" in msg:
            estado_respiracion = "Mal"
        elif "dificultad" in msg  or "rapida" in msg or "agitada" in msg:
            estado_respiracion = "Dificultad"
        elif "entrecortada" in msg:
            estado_respiracion = "Entrecortada"
        else:
            estado_respiracion = "Bien"

        ret = SlotSet("slot_respiracion_estado", estado_respiracion)
        dispatcher.utter_message(f"Entiendo, tu estado respiracion es {estado_respiracion}.")
        if estado_respiracion == "Bien":
            dispatcher.utter_message("Me alegra saber que estás bien a pesar del sismo.")
        elif estado_respiracion == "Mal":
            dispatcher.utter_message("Lamentablemente, el polvo puede afectar la respiración. Intenta buscar un lugar con aire más limpio e improvisa una mascarilla si es necesario.")
        elif estado_respiracion == "Dificultad":
            dispatcher.utter_message("Si tienes dificultad para respirar, intenta mantener la calma. Evita esfuerzos innecesarios.")
        elif estado_respiracion == "Entrecortada":
            dispatcher.utter_message("Si experimentas una respiración entrecortada, trata de mantener la calma. Evita esfuerzos innecesarios.")
        dispatcher.utter_message("Como esta tu circulacion? Normal, irregular, baja.")
        return [ret]

class RecopilarEstadoCirculacion(Action):
    def name(self) -> Text:
        return "recopilar_estado_circulacion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        circulacion_estado = tracker.get_slot('circulacion_estado')
        msg = tracker.latest_message.get('text').lower()
        if "baja" in msg or "irregular" in msg or "entumecidos" in msg:
            circulacion_estado = "Mala"
        elif "normal" in msg or "buena" in msg or "estable" in msg:
            circulacion_estado = "Normal"
        else:
            circulacion_estado = "Normal"

        ret = SlotSet("slot_circulacion_estado", circulacion_estado)
        dispatcher.utter_message(f"Entiendo, tu estado de circulación es {circulacion_estado}.")
        if circulacion_estado == "Mala":
                dispatcher.utter_message("Eso suena preocupante. Intenta mantener la calma.. Te auxiliare en el proceso")
        elif circulacion_estado == "Estable":
                dispatcher.utter_message("Bien, eso suena alentador. ")
        dispatcher.utter_message(text="¿En general, has presentado mareo o desorientacion?")
        return [ret]

class RecopilarEstadoNeurologico(Action):
    def name(self) -> Text:
        return "recopilar_estado_neurologico"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        neurologico_estado = tracker.get_slot('neurologico_estado')
        msg = tracker.latest_message.get('text').lower()
        if "normal" in msg or "buena" in msg or "estable" in msg or "bien" in msg or "tranquila" in msg:
            neurologico_estado = "Normal"
        elif "mareos" in msg or "mareada" in msg or "desorientado" in msg or "desorientada" in msg or "nauseas" in msg or "dolores" in msg:
            neurologico_estado = "Mala"

        ret = SlotSet("slot_neurologico_estado", neurologico_estado)
        dispatcher.utter_message(f"Entiendo, tu estado neurológico es {neurologico_estado}.")
        if neurologico_estado == "Mala":
            dispatcher.utter_message("Eso suena preocupante. Intenta mantener la calma, a continuacion te proporcionare algunas indicaciones de apoyo en lo que llega la ayuda.")
        elif neurologico_estado == "Normal":
            dispatcher.utter_message("Bien, eso suena alentador.")
        dispatcher.utter_message("Estamos evaluando")
        dispatcher.utter_message("Proporciona tu edad y si tienes algun antecedente o condicion medica que deba saber")
        return [ret]

class DeterminarEstadoGeneral(Action):
    def name(self) -> Text:
        return "determinar_estado_general"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        respiracion_estado = tracker.get_slot('slot_respiracion_estado')
        circulacion_estado = tracker.get_slot('slot_circulacion_estado')
        neurologico_estado = tracker.get_slot('slot_neurologico_estado')

        estados_graves = ["Mala", "mal", "pesada", "agotada", "dificultad", "baja", "irregular", "entumecidos", "mareos", "confusion", "desorientado"]
        estados_favorables = ["Normal","bien", "normal", "fuerte", "buena"]
        puntuacion = 0

        if respiracion_estado in estados_graves:
            puntuacion += 1
        if circulacion_estado in estados_graves:
            puntuacion += 1
        if neurologico_estado in estados_graves:
            puntuacion += 1

        if puntuacion >= 2:
            estado_general = "grave"
            dispatcher.utter_message(text="Tu estado es grave. Busca atención médica inmediatamente.")
        elif puntuacion == 1:
            estado_general = "estable"
            dispatcher.utter_message(text="Tu estado es estable. Continuaremos con el seguimiento de tu atención.")
        else:
            estado_general = "favorable"
            dispatcher.utter_message(text="Tu estado es favorable. Asegúrate de seguir monitorizando tus signos vitales.")

        return [SlotSet("slot_estado_general", estado_general)]

############ Tranquilizar

class TranquilizarApoyar(Action):
    def name(self) -> Text:
        return "tranquilizar_apoyar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre_usuario = tracker.get_slot("slot_nombre_usuario")
        personas_heridas = tracker.get_slot("slot_tipo_persona")
        prioridad_alta = tracker.get_slot("slot_prioridad_alta")

        ret = SlotSet("slot_nombre_usuario", nombre_usuario)
        if nombre_usuario:
            if personas_heridas:        
                if personas_heridas == "solo":
                    dispatcher.utter_message(text=f"{nombre_usuario}, no te preocupes. La ayuda está en camino.")
                    dispatcher.utter_message(text="Si es posible, asegúrate de mantener a salvo a la persona herida.")
                elif personas_heridas == "acompanado":
                    dispatcher.utter_message(text=f"{nombre_usuario}, no te preocupes. La ayuda está en camino.")
                    dispatcher.utter_message(text="Si es posible, asegúrate de mantener a salvo a las personas heridas.")
                else:
                    dispatcher.utter_message(text="No se detectó información sobre si estás solo o acompañado.")
            else:
                dispatcher.utter_message(text="No se detectó información sobre si estás solo o acompañado.")

            if prioridad_alta:
                dispatcher.utter_message(text="Tu situación se considera de prioridad alta. Estamos enviando ayuda adicional.")
                dispatcher.utter_message(text="Sigue las instrucciones que te brindaremos y mantén la calma.")
            else:
                dispatcher.utter_message(text="Recuerda mantener la calma y seguir las instrucciones que te brindaremos.")
            
            dispatcher.utter_message("Te comparto algunos consejos utiles a continuacion")
            dispatcher.utter_message("...")
            dispatcher.utter_message("...")
            dispatcher.utter_message("...")
            dispatcher.utter_message("Se le solicita al cuerpo de emergencia, reportar su llegada")
            dispatcher.utter_message("...")
            dispatcher.utter_message("...")
            dispatcher.utter_message("...")
        return [ret]

############ Instrucciones para shock

class IdentificarPosibilidadShock(Action):
    def name(self) -> Text:
        return "identificar_posibilidad_shock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        estado_circulacion = tracker.get_slot("slot_estado_circulacion")

        if estado_circulacion == "débil":
            dispatcher.utter_message(text="Si te encuentras en un estado de shock, te recomendaría que busques un lugar seguro y te sientes o te acuestes.")
            dispatcher.utter_message(text="Intenta mantener la calma y respirar profundamente.")
            dispatcher.utter_message(text="Si es posible, pide ayuda a alguien cercano")
        else:
            dispatcher.utter_message(text="No se detectaron signos de shock en tu estado de circulación.")        
        return []

class ProporcionarInstruccionesShock(Action):
    def name(self) -> Text:
        return "proporcionar_instrucciones_shock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Si te encuentras en un estado de shock, te recomendaría que busques un lugar seguro y te sientes o te acuestes.")
        dispatcher.utter_message(text="Intenta mantener la calma y respirar profundamente.")
        dispatcher.utter_message(text="Si es posible, pide ayuda a alguien cercano o llama a los servicios de emergencia.")
        dispatcher.utter_message(text="¿Hay algo más en lo que pueda ayudarte?")

        return []

############ Recopilación de información de la víctima

class DatosVictima(Action):
    def name(self) -> Text:
        return "datos_victima"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        edad = tracker.get_slot("slot_edad")
        antecedentes = tracker.get_slot("slot_antecedentes")

        if edad:
            dispatcher.utter_message(text=f"Tienes {edad} años.")
        else:
            dispatcher.utter_message(text="No se detectó información sobre tu edad.")

        if antecedentes:
            dispatcher.utter_message(text=f"Tienes los siguientes antecedentes médicos o condiciones: {antecedentes}")
        else:
            dispatcher.utter_message(text="No se detectaron antecedentes médicos o condiciones.")
        dispatcher.utter_message(text="Por favor, proporciona un contacto de emergencia (número de teléfono y nombre)")
        return []

############ Recursos adicionales y contacto de emergencia

class SolicitarRecursosAdicionales(Action):
    def name(self) -> Text:
        return "solicitar_recursos_adicionales"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="¿Necesitas recursos adicionales para la atención de la víctima?")
        return []

class RecopilarRecursosAdicionales(Action):
    def name(self) -> Text:
        return "recopilar_recursos_adicionales"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        recursos_adicionales = tracker.get_slot("slot_recursos_adicionales")

        if recursos_adicionales:
            dispatcher.utter_message(text="Entendido. Estamos gestionando los recursos que has solicitado.")
            dispatcher.utter_message(text="Por favor, proporciona un contacto de emergencia (número de teléfono y nombre)")
        else:
            dispatcher.utter_message(text="No se detectaron solicitudes de recursos adicionales.")
            dispatcher.utter_message(text="Por favor, proporciona un contacto de emergencia (número de teléfono y nombre)")
        return []

class InformarContactoEmergencia(Action):
    def name(self) -> Text:
        return "accion_informar_contacto_emergencia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        contacto_emergencia = tracker.get_slot("slot_contacto_emergencia")

        if contacto_emergencia:
            dispatcher.utter_message(text="Mandando un reporte preventivo a tu contacto.")
        else:
            dispatcher.utter_message(text="No se detectó información de contacto de emergencia.")
        return []

############ Despedida

class Despedida(Action):
    def name(self) -> Text:
        return "despedida_respuesta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = tracker.current_slot_values()

        reporte = "Reporte de la conversación:\n"
        for slot, value in slots.items():
            reporte += f"- {slot}: {value}\n"

        dispatcher.utter_message(text=reporte)
        dispatcher.utter_message(text="Gracias por utilizar nuestro servicio de atención de emergencia.")
        dispatcher.utter_message(text="Espero que te encuentres bien y que todo se solucione satisfactoriamente.")
        dispatcher.utter_message(text="Si necesitas ayuda en el futuro, no dudes en contactarnos.")
        dispatcher.utter_message(text="¡Cuídate!")
        return []
