import clips


# Comprobar las percepciones del agente
def what_I_see(self):
    things = self.whats_here()
    walls = things['walls']
    objects = things['objects']
    return walls, objects


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
