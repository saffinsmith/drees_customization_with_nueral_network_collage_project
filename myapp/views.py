import pickle

import razorpay
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from keras.src.saving import load_model
from keras.src.utils import pad_sequences

from .models import PartsImage
from .forms import PartsForm

from datetime import datetime


# Create your views here.
def home(request):
    return render(request, 'home.html')


def add_category(request):
    c_name = request.POST['name']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO category VALUES(null,'" + c_name + "')")
    return HttpResponse("<script>alert('Category  Added...');window.location='/admin_home';</script>")



def add_category_expert(request):
    c_name = request.POST['name']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO category VALUES(null,'" + c_name + "')")
    return HttpResponse("<script>alert('Category  Added...');window.location='/expert_home';</script>")


def add_category_expert_link(request):
    return render(request, 'expert_add_category.html')


def add_category_link(request):
    return render(request, 'add_category.html')


def view_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    return render(request, 'view_category.html', {'data': pin})


def view_category_expert(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    return render(request, 'expert_view_category.html', {'data': pin})



def edit_category(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from category where category_id='" + id + "'")
    pin = cursor.fetchall()
    return render(request, 'edit_category.html', {'data': pin})


def update_category(request):
    cursor = connection.cursor()
    c_name = request.POST['name']

    id = request.POST['category_id']

    cursor.execute(
        "UPDATE category SET category_id = '" + id + "',name='" + c_name + "' WHERE category_id = '" + id + "' ")
    cursor.execute("SELECT * FROM category ")
    item = cursor.fetchall()
    return render(request, 'view_category.html', {'data': item})


def delete_category(request, id):
    cursor = connection.cursor()
    cursor.execute("delete  from category where category_id='" + id + "'")

    return HttpResponse("<script>alert('Deleted...');window.location='/view_category';</script>")


def add_fabrics(request):
    if request.method == "POST":
        id = request.POST['category_id']
        f_name = request.POST['fabric_name']
        f_price = request.POST['price']
        f_image = request.POST['image_url']

        cursor = connection.cursor()
        print('hi')
        cursor.execute(
            "INSERT INTO fabrics VALUES(null,'" + id + "','" + f_name + "','" + f_price + "','" + f_image + "')")
        return HttpResponse("<script>alert('Added successfully...');window.location='/admin_home';</script>")
    return render(request, 'add_fabrics.html')


def add_fabrics_link(request, id):
    return render(request, 'add_fabrics.html', {'category_id': id})


def view_fabrics(request, id):
    cursor = connection.cursor()
    cursor.execute(
        "select f.*,c.name from fabrics as f join category as c on f.category_id=c.category_id where f.category_id='" + id + "'")
    pin = cursor.fetchall()
    return render(request, 'view_fabrics.html', {'data': pin})


def edit_fabrics(request, f_id):
    cursor = connection.cursor()
    cursor.execute("select * from fabrics where fabrics_id='" + f_id + "'")
    pin = cursor.fetchall()
    return render(request, 'edit_fabrics.html', {'data': pin})


def update_fabrics(request):
    cursor = connection.cursor()

    f_name = request.POST['fabric_name']
    f_price = request.POST['price']
    f_image = request.POST['image_url']
    f_id = request.POST['fabrics_id']
    cursor.execute(
        "UPDATE fabrics SET fabrics_id='" + f_id + "', fabric_name='" + f_name + "' ,price='" + f_price + "',image_url='" + f_image + "' WHERE fabrics_id = '" + f_id + "'")
    cursor.execute("SELECT * FROM fabrics ")
    item = cursor.fetchall()
    return redirect("admin_home")


def delete_fabrics(request, f_id):
    cursor = connection.cursor()
    cursor.execute("delete  from fabrics where fabrics_id='" + f_id + "'")

    return HttpResponse("<script>alert('Deleted...');window.location='/view_fabrics';</script>")


def add_shirt_parts(request):
    p_name = request.POST['name']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO component_type VALUES(null,'" + p_name + "')")
    return HttpResponse("<script>alert('Items  Added...');window.location='/admin_home';</script>")


def add_parts_link(request):
    return render(request, 'add_shirt_parts.html')


import random


def view_parts_image_user(request, p_id, p_name):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT t.idcomponent_style_type,t.file_path,t.component_name,s.name from component_style_type as t join component_type as s on t.idcomponent_type=s.idcomponent_type where t.idcomponent_type='" + p_id + "' AND t.component_name='" + p_name + "' ")
    pin = cursor.fetchall()

    shuffled_data = list(pin)
    random.shuffle(shuffled_data)

    print(pin)
    return render(request, 'view_parts_image_user.html', {'data': shuffled_data, 'p_name': p_name})


def view_parts(request):
    cursor = connection.cursor()
    cursor.execute("select * from shirt_parts")
    pin = cursor.fetchall()
    return render(request, 'view_parts.html', {'data': pin})


def edit_parts(request, p_id):
    cursor = connection.cursor()
    cursor.execute("select * from component_type where idcomponent_type='" + p_id + "'")
    pin = cursor.fetchall()
    return render(request, 'edit_parts.html', {'data': pin})


def select_fabrics(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fabrics WHERE fabrics_id = %s", [id])
    pin = cursor.fetchone()
    f_url = pin[4] if pin else None
    if f_url:
        request.session['fabric_url'] = f_url
        request.session['fabric_id'] = id
        request.session['fabric_price'] = pin[3]
        print(f_url)
        return HttpResponse("<script>alert('Fabric selected...');window.location='/user_home';</script>")
    else:
        return HttpResponse("<script>alert('Fabric not found.');window.location='/user_home';</script>")


def select_part_by_user(request, id, cname):
    cursor = connection.cursor()
    cursor.execute("select * from component_style_type where idcomponent_style_type='" + str(id) + "'")
    pin = cursor.fetchone()
    img_path = pin[2]

    print(cname)

    print(id)
    cname = cname.lower()
    if cname == 'neck':
        request.session['neck_id'] = id
        request.session['neck_image'] = img_path
        print(cname + ":" + img_path)

    if cname == 'sleeve':
        request.session['sleev_id'] = id
        request.session['sleeve_image'] = img_path
        print(cname + ":" + img_path)

    return HttpResponse("<script>alert('Item Selected...');window.location='/view_part_user';</script>")


def select_size(request):
    price = request.session['fabric_price']
    price = int(price)
    amount = price * 5
    s = amount + 5000
    request.session['amount'] = s
    print(s)
    return render(request, 'select_size.html', {"amount": s})


def payment(request):
    qry = request.session['insert_query']
    cursor = connection.cursor()
    cursor.execute(qry)
    cursor.close()
    return redirect("user_home")


def payment_start(request):
    neck_id = request.session.get('neck_id')
    sleev_id = request.session.get('sleev_id')

    price = request.session.get('amount')
    fabric_id = request.session.get('fabric_id')

    if neck_id is None:
        neck_id = "3"
    if sleev_id is None:
        sleev_id = "1"

    if price is None:
        price = "1"
    if fabric_id is None:
        fabric_id = "1"

    user_id = request.session['user_id']
    user_date = request.POST["datepicker"]
    suggestion = request.POST["suggestion"]
    options = request.POST["options"]

    # cursor.execute("INSERT INTO user_selections VALUES(null,'"+user_id+"',curdate() ,'request','" + str(fabric_id) + "','" + str(price) + "','" + str(neck_id) + "','" + str(sleev_id) + "','"+user_date+"'  )")
    request.session[
        'insert_query'] = "INSERT INTO user_selections VALUES(null,'" + user_id + "',curdate() ,'request','" + str(
        fabric_id) + "','" + str(price) + "','" + str(neck_id) + "','" + str(sleev_id) + "','" + user_date + "' ,'"+options+"','"+suggestion+"','No Reply' )"
    keys_to_delete = ['neck_id', 'fabric_id', 'sleev_id', 'amount']
    for key in keys_to_delete:
        if key in request.session:
            del request.session[key]

    request.session.modified = True
    price = price * 100
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    return render(request, "payment.html", {"amount": price})


def user_view_order(request):
    cursor = connection.cursor()
    user_id = request.session['user_id']
    cursor.execute(
        "select us.* ,f.image_url from user_selections AS us JOIN fabrics AS f ON us.fabrics_id=f.fabrics_id where us.user_id='" + user_id + "'")
    pin = cursor.fetchall()
    return render(request, 'UserViewOrder.html', {'data': pin})



def expert_view_suggestion(request):
    cursor = connection.cursor()
    cursor.execute(
        "select us.* ,f.image_url from user_selections AS us JOIN fabrics AS f ON us.fabrics_id=f.fabrics_id and us.status !='cancel' ")
    pin = cursor.fetchall()
    return render(request, 'expert_view_suggestion.html', {'data': pin})


# views.py
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def expert_reply(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_selections WHERE user_selection_id=%s", [id])
    enquiry = cursor.fetchone()
    if request.method == "POST":
        reply = request.POST['reply']
        cursor.execute("""
            UPDATE user_selections
            SET reply=%s 
            WHERE user_selection_id=%s
        """, [reply, id])

        messages.success(request, "Reply sent successfully!")
        return redirect('/expert_view_suggestion')
    return render(request, 'expert_reply.html', {'data': enquiry})


def admin_view_order(request):
    cursor = connection.cursor()
    cursor.execute(
        "select us.* ,f.image_url from user_selections AS us JOIN fabrics AS f ON us.fabrics_id=f.fabrics_id and us.status !='cancel' ")
    pin = cursor.fetchall()
    return render(request, 'AdminViewOrder.html', {'data': pin})


def expert_view_order(request):
    cursor = connection.cursor()
    cursor.execute(
        "select us.* ,f.image_url from user_selections AS us JOIN fabrics AS f ON us.fabrics_id=f.fabrics_id and us.status !='cancel' ")
    pin = cursor.fetchall()
    return render(request, 'ExpertViewOrder.html', {'data': pin})



def admin_view_order_design(request, id):
    cursor = connection.cursor()
    print(id)
    cursor.execute("select * from user_selections where user_selection_id ='" + str(id) + "' ")
    pin = cursor.fetchone()
    fab_id = pin[4]
    neck_id = pin[6]
    sleeve_id = pin[7]

    cursor.execute("select image_url from fabrics where fabrics_id ='" + str(fab_id) + "' ")
    pin = cursor.fetchone()
    fab_url = pin[0]

    cursor.execute("select file_path from component_style_type where idcomponent_style_type ='" + str(neck_id) + "' ")
    pin = cursor.fetchone()
    neck_url = pin[0]

    cursor.execute("select file_path from component_style_type where idcomponent_style_type ='" + str(sleeve_id) + "' ")
    pin = cursor.fetchone()
    sleeve_url = pin[0]

    # request.session['fab']=fab_url
    # request.session['neck'] = neck_url
    # request.session['sleeve'] = sleeve_url

    return render(request, 'AdminViewUserDesign.html',
                  {'fab_url': fab_url, 'neck_url': neck_url, 'sleeve_url': sleeve_url})



def expert_view_order_design(request, id):
    cursor = connection.cursor()
    print(id)
    cursor.execute("select * from user_selections where user_selection_id ='" + str(id) + "' ")
    pin = cursor.fetchone()
    fab_id = pin[4]
    neck_id = pin[6]
    sleeve_id = pin[7]

    cursor.execute("select image_url from fabrics where fabrics_id ='" + str(fab_id) + "' ")
    pin = cursor.fetchone()
    fab_url = pin[0]

    cursor.execute("select file_path from component_style_type where idcomponent_style_type ='" + str(neck_id) + "' ")
    pin = cursor.fetchone()
    neck_url = pin[0]

    cursor.execute("select file_path from component_style_type where idcomponent_style_type ='" + str(sleeve_id) + "' ")
    pin = cursor.fetchone()
    sleeve_url = pin[0]

    # request.session['fab']=fab_url
    # request.session['neck'] = neck_url
    # request.session['sleeve'] = sleeve_url

    return render(request, 'ExpertViewUserDesign.html',
                  {'fab_url': fab_url, 'neck_url': neck_url, 'sleeve_url': sleeve_url})



def make_order(request):
    yoke_id = request.session['yoke_id']
    sleev_id = request.session['sleev_id']
    collar_id = request.session['collar_id']
    button_id = request.session['button_id']
    pocket_id = request.session['pocket_id']
    cuff_id = request.session['cuff_id']

    price = request.session['fabric_price']
    fabric_id = request.session['fabric_id']
    user_id = request.session['user_id']
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO user_selections VALUES(null,'0','" + collar_id + "','" + pocket_id + "','" + button_id + "','" + cuff_id + "','" + yoke_id + "','" + sleev_id + "','" + user_id + "',curdate(),'request','" + fabric_id + "','" + amount + "')")
    return HttpResponse("<script>alert('Items  Added...');window.location='/view_part_user';</script>")


def update_parts(request):
    cursor = connection.cursor()
    p_name = request.POST['name']

    p_id = request.POST['shirt_parts_id']

    cursor.execute(
        "UPDATE component_type SET name='" + p_name + "' WHERE idcomponent_type = '" + p_id + "' ")
    cursor.execute("SELECT * FROM component_type ")
    item = cursor.fetchall()
    return render(request, 'view_parts.html', {'data': item})


def delete_parts(request, p_id):
    cursor = connection.cursor()
    cursor.execute("DELETE from component_type where idcomponent_type='" + p_id + "'")
    return HttpResponse("<script>alert('Deleted successfully..');window.location='/view_parts';</script>")


# add parts image
def add_parts_image(request):
    if request.method == "POST":
        p_id = request.POST['shirt_parts_id']
        p_path = request.POST['file_path']
        p_component = request.POST['component_name']
        cursor = connection.cursor()
        print(p_id)
        cursor.execute(
            "INSERT INTO shirt_parts_images VALUES(null,'" + p_id + "','" + p_path + "','" + p_component + "')")
        return HttpResponse("<script>alert('Items  Added...');window.location='/view_parts';</script>")
    return render(request, 'add_parts_image.html')


def add_measurements(request):
    if request.method == "POST":
        user_id = request.session["user_id"]
        waist = request.POST['waist']
        Hip = request.POST['Hip']
        Length = request.POST['Length']
        shoulder_full_length = request.POST['shoulder_full_length']
        arm_around = request.POST['arm_around']
        front_neck_depth = request.POST['front_neck_depth']
        sleev_length = request.POST['sleev_length']

        sleev_opening = request.POST['sleev_opening']
        shoulder = request.POST['shoulder']
        back_neck_depth = request.POST['back_neck_depth']
        blowse_length = request.POST['blowse_length']

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO measurement VALUES(null,'" + user_id + "','" + waist + "','" + Hip + "','" + Length + "','" + shoulder_full_length + "','" + arm_around + "','" + front_neck_depth + "','" + sleev_length + "','" + sleev_opening + "','" + shoulder + "','" + back_neck_depth + "','" + blowse_length + "','set')")
        cursor.close()
        return HttpResponse("<script>alert('Items  Added...');window.location='/select_size';</script>")
    return render(request, 'user_measurement.html')


def cancel_order(request, id):
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute("update user_selections set status='cancel' where user_selection_id=%s", [id])
        return redirect("user_home")
    return redirect("user_home")


def send_feedback(request):
    if request.method == "POST":
        cursor = connection.cursor()
        user_id=request.session["user_id"]
        details=request.POST['feedback']
        cursor.execute("insert into feedback values(null,'"+user_id+"' ,curdate(),'"+details+"' )")
        return redirect("user_home")
    return render(request, 'send_feedback.html')



def admin_view_cancel_order(request):
    cursor = connection.cursor()
    cursor.execute("select us.* ,f.image_url from user_selections AS us JOIN fabrics AS f ON us.fabrics_id=f.fabrics_id where us.status ='cancel'")
    pin = cursor.fetchall()
    cursor.close()
    return render(request, 'AdminViewCancelOrder.html', {'data': pin})


def admin_view_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select   * from feedback")
    pin = cursor.fetchall()
    cursor.close()
    return render(request, 'AdminViewFeedback.html', {'data': pin})



def admin_view_measurements_link(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from measurement where user_id='" + id + "' ")
    pin = cursor.fetchone()
    if pin:
        cursor.close()
        return render(request, 'admin_view_user_measurement.html', {'data': pin})
    return redirect("admin_home")


def expert_view_measurements_link(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from measurement where user_id='" + id + "' ")
    pin = cursor.fetchone()
    if pin:
        cursor.close()
        return render(request, 'expert_view_user_measurement.html', {'data': pin})
    return redirect("expert_home")



def measurements_link(request):
    cursor = connection.cursor()
    user_id = request.session["user_id"]
    cursor.execute("select * from measurement where user_id='" + user_id + "' ")
    pin = cursor.fetchone()
    if pin:
        cursor.close()
        return render(request, 'ViewMeasurements.html', {'data': pin})
    return render(request, 'user_measurement.html')


def view_measurements(request):
    cursor = connection.cursor()
    user_id = request.session["user_id"]
    cursor.execute("select * from measurement where user_id='" + user_id + "' ")
    pin = cursor.fetchone()
    cursor.close()
    return render(request, 'ViewMeasurements.html', {'data': pin})


def work_completed(request, id):
    cursor = connection.cursor()
    cursor.execute(
        "update user_selections set status='Work completed and shipped' where user_selection_id='" + id + "' ")
    pin = cursor.fetchone()
    cursor.close()
    return redirect("admin_home")


def expert_work_completed(request, id):
    cursor = connection.cursor()
    cursor.execute(
        "update user_selections set status='Work completed and shipped' where user_selection_id='" + id + "' ")
    pin = cursor.fetchone()
    cursor.close()
    return redirect("expert_home")


def date_changed(request, id):
    cursor = connection.cursor()
    cursor.execute(
        "update user_selections set status='Date changed' where user_selection_id='" + id + "' ")
    pin = cursor.fetchone()
    cursor.close()
    return redirect("admin_home")


def expert_date_changed(request, id):
    cursor = connection.cursor()
    cursor.execute(
        "update user_selections set status='Date changed' where user_selection_id='" + id + "' ")
    pin = cursor.fetchone()
    cursor.close()
    return redirect("expert_home")





def add_parts_image_link(request, p_id):
    print(p_id)

    return render(request, 'add_parts_image.html', {'shirt_parts_id': p_id})


def view_parts_image(request):
    cursor = connection.cursor()
    # p_id=request.POST['shirt_parts_id']
    # cursor.execute("SELECT t.shirt_parts_id,t.file_path,t.component_name,s.name from shirt_parts_images as t join shirt_parts as s on t.shirt_parts_id=s.shirt_parts_id where t.shirt_parts_id='"+p_id+"'")
    cursor.execute("select * from shirt_parts_images")
    pin = cursor.fetchall()
    return render(request, 'view_parts_image.html', {'data': pin})


def edit_parts_image(request, image_id):
    cursor = connection.cursor()
    cursor.execute("select * from shirt_parts_images where id='" + image_id + "'")
    pin = cursor.fetchall()
    return render(request, 'edit_parts_image.html', {'data': pin})


def update_parts_image(request):
    cursor = connection.cursor()
    p_id = request.POST['shirt_parts_id']
    f_path = request.POST['file_path']
    c_name = request.POST['component_name']
    image_id = request.POST['shirt_parts_image_id']
    cursor.execute(
        "UPDATE shirt_parts_images SET id='" + image_id + "', shirt_parts_id = '" + p_id + "',file_path='" + f_path + "' ,component_name='" + c_name + "' WHERE id = '" + image_id + "' ")
    cursor.execute("SELECT * FROM shirt_parts_images ")
    item = cursor.fetchall()
    return render(request, 'view_parts_image.html', {'data': item})


def delete_parts_image(request, image_id):
    cursor = connection.cursor()
    cursor.execute("DELETE from shirt_parts_images where id='" + image_id + "'")
    return HttpResponse("<script>alert('Deleted successfully..');window.location='/view_parts_image';</script>")


def view_category_user(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    return render(request, 'view_category_user.html', {'data': pin})


def view_shirt_part(request, p_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT t.shirt_parts_id,t.file_path,t.component_name,s.name from component_style_type as t join component_type as s on t.shirt_parts_id=s.shirt_parts_id where t.shirt_parts_id='" + p_id + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, 'view_shirt_part.html', {'data': pin})


def view_part_user(request):
    cursor = connection.cursor()
    cursor.execute("select * from component_type")
    pin = cursor.fetchall()
    return render(request, 'view_part_user.html', {'data': pin})


def view_fabrics_user(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from fabrics where category_id='" + id + "'")
    pin = cursor.fetchall()
    return render(request, 'view_fabrics_user.html', {'data': pin})


def view_selection(request):
    return render(request, 'view_user_selections.html')


def user_nav(request):
    return render(request, 'user_nav.html')


def navigation_design(request):
    return render(request, 'navigation_design.html')


def base(request):
    return render(request, 'base.html')


def user_page(request):
    return render(request, 'user_page.html')


def navbar(request):
    return render(request, 'navbar.html')


def add_cart(request):
    return render(request, 'add_cart.html')


# user registration



def user_registration(request):
    user_name = request.POST['name']
    user_address = request.POST['address']
    user_email = request.POST['email']
    user_id = request.POST['user_id']
    user_contact = request.POST['phone']
    user_password = request.POST['password']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_register WHERE user_id = %s", [user_id])
    data = cursor.fetchone()
    if data:
        return HttpResponse("<script>alert('User ID already exists');window.location='registration_link';</script>")
    else:
        cursor.execute(
            "INSERT INTO user_register (user_id, name, address, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s)",
            [user_id, user_name, user_address, user_email, user_contact, user_password]
        )
        return HttpResponse("<script>alert('Registration Successfully');window.location='login_link';</script>")



def registration_link(request):
    return render(request, 'user_registration.html')


def view_user_register(request):
    cursor = connection.cursor()
    cursor.execute("select * from user_register")
    pin = cursor.fetchall()
    print(pin)
    return render(request, 'view_user_register.html', {'data': pin})


def admin_view_order_report(request):
    cursor = connection.cursor()
    cursor.execute("select * from user_selections where status !='cancel'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, 'AdminViewOrderReport.html', {'data': pin})


def admin_view_cancel_report(request):
    cursor = connection.cursor()
    cursor.execute("select * from user_selections where status='cancel' ")
    pin = cursor.fetchall()
    print(pin)
    return render(request, 'AdminViewCancelReport.html', {'data': pin})


# delete user registration
def delete_user(request, u_id):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user_register WHERE user_id=" + str(u_id) + " ")
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/view_user_register';</script>")


def edit_user_register(request, u_id):
    cursor = connection.cursor()
    cursor.execute("select * from user_register")
    pin = cursor.fetchall()
    print(pin)
    return render(request, 'edit_user_register.html', {'data': pin})


def update_user_register(request):
    cursor = connection.cursor()
    u_id = request.POST['user_id']
    user_name = request.POST['name']
    user_address = request.POST['address']
    user_contact = request.POST['contact']
    user_email = request.POST['email']
    user_password = request.POST['password']
    cursor.execute(
        "UPDATE user_register SET user_id = '" + u_id + "',name='" + user_name + "',address='" + user_address + "',contact='" + user_contact + "',email='" + user_email + "',password='" + user_password + "'WHERE user_id = '" + u_id + "' ")
    cursor.execute("SELECT * FROM user_register")
    item = cursor.fetchall()
    return render(request, 'view_user_register.html', {'data': item})


def login(request):
    if request.method == "POST":
        u_id = request.POST['user_id']
        user_password = request.POST['password']
        cursor = connection.cursor()
        request.session["user_id"] = u_id

        cursor.execute("SELECT * FROM expert WHERE expert_id = '" + u_id + "' AND password = '" + user_password + "'")
        admin_result = cursor.fetchone()

        if admin_result:
            request.session["user_id"] = u_id
            return redirect('expert_home')

        cursor.execute("SELECT * FROM user_register WHERE user_id = '" + u_id + "' AND password = '" + user_password + "' ")
        user_result = cursor.fetchone()

        if user_result:
            return redirect('user_rec')
            #return redirect('user_home')

        # Check admin login
        cursor.execute("SELECT * FROM login WHERE admin_id = '" + u_id + "' AND password = '" + user_password + "'")
        admin_result = cursor.fetchone()

        if admin_result:
            request.session["user_id"] = u_id
            return redirect('admin_home')

        return HttpResponse("<script>alert('Invalid credentials');window.location='/';</script>")
    else:
        return HttpResponse("<script>alert('Invalid request method');window.location='/';</script>")


def login_link(request):
    return render(request, 'login.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def expert_home(request):
    return render(request, 'expert_home.html')



def adminheader(request):
    return render(request, 'adminheader.html')


def adminfooter(request):
    return render(request, 'adminfooter.html')


def user_home(request):
    return render(request, 'user_home.html')


def turf_header(request):
    return render(request, 'turf_header.html')


def admin_design(request):
    return render(request, 'admin_design.html')


def about(request):
    return render(request, 'about.html')


def user_design(request):
    return render(request, 'user_design.html')


def admin_navigation(request):
    return render(request, 'admin_navigation.html')


def registerheader(request):
    return render(request, 'registerheader.html')


def registerfooter(request):
    return render(request, 'registerfooter.html')


def user_rec(request):
    return render(request, 'recoment.html')


def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'logout.html')


def view_booking_admin(request):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT b.idbooking, b.user_id,t.address, b.book_date, b.hour, b.status FROM booking AS b JOIN turf_register AS t ON t.turf_register_no = b.turf_register_no JOIN district AS d ON t.district_id = d.district_id JOIN place AS p ON t.place_id = p.place_id ")
    pin = cursor.fetchall()
    print(pin)
    return render(request, 'view_booking_admin.html', {'data': pin})


correct_count = 0

# --------------------------------------------------------------
from django.db import connection


def load_question(request):
    cursor = connection.cursor()
    cursor.execute("SELECT question, answer FROM data")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    df = pd.DataFrame(data, columns=['question', 'answer'])
    return render(request, 'view_bills.html', {'data': data})


import pandas as pd
import numpy as np
import tensorflow as tf

with open(r"doc\tokens.pkl", "rb") as file:
    tokenizer = pickle.load(file)
model = load_model(r"doc\Fashion_Model.keras")


def generate_answer(question):
    seq = tokenizer.texts_to_sequences([question])
    seq = pad_sequences(seq, maxlen=13, padding='post')
    pred = model.predict(seq)
    pred_index = np.argmax(pred, axis=-1)

    answer_words = [tokenizer.index_word.get(idx, '') for idx in pred_index[0] if idx != 0]
    return ' '.join(answer_words)


from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render
import json


def call_first(request):
    if request.method == 'POST':
        # Get user input from the POST request
        body = json.loads(request.body)
        user_input = body.get('user_input', '')

        generated_answer = generate_answer(user_input)
        print("Generated Answer:", generated_answer)

        return JsonResponse({'generated_answer': generated_answer})

    # Handle GET request for rendering the HTML page
    return render(request, 'ViewBot.html')
