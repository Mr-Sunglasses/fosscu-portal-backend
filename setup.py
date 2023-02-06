from main import db,Puppies

db.create_all()

Sam = Puppies(name="Sammy", age=3)
Frank = Puppies(name="Frankie", age=4)

print(Sam.id)
print(Frank.id)

db.session.add_all([Sam, Frank])

db.session.commit()

print(Sam.id)
print(Frank.id)