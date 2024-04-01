from app import app

@app.get('/products')
def inventory():
    pass

@app.post('/products')
def add_prod():
    pass

@app.put('/products/<int:id>')
def update_prod():
    pass

@app.delete('/products/<int:id>')
def del_prod():
    pass