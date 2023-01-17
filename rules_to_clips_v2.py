import clips


# Comprobar las percepciones del agente
def what_I_see(self):
    things = self.whats_here()
    walls = things['walls']
    objects = things['objects']
    return walls, objects


# Reiniciar el entorno CLIPS del agente
def reset_environment(env):
    env.strategy = clips.common.Strategy.RANDOM
    no_change = False
    while not no_change:
        no_change = True

        for fact in env.facts():
            if str(fact).startswith("(walls "):
                fact.retract()
                no_change = False
            elif str(fact).startswith("(pending_function_calls"):
                fact.retract()
                no_change = False
            elif str(fact).startswith("(available_object"):
                fact.retract()
                no_change = False
    # Resetear el hecho PENDING FUNCTION CALLS
    env.assert_string("(pending_function_calls)")


# Crear y añadir el hecho walls en el entorno CLIPS
def set_walls(env, walls):
    fact = "(walls"
    for i in walls:
        if walls[i]:
            fact += " " + i
    fact += ")"
    env.assert_string(fact)
    
    
def move(self):
  # Elimina los hechos que no necesita del entorno CLIPS
  reset_environment(env)

  # Recoge las paredes y objetos que detecta el agente
  walls, objects = what_I_see(self)

  # Crear el hecho de las paredes en el entorno CLIPS
  set_walls(env,walls)

  # Crear las posibles funciones accesibles al agente
  for i in objects:
        for key in i:
            if key.endswith('_function'):
                object_function = "ob_" + str(id(i)) + "_funct"
                available_objects = {object_function: i[key]}
                new_object = '(available_object ' + str(
                    i['type']) + ' "' + "available_objects" + "['" + object_function + "']" + '(self)")'
                env.assert_string(new_object)

  # Ejecutar pasos de agente
  env.run(1)

  # Ejecutar las opciones en pending_function_calls
  for i, fact in enumerate(env.facts()):
    if str(fact).startswith("(pending_function_calls"):
      functions = str(fact)[:-1].split()[1:]
      for j in functions:
        eval(j.replace('"',''))
