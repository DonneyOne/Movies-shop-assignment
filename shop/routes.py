import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Producer, Movie, User, Review
from shop.forms import RegistrationForm, LoginForm, ReviewForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies, title='My Wonderful movie Shop')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/movie/<int:movie_id>", methods=['GET', 'POST'])
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.all()
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(username=current_user.username, review=form.review.data, item_id=movie_id)
        db.session.add(review)
        db.session.commit()
        flash('Your review is submitted')
        return redirect(url_for('home'))
    return render_template("movie.html", movie=movie, form=form, reviews=reviews)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.  You can now log in.')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    session["cart"] = []
    session["wishlist"] = []
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
        return render_template('login.html', form=form)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session["cart"] = []
    session["wishlist"] = []
    logout_user()
    return redirect(url_for('home'))


@app.route("/add_to_cart/<int:movie_id>")
def add_to_cart(movie_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(movie_id)
    flash("The movie is added to your shopping cart!")
    return redirect("/cart")

@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
    if "cart" not in session:
        flash('There is nothing in your cart.')
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}
        total_price = 0
        total_quantity = 0
        for item in items:
            movie = Movie.query.get_or_404(item)
            total_price += movie.price
            if movie.id in cart:
                cart[movie.id]["quantity"] += 1
            else:
                cart[movie.id] = {"quantity":1, "title": movie.title, "price":movie.price}
            total_quantity = sum(item['quantity'] for item in cart.values())
        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_quantity = total_quantity)
    return render_template('cart.html')

@app.route("/delete_movie/<int:movie_id>", methods=['GET', 'POST'])
def delete_movie(movie_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].remove(movie_id)
    flash("The movie has been removed from your shopping cart!")
    session.modified = True
    return redirect("/cart")
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if session["cart"] == []:
        flash("There are no purchases to pay for.")
        return redirect("/home")
    return render_template("checkout.html", title="checkout")

@app.route("/done", methods=["GET", "POST"])
def done():
    session["cart"] = []
    return render_template("done.html", title="Thanks")

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
    if "wishlist" not in session:
        flash('There is nothing in your wishlist.')
        return render_template("wishlist.html", display_wishlist = {}, total = 0)
    else:
        items = session["wishlist"]
        wishlist = {}
        total_price = 0
        total_quantity = 0
        for item in items:
            movie = Movie.query.get_or_404(item)
            total_price += movie.price
            if movie.id in wishlist:
                wishlist[movie.id]["quantity"] += 1
            else:
                wishlist[movie.id] = {"quantity":1, "title": movie.title, "price":movie.price}
            total_quantity = sum(item['quantity'] for item in wishlist.values())
    return render_template("wishlist.html", title='Your Wishlist', display_wishlist = wishlist, total = total_price, total_quantity = total_quantity)

@app.route("/delete_wishlist/<int:movie_id>", methods=['GET', 'POST'])
def delete_wishlist(movie_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(movie_id)
    flash("The movie has been removed from your wishlist!")
    session.modified = True
    return redirect("/wishlist")
@app.route("/add_to_wishlist/<int:movie_id>")
def add_to_wishlist(movie_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].append(movie_id)

    flash("The movie is added to your wishlist!")
    return redirect("/wishlist")
@app.route("/sortbyprice")
def sortbyprice():
    movies = Movie.query.order_by(Movie.price).all()
    return render_template("home.html", movies=movies)
@app.route("/sortbyprice2")
def sortbyprice2():
    movies = Movie.query.order_by(Movie.price).all()
    movies.reverse()
    return render_template("home.html", movies=movies)
    
