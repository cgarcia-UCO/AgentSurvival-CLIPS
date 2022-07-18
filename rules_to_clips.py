import clips

def clips_que_veo(paredes):
    #Pasamos el entorno del agente a CLIPS
    if paredes['left']:
        izq = 1
    else:
        izq = 0
    if paredes['right']:
        der = 1
    else:
        der = 0
    if paredes['front']:
        fr = 1
    else:
        fr = 0
    if paredes['back']:
        det = 1
    else:
        det = 0

    return izq,der,fr,det

def clips_to_code(self,reglas,paredes,objetos):
    izq,der,fr,det = clips_que_veo(paredes)

    #Creación del entorno CLIPS
    env = clips.Environment()

    #Creación de template muros en el entorno CLIPS
    template_string = """
    (deftemplate muros
      (slot izq (type INTEGER))
      (slot der (type INTEGER))
      (slot fr (type INTEGER))
      (slot det (type INTEGER)))
    """
    env.build(template_string)

    #Introducción del hecho muros con los valores obtenidos anteriormente
    muros = env.find_template('muros')
    fact = muros.assert_fact(izq=izq,
                                der=der,
                                fr=fr,
                                det=det)

    #Introducción de las reglas escritas por el usuario al entorno CLIPS
    for regla in reglas:
        env.build(regla)

    #Ejecución del entorno CLIPS
    env.run()

    #Revisa los hechos después de la ejecución del entorno para que el agente realice los movimientos
    for fact in env.facts():
        if str(fact) == "(turn_right)":
            self.turn_right()
        if str(fact) == "(turn_left)":
            self.turn_left()
        if str(fact) == "(move_forward)":
            self.move_forward()