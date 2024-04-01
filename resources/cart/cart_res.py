from app import app

@app.get('/cart')
def contents():
    pass

@app.post('/cart')
def add_item():
    pass

@app.put('/cart/<int:id>')
def update_item():
    pass

@app.delete('/cart/<int:id>')
def del_item():
    pass