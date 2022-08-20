def reset_environment(env):
    no_change = False
    while not no_change:  # He descubierto que un retract fastidia el bucle. Por eso hay que meterlo en un while
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
    # Resetear el hecho muros y PENDING FUNCTION CALLS
    env.assert_string("(pending_function_calls)")


def set_walls(env, paredes):
    muros = "(walls"

    for i in paredes:
        if paredes[i]:
            muros += " " + i

    muros += ")"

    env.assert_string(muros)


def donde_estoy(env):
    for fact in env.facts():
        if str(fact).startswith("(pos "):
            pos = str(fact)[:-1].split()[1:]
        if str(fact).startswith("(ori "):
            ori = str(fact)[:-1].split()[1:]

    return pos, ori


def reset_position(env, memory):
    no_change = False
    while not no_change:  # He descubierto que un retract fastidia el bucle. Por eso hay que meterlo en un while
        no_change = True

        for fact in env.facts():
            if str(fact).startswith("(pos "):
                fact.retract()
                no_change = False
            elif str(fact).startswith("(ori "):
                fact.retract()
                no_change = False

    env.assert_string("(pos 0 0)")
    env.assert_string("(ori 1 0)")
    memory.clear()


def refresh_position(env, j):
    pos, ori = donde_estoy(env)

    if j == "self.move_forward()":
        x = int(pos[0]) + int(ori[0])
        y = int(pos[1]) + int(ori[1])
        for fact in env.facts():
            if str(fact).startswith("(pos "):
                fact.retract()
                posicion = "(pos " + str(x) + " " + str(y) + ")"
                env.assert_string(posicion)

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
                orientacion = "(ori " + str(ori2[0]) + " " + str(ori2[1]) + ")"
                env.assert_string(orientacion)

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
                orientacion = "(ori " + str(ori2[0]) + " " + str(ori2[1]) + ")"
                env.assert_string(orientacion)


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
