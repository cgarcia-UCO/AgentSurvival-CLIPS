import clips


# Comprobar las percepciones del agente
def what_I_see(self):
    things = self.whats_here()
    walls = things['walls']
    objects = things['objects']
    return walls, objects


# Ejecutar la función de salida si el objeto detectado es de tipo salida
def exit_if_possible(self, objects):
    for i in objects:
        if i['type'] == 'exit':
            i['exit_function'](self)


# Transformar los datos para crear el hecho "muros"
def what_I_see_CLIPS(walls):
    # Pasamos el entorno del agente a CLIPS
    if walls['left']:
        izq = 1
    else:
        izq = 0
    if walls['right']:
        der = 1
    else:
        der = 0
    if walls['front']:
        fr = 1
    else:
        fr = 0
    if walls['back']:
        det = 1
    else:
        det = 0

    return izq, der, fr, det


def rules_to_CLIPS(self, rules, walls):
    izq, der, fr, det = what_I_see_CLIPS(walls)

    # Creación del entorno CLIPS
    env = clips.Environment()

    # Creación de template muros en el entorno CLIPS
    template_string = """
    (deftemplate muros
      (slot izq (type INTEGER))
      (slot der (type INTEGER))
      (slot fr (type INTEGER))
      (slot det (type INTEGER)))
    """
    env.build(template_string)

    # Introducción del hecho muros con los valores obtenidos anteriormente
    muros = env.find_template('muros')
    fact = muros.assert_fact(izq=izq,
                             der=der,
                             fr=fr,
                             det=det)

    # Introducción de las reglas escritas por el usuario al entorno CLIPS
    for i in rules:
        env.build(i)

    # Ejecución del entorno CLIPS
    env.run()

    # Revisa los hechos después de la ejecución del entorno para que el agente realice los movimientos
    for fact in env.facts():
        if str(fact) == "(turn_right)":
            self.turn_right()
        if str(fact) == "(turn_left)":
            self.turn_left()
        if str(fact) == "(move_forward)":
            self.move_forward()
