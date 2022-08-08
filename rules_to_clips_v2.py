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
    # Resetear el hecho muros y PENDING FUNCTION CALLS
    env.assert_string("(pending_function_calls)")


def set_walls(env, paredes):
    muros = "(walls"

    for i in paredes:
        if paredes[i]:
            muros += " " + i

    muros += ")"

    env.assert_string(muros)
