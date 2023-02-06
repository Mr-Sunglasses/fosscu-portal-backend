from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, RadioField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_key"

class Info_form(FlaskForm):
    Name = StringField(label="What is the Name of Your Puppy", validators=[DataRequired()])
    Breed = StringField(label="What is your breed ?", validators=[DataRequired()])
    neatured = BooleanField(label="Is Your Puppy Neatured ?")
    mood = RadioField(label="Please Choose Your Mood: ", choices=[('mood_one', 'Happy'), ('mood_two', 'Excited')])
    food_choice = SelectField(label= u"Pick Your Favorite Food ?", choices=[('food_1', 'Chicken'), ('food_2', 'Fish'), ('food_3', 'Goat')])
    feedback = TextAreaField(label=u"Please Give Us Feedback ?")
    Submit = SubmitField(label="Submit")


@app.route('/', methods=['GET', 'POST'])
def home():
    # breed = False

    form = Info_form()

    if form.validate_on_submit():
        session['name'] = form.Name.data
        session['breed'] = form.Breed.data
        session['neatured'] = form.neatured.data
        session['mood'] = form.mood.data
        session['food_choice'] = form.food_choice.data
        session['feedback'] = form.feedback.data

        flash(message=f"Thanks For Submitting the Information of {session['name']}")

        return redirect(url_for('thankyou'))
    
    return render_template('index.html', form=form)


@app.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(debug=True)
