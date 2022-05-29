
def get_data_from_params(request):
    if request.args:
        data = request.args.getlist('ingredients[]')
    elif request.form:
        data = list(request.form.listvalues())[0]
    elif request.json:
        data = [ i['ingredients[]'] for i in request.json]
    else:
        data = []

    return data
