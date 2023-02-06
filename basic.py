from main import db, Puppy, Owner, Toy

# rufus = Puppy(name="Rufus")
# fido = Puppy(name="Fido")
#
# db.session.add_all([rufus, fido])
# db.session.commit()
#
# # Check
# print(Puppy.query.all())
#
# rufus = Puppy.query.filter_by(name='Rufus').first()
# print(rufus)
#
# kanishk = Owner(owner_name="Kanishk", puppy_id=rufus.id)
#
# toy1 = Toy(item_name="Chew_Toy", puppy_id=rufus.id)
# toy2 = Toy(item_name="Fricker", puppy_id=rufus.id)
#
# db.session.add_all([kanishk, toy1, toy2])
# db.session.commit()

rufus = Puppy.query.filter_by(name='Rufus').first()
print(rufus)
print(rufus.report_toys())