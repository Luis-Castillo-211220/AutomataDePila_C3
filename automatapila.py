import tkinter as tk
from tkinter import scrolledtext
import re

class PDA:
    def __init__(self, grammar, terminals):
        self.grammar = grammar
        self.terminals = terminals
        self.stack = []
        self.stack_history = [] 
        
    # automata de pila
    def parse(self, input_string):
        self.stack.append("PX")  # Símbolo de inicio
        print("Pila:", self.stack)
        self.stack_history.append("Pila: " + str(self.stack))
        index = 0
        while self.stack and index <= len(input_string):
            # print("Pila:", self.stack)
            index = self.skip_whitespace(
                input_string, index
            )  # Saltar espacios en blanco
            if index >= len(input_string):
                break

            top = self.peek()
            remaining_input = input_string[index:]

            if top in self.grammar:
                self.process_non_terminal(top, remaining_input)
            elif self.match_terminal(top, remaining_input):
                match_length = len(
                    re.match(self.terminals[top], remaining_input).group()
                )
                index += match_length
                self.pop()
            else:
                raise Exception(f"Error de sintaxis cerca de la posición {index}")
            print("Pila:", self.stack)
            self.stack_history.append("Pila: " + str(self.stack))
        return len(self.stack) == 0

    def process_non_terminal(self, non_terminal, input_string):
        self.pop()

        if non_terminal == "RE":
            self.choose_production_for_RE(input_string)
        elif (
            non_terminal == "PX"
        ):  # accesos para distintas opciones en las producciones
            self.choose_production_for_PX(input_string)
        elif non_terminal == "VL":
            self.choose_production_for_VL(input_string)
        elif non_terminal == "P":
            self.choose_production_for_P(input_string)
        elif non_terminal == "RP":
            self.choose_production_for_RP(input_string)
        elif non_terminal == "RC":
            self.choose_production_for_RC(input_string)
        elif non_terminal == "RCA":
            self.choose_production_for_RCA(input_string)
        elif non_terminal == "R":
            self.choose_production_for_R(input_string)
        elif non_terminal == "ORTA":
            self.choose_production_for_ORTA(input_string)
        elif non_terminal == "RFB":
            self.push_production(
                self.grammar["RFB"][0]
            )  # Si se encuentra una regla con doble produccion
        elif non_terminal == "PRA":
            self.push_production(self.grammar["PRA"][0])
        elif non_terminal == "PRB":
            self.push_production(self.grammar["PRB"][0])
        elif non_terminal == "RFE":
            self.push_production(self.grammar["RFE"][0])
        elif non_terminal == "RPA":
            self.push_production(self.grammar["RPA"][0])
        elif non_terminal == "RI":
            self.push_production(self.grammar["RI"][0])
        #  self.push_production(self.grammar["RI"][1])
        elif non_terminal == "CDC":
            self.push_production(self.grammar["CDC"][0])
        elif non_terminal == "RIA":
            self.push_production(self.grammar["RIA"][0])
        #  self.push_production(self.grammar["RIA"][1])
        elif non_terminal == "RIB":
            self.push_production(self.grammar["RIB"][0])
        #  self.push_production(self.grammar["RIB"][1])
        elif non_terminal == "RIC":
            self.push_production(self.grammar["RIC"][0])
        #  self.push_production(self.grammar["RIC"][1])
        elif non_terminal == "RID":
            self.push_production(self.grammar["RID"][0])
            # self.push_production(self.grammar["RID"][1])
        elif non_terminal == "RW":
            self.push_production(self.grammar["RW"][0])
        elif non_terminal == "S":
            self.push_production(self.grammar["S"][0])
        elif non_terminal == "SC":
            self.push_production(self.grammar["SC"][0])
        elif non_terminal == "SD":
            self.push_production(self.grammar["SD"][0])
        elif non_terminal == "SE":
            self.push_production(self.grammar["SE"][0])
        else:
            # Para otros no terminales NT
            self.choose_production(non_terminal, input_string)

    # FUNCIONES PARA AYUDAR A ELEGIR OPCIONES DE LAS REGLAS

    def choose_production_for_ORTA(self, input_string):
        if re.match(self.terminals["CM"], input_string):
            self.push_production(self.grammar["ORTA"][0])
        elif re.match(self.terminals["ID"], input_string):
            self.push_production(self.grammar["ORTA"][1])
        elif re.match(self.terminals["NUMBER"], input_string):
            self.push_production(self.grammar["ORTA"][2])
        # else:
        #     raise Exception(
        #         f"No se pudo encontrar una producción adecuada para 'ORTA' con entrada {input_string}")

    def choose_production_for_R(self, input_string):
        if re.match(self.terminals["RT"], input_string):
            self.push_production(self.grammar["R"][0])
        else:
            self.push_production(self.grammar["R"][1])

    def choose_production_for_RCA(self, input_string):
        if re.match(self.terminals["CE"], input_string):
            self.push_production(self.grammar["RCA"][0])
        else:
            self.push_production(self.grammar["RCA"][1])

    def choose_production_for_RE(self, input_string):
        if re.match(self.terminals["E"], input_string):
            self.push_production(self.grammar["RE"][0])
        elif re.match(self.terminals["Q"], input_string):
            self.push_production(self.grammar["RE"][1])


    def is_epsilon_production_for_RE(self, input_string):
        return not input_string.startswith(self.terminals["E"])

    def choose_production_for_RC(self, input_string):
        if re.match(self.terminals["ID"], input_string):
            self.push_production(self.grammar["RC"][0])
        else:
            self.push_production(self.grammar["RC"][1])

    def choose_production_for_P(self, input_string):
        if re.match(self.terminals["TP"], input_string):
            self.push_production(self.grammar["P"][0])
        else:
            self.push_production(self.grammar["P"][1])

    def choose_production_for_RP(self, input_string):
        if re.match(self.terminals["CO"], input_string):
            self.push_production(self.grammar["RP"][0])
        else:
            self.push_production(self.grammar["RP"][1])

    def choose_production_for_VL(self, input_string):
        if re.match(self.terminals["PA"], input_string):
            self.push_production(self.grammar["VL"][0])
        elif re.match(self.terminals["Q"], input_string):
            self.push_production(self.grammar["VL"][1])

    def choose_production_for_PX(self, input_string):
        if input_string.startswith("Fn"):
            # Si la entrada comienza con 'Fn', elige la producción 'F RF'
            self.push_production(self.grammar["PX"][1])  # "F RF"
        elif input_string.startswith("if"):
            # Si la entrada comienza con 'if', elige la producción 'I RI'
            self.push_production(self.grammar["PX"][2])  # "I RI"
        elif input_string.startswith("while"):
            # Si la entrada comienza con 'while', elige la producción 'W RW'
            self.push_production(self.grammar["PX"][3])  # "W RW"
        elif input_string.startswith("switch"):
            # Si la entrada comienza con 'switch', elige la producción 'SW S'
            self.push_production(self.grammar["PX"][4])  # "SW S"
        else:
            self.push_production(self.grammar["PX"][0])

    def choose_production(self, non_terminal, input_string):
        for production in self.grammar[non_terminal]:
            if self.is_valid_production(production, input_string):
                self.push_production(production)
                return
        raise Exception(
            f"No se pudo encontrar una producción adecuada para {non_terminal} con entrada {input_string}"
        )

    def is_valid_production(self, production, input_string):
        symbols = production.split()
        if not symbols:
            return False
        first_symbol = symbols[0]
        if first_symbol in self.terminals:
            return re.match(self.terminals[first_symbol], input_string) is not None
        else:
            return False

    def push_production(self, production):
        for symbol in reversed(production.split()):
            self.push(symbol)

    def skip_whitespace(self, input_string, index):
        while index < len(input_string) and input_string[index].isspace():
            index += 1
        return index

    def match_terminal(self, terminal, input_string):
        pattern = self.terminals[terminal]
        return re.match(pattern, input_string)

    def push(self, symbol):
        if symbol != "ε":  # ε representa la cadena vacía
            self.stack.append(symbol)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1] if self.stack else None


terminals = {
    "ID": r"[a-z_][a-z0-9_]*",
    "NUMBER": r"[0-9]+",
    "TP": r"(int|string)",
    "AS": r"=>",
    "PA": r"\(",
    "PC": r"\)",
    "CM": r'"',
    # 'CC': r'"',
    "CO": r",",
    "F": r"Fn",
    "C": r"contenido",
    "LA": r"\{",
    "LC": r"\}",
    "I": r"if",
    "OR": r"(<|>|==|>=|<=|!=)",
    "E": r"else",
    "W": r"while",
    "SW": r"switch",
    "CE": r"case",
    "DT": r"default",
    "BR": r"break",
    "RT": r"rtn",
    "Q": r"$"
}

# Gramática de ejemplo
grammar = {
    "PX": ["V", "F RF", "I RI", "W RW", "SW S"],  # PX
    "V": ["ID VA"],  # V
    "VA": ["AS VB"],
    "VB": ["TP VL"],
    "RF": ["AS RFA"],  # RF
    "RFA": ["ID RFB"],
    "RFB": ["PR RFC"],
    "RFC": ["LA RFD"],
    "RFD": ["C RFE"],
    "RFE": ["R LC"],
    "RI": ["CD RIA"],  # RI
    "RIA": ["AS RIB"],
    "RIB": ["LA RIC"],
    "RIC": ["C RID"],
    "RID": ["LC RE"],
    "RW": ["CD RWA"],  # RW
    "RWA": ["AS RWB"],
    "RWB": ["LA RWC"],
    "RWC": ["C LC"],
    "S": ["OP SA"],  # S
    "SA": ["AS SB"],
    "SB": ["LA SC"],
    "SC": ["CA SD"],
    "SD": ["RCA SE"],
    "SE": ["DF LC"],
    # "VL": ["PA VLA", "PA VLD", "ε"],  # VL
    # "VLA": ["CM VLB"],
    # "VLB": ["ID VLC"],
    # "VLC": ["CM PC"],
    # "VLD": ["NUMBER PC"],
    "VL": ["PA VLA", "Q"],  # VL
    "VLA": ["CM VLB", "NUMBER VLD"],
    "VLB": ["ID VLC"],
    "VLC": ["CM PC"],
    "VLD": ["PC"],
    "P": ["TP ID", "ε"],  # P
    "PR": ["PA PRA"],  # PR
    "PRA": ["P PRB"],
    "PRB": ["RP PC"],
    "RP": ["CO RPA", "ε"],  # RP
    "RPA": ["P RP"],
    "CD": ["PA CDA"],  # CD
    "CDA": ["ID CDB"],
    "CDB": ["OR CDC"],
    "CDC": ["RC PC"],
    "RC": ["ID", "NUMBER"],  # RC
    "RE": ["E REA", "Q"],  # RE
    "REA": ["AS REB"],
    "REB": ["LA REC"],
    "REC": ["C LC"],
    "OP": ["PA OPA"],  # OP
    "OPA": ["ID PC"],
    "CA": ["CE CAA"],  # CA
    "CAA": ["NUMBER CAB"],
    "CAB": ["AS CAC"],
    "CAC": ["LA CAD"],
    "CAD": ["C CAE"],
    "CAE": ["BR LC"],
    "RCA": ["CA RCA", "ε"],  # RCA
    "DF": ["DT DFA"],  # DF
    "DFA": ["AS DFB"],
    "DFB": ["LA DFC"],
    "DFC": ["C LC"],
    "R": ["RT ORT", "ε"],  # R
    # "ORT": ["PA ORTA", "PA ORTD", "PA ORTE"],  # ORT
    # "ORTA": ["CM ORTB"],
    # "ORTB": ["ID ORTC"],
    # "ORTC": ["CM PC"],
    # "ORTD": ["ID PC"],
    # "ORTE": ["NUMBER PC"],
    "ORT": ["PA ORTA"],  # ORT
    "ORTA": ["CM ORTB", "ID ORTD", "NUMBER ORTD"],
    "ORTB": ["ID ORTC"],
    "ORTC": ["CM PC"],
    "ORTD": ["PC"],
}

def analyze():
    input_string = text_area.get("1.0", tk.END)
    pda = PDA(grammar, terminals)
    is_valid = pda.parse(input_string)

    # Mostrar el historial de la pila
    stack_history_text = "\n".join(pda.stack_history)
    stack_history_area.config(state=tk.NORMAL)  # Habilitar edición para actualizar
    stack_history_area.delete("1.0", tk.END)  # Borrar contenido anterior
    stack_history_area.insert(tk.END, stack_history_text)  # Insertar historial de la pila
    stack_history_area.config(state=tk.DISABLED)  # Deshabilitar edición

    if is_valid:
        result_label.config(text="La cadena está correctamente escrita.")
    else:
        result_label.config(text="La cadena no está correctamente escrita.")

# Creación de la ventana principal
root = tk.Tk()
root.title("Analizador de Cadenas")

# Área de texto para la entrada
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5)
text_area.pack(pady=10)

# Botón para analizar
analyze_button = tk.Button(root, text="Analizar Cadena", command=analyze)
analyze_button.pack(pady=5)

# Área de texto para mostrar el historial de la pila
stack_history_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, state=tk.DISABLED)
stack_history_area.pack(pady=10)

# Etiqueta para mostrar resultados
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()