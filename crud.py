from main import db,Puppies


## Create 
js = Puppies(name="Julian", age=1)

db.session.add(js)
db.session.commit()

## Read
all_puppies = Puppies.query.all()
print(all_puppies)


# Select by Id
puppy1 = Puppies.query.get(1)
print(puppy1.name)

# Filter
julian_puppy = Puppies.query.filter_by(name='Julian')
print(julian_puppy.all())


# Update
first_puppy = Puppies.query.get(1)
first_puppy.age = 5
db.session.add(first_puppy)
db.session.commit()


# Delete
last_puppy = Puppies.query.get(3)
db.session.delete(last_puppy)
db.session.commit()

# All puppies
all_puppies = Puppies.query.all()
print(all_puppies)