from flask import Flask, render_template,url_for,redirect,request
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#main page
@app.route('/')
@app.route('/restaurants')
def restaurantsList():
    restaurants = session.query(Restaurant).all()

    return render_template('restaurants.html', restaurants = restaurants)

#newres page
@app.route('/restaurants/new',methods=['GET', 'POST'])
def newRestaurant():
    if request.method =='POST':
        newres = Restaurant(name = request.form['name'])
        session.add(newres)
        session.commit()
        return redirect(url_for('restaurantsList'))
    else:
        return render_template('newRestaurant.html')


#edit page
@app.route('/restaurants/<int:restaurant_id>/edit',methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    name = (session.query(Restaurant).filter_by(id =restaurant_id).one()).name
    if request.method =='POST':
        restaurant_id = restaurant_id
        editres = session.query(Restaurant).filter_by(id = restaurant_id).one()
        editres.name = request.form['name']
        session.add(editres)
        session.commit()
        return redirect(url_for('restaurantsList'))
    else:
        return render_template('editRestaurant.html', restaurant_id = restaurant_id,name = name)




@app.route('/restaurants/<int:restaurant_id>/delete',methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    name = (session.query(Restaurant).filter_by(id =restaurant_id).one()).name
    if request.method =='POST':
        restaurant_id = restaurant_id
        editres = session.query(Restaurant).filter_by(id = restaurant_id).one()
        session.delete(editres)
        session.commit()
        return redirect(url_for('restaurantsList'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, name = name)
#end of main page routing#

#specific menu page routing#



@app.route ('/restaurants/<int:restaurant_id>')
@app.route ('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    #return "This page is the menu for the restaurant %s" % restaurant_id


    return render_template('menu.html',  restaurant_id = restaurant_id, items = items,name = name)




@app.route ('/restaurant/menu/new')
def newMenuItem():
    #return "This page will make new item for restaurant %s" % restaurant_id
    return render_template('newMenuItem.html', restaurant = restaurant)




@app.route ('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    name = (items[menu_id]['name'])
    #return "This page will edit menu item for menu %s" % menu_id
    return render_template('editMenuItem.html', restaurant = restaurant, restaurant_id = restaurant_id, menu_id = menu_id, name = name)




@app.route ('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    name = (items[menu_id]['name'])
    #return "This page will delete menu item for menu %s" % menu_id
    return render_template('deleteMenuItem.html', restaurant = restaurant, restaurant_id = restaurant_id, menu_id = menu_id, name = name)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
