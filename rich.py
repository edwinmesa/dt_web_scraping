shops = dict([
    ('Bogotá, D.c.', 'EXITO Calle 80'),
    ('Medellín', 'Exito Poblado'),
])


# for (col, row), piece in shops.items():
#     print(col, row, piece)


a_dict =  {'Bogotá, D.c.': 'EXITO Calle 80', 'Medellín': 'Exito Poblado'}
for city, suc in a_dict.items():
  print(city, '->', suc)