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
            elif str(fact).startswith("(caution_loop"):
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


# Actualizar la posición y la orientación del agente dependiendo de sus movimientos
def refresh_position(env, j):
    pos, ori = where_I_am(env)

    if j == "self.move_forward()":
        x = int(pos[0]) + int(ori[0])
        y = int(pos[1]) + int(ori[1])
        for fact in env.facts():
            if str(fact).startswith("(pos "):
                fact.retract()
                position = "(pos " + str(x) + " " + str(y) + ")"
                env.assert_string(position)

    elif j == "self.turn_right()":
        if ori == ['1', '0']:
            ori2 = ['0', '1']
        elif ori == ['0', '1']:
            ori2 = ['-1', '0']
        elif ori == ['-1', '0']:
            ori2 = ['0', '-1']
        elif ori == ['0', '-1']:
            ori2 = ['1', '0']
        for fact in env.facts():
            if str(fact).startswith("(ori "):
                fact.retract()
                orientation = "(ori " + str(ori2[0]) + " " + str(ori2[1]) + ")"
                env.assert_string(orientation)

    elif j == "self.turn_left()":
        if ori == ['1', '0']:
            ori2 = ['0', '-1']
        elif ori == ['0', '-1']:
            ori2 = ['-1', '0']
        elif ori == ['-1', '0']:
            ori2 = ['0', '1']
        elif ori == ['0', '1']:
            ori2 = ['1', '0']
        for fact in env.facts():
            if str(fact).startswith("(ori "):
                fact.retract()
                orientation = "(ori " + str(ori2[0]) + " " + str(ori2[1]) + ")"
                env.assert_string(orientation)


# Comprobar si el agente ha pasado por una misma posición en tres ocasiones
def check_memory(memory, pos, env):

    found = False
    for i in memory:
        if i[0] == pos:
            i[1] += 1
            found = True

    if not found:
        memory.append([pos, 1])

    for j in memory:
        if j[1] >= 3:
            env.assert_string("(caution_loop)")
            j[1] = 0


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
    def __init__(self, rules):
        self.env = clips.Environment()
        for i in rules:
            self.env.build(i)
        self.env.reset()
        self.memory = []

    # Actualizar el entorno CLIPS y devolver las percepciones del agente
    def agent_context(self, agent):
        # Reiniciar el entorno CLIPS borrando los hechos innecesarios
        reset_environment(self.env)

        # Obtener las percepciones del agente
        walls, objects = what_I_see(agent)

        # Obtener la posición del agente
        pos, ori = where_I_am(self.env)

        # Crea el hecho de muros en el entorno CLIPS
        set_walls(self.env, walls)

        # Actualiza la memoria
        check_memory(self.memory, pos, self.env)

        return walls, objects, pos, ori
