import clips


# Comprobar las percepciones del agente
def what_I_see(self):
    things = self.whats_here()
    walls = things['walls']
    objects = things['objects']
    return walls, objects


# Comprobar la posición y la orientación del agente
def where_I_am(env):
    for fact in env.facts():
        if str(fact).startswith("(pos "):
            pos = str(fact)[:-1].split()[1:]
        if str(fact).startswith("(ori "):
            ori = str(fact)[:-1].split()[1:]

    return pos, ori


# Reiniciar el entorno CLIPS del agente
def reset_environment(env):
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
            elif str(fact).startswith("(caution_loop)"):
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


# Reinicia la posición del agente y limpia su memoria
def reset_position(env, memory):
    no_change = False
    while not no_change:
        no_change = True

        for fact in env.facts():
            if str(fact).startswith("(pos "):
                fact.retract()
                no_change = False
            elif str(fact).startswith("(ori "):
                fact.retract()
                no_change = False

    # Reinicia los hechos de posición y orientación
    env.assert_string("(pos 0 0)")
    env.assert_string("(ori 1 0)")
    memory.clear()


# Comprobar si el agente ha pasado por una misma posición en tres ocasiones
def check_memory(memory, env):

    position = ['0', '0']
    for fact in env.facts():
        if str(fact).startswith("(pos "):
            position = str(fact)[:-1].split()[1:]

    found = False
    for i in memory:
        if i[0] == position:
            i[1] += 1
            found = True
            if i[1] >= 5:
                env.assert_string("(caution_loop)")

    if not found:
        memory.append([position, 1])


def algorithm(objects, env, available=None):
    # Crear las posibles funciones accesibles al agente
    for i in objects:
        for key in i:
            if key.endswith('_function'):
                object_function = "ob_" + str(id(i)) + "_funct"
                available = {object_function: i[key]}
                new_object = '(available_object ' + str(
                    i['type']) + ' "' + "available_objects" + "['" + object_function + "']" + '(self)")'
                env.assert_string(new_object)

    # Ejecutar pasos de agente
    env.run(1)

    # Conseguir las funciones del hecho PENDING_FUNCTION_CALLS para devolverlas
    for i, fact in enumerate(env.facts()):
        if str(fact).startswith("(pending_function_calls"):
            funct = str(fact)[:-1].split()[1:]

    return funct, available


class Agent_CLIPS:

    # Se inicializa el entorno y se añaden las reglas CLIPS
    def __init__(self, path):
        self.env = clips.Environment()
        self.env.load(path)
        self.env.reset()
        self.memory = []

    # Actualizar el entorno CLIPS y devolver las percepciones del agente
    def agent_context(self, agent):
        # Reiniciar el entorno CLIPS borrando los hechos innecesarios
        reset_environment(self.env)

        # Obtener las percepciones del agente
        walls, objects = what_I_see(agent)

        # Crea el hecho de muros en el entorno CLIPS
        set_walls(self.env, walls)

        # Actualiza la memoria
        check_memory(self.memory, self.env)

        return walls, objects
