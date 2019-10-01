from flask import render_template,url_for,request,redirect,flash,session, abort
from datetime import datetime
from todo.models import User, Bookmark
from todo.forms import BookmarkForm, SignupForm, LoginForm, RequestResetForm, ResetPasswordForm
from todo import app, db, login_manager, mail
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
import socket



#the user loader
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/edit/<int:bookmark_id>', methods=['GET','POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if bookmark.user != current_user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash('Bookmark edited Successfully')
        return redirect(url_for('bookmark'))
    return render_template('edit_bm.html', form=form)


@app.route('/delete/<int:bookmark_id>', methods=['GET','POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if bookmark.user != current_user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash(f'Successfully deleted {bookmark.description}')
        return redirect(url_for('bookmark'))
    return render_template('delete_bm.html', form=form)
    


def send_reset_email(user):
    #socket.getaddrinfo('localhost',5000)
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
        sender='abdullahomotoke@gmail.com', 
        recipients=[user.email])
    msg.body=f'''
            To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

Thank you
    '''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Confirmation email sent')
        return redirect(url_for('index'))
    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token')
        return redirect(url_for(reset_request))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash(f'Your Password has been updated successfully! Please Login.')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)


'''
@app.route('/edit/<int:bookmark_id>', methods=['GET','POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flask('Bookmark edited Successfully')
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form)
'''


#index page route
@app.route('/')
@login_required
def index():
    x=datetime.now()
    time=x.strftime('%X')
    date=x.strftime('%x')
    return render_template('index.html', user=current_user, time=time, date=date)



    #registration route
@app.route('/create-account',methods=['POST','GET'])
def register():
    form=SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {user.username}! Please Login.')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


    #Login route
@app.route('/Login', methods=['GET','POST'])
def login():
    title='Login'
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash(f'Successfully Logged in as {current_user.username}!')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', title=title, form=form)
    

    #Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

    #route to view your bookmarks
@app.route('/bookmark')
@login_required
def bookmark():
    title='Bookmark'
    #books=current_user.bookmarks.order_by(current_user.bookmarks.date.desc())
    books = current_user.bookmarks.order_by(Bookmark.date.desc())
    return render_template('bookmark.html',title=title,new_bookmarks=books)
   # return render_template('bookmark.html',title=title,new_bookmarks=models.Bookmark.newest(5))


    # route to add bookmark
@app.route('/add-bookmark',methods=['POST','GET'])
@login_required
def add_bm():
    title='Add bookmark'
    form = BookmarkForm()
    try:
        if form.validate_on_submit():
            url=form.url.data
            description=form.description.data
            bm = Bookmark(user=current_user, url=url, description=description)
            db.session.add(bm)
            db.session.commit()
            flash(f'Successfully Added {description}')
            return redirect(url_for('bookmark'))
    except:
        print('Error')

    return render_template('add_bm.html',title=title, form=form)
