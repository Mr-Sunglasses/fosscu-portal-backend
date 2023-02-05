from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    puppies = {
        "Rufus": "Pompeiian",
        "Tom": "German Shepherd",
        "Jimmy": "Golden Retriever"
    }
    return render_template('home.html', puppies=puppies)

@app.route('/information')
def info():
    return render_template('info.html')


@app.route("/register")
def signup_form():
    return render_template('form.html')

@app.route("/thank_you")
def thank_you():
    Name = request.args.get("Name")
    Breed = request.args.get("Breed")
    return render_template('thankyou.html', Name=Name, Breed=Breed)

@app.route('/puppies/<name>')
def get_name(name):
    puppies = {
        "Rufus": "Pompeiian",
        "Tom": "German Shepherd",
        "Jimmy": "Golden Retriever"
    }
    search_name = name
    return render_template("search.html", puppies=puppies, search_name=search_name)


@app.route('/gen_pass')
def gen_pass():
    return render_template('form_pass.html')

@app.route('/verify_pass')
def verify_pass():
    password = request.args.get('get_pass')
    param1 = False
    param2 = False
    param3 = False
    for i in password:
        if i in range(0,10):
            param1 = True
            break
    for j in password:    
        if i in ["!", "@", "$"]:
            param2 = True
            break
    
    for k in password:
        if i in ["A","B","C"]:
            param3 = True
            break

        
    all_params = [param1, param2, param3]
    return render_template('verify_pass.html', password=password, all_params=all_params)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)