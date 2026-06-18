
def divide(state:dict) -> dict:
    try:
        return {'result': state['a'] / state['b']}
    except Exception as e:
        return {'result': 0}
