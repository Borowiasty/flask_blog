import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pictur_fn = random_hex + f_ext
    pictur_path = os.path.join(app.root_path, 'static/profile_pics', pictur_fn)
    
    output_size = (125, 125)
    resize_image = Image.open(form_picture)
    resize_image.thumbnail(output_size)
    resize_image.save(pictur_path)

    return pictur_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', 
                  sender= 'noreply@demo.com', 
                  recipients= [user.email])
    
    msg.body = f'''To reset your password, visit link:
{url_for('users.resetToken', token= token, _external= True)}

If you did not make this request, simply ignore this email and no changes will be made 
'''
    mail.send(msg)