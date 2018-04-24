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
    restaurant = session.query(Restaurant).filter_by(id =
            restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    name = restaurant.name

    return render_template('menu.html', restaurant=restaurant ,restaurant_id = restaurant_id, name = name,items = items)




@app.route ('/restaurants/<int:restaurant_id>/menu/new',methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    prename = session.query(Restaurant).filter_by(id = restaurant_id).one()
    name = prename.name
    #return "This page will make new item for restaurant %s" % restaurant_id
    if request.method =='POST':
        newmenuItem = MenuItem(restaurant_id=restaurant_id,name = request.form['name'], price = request.form['price'],description = request.form['description'],course = request.form['course'])
        session.add(newmenuItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html',restaurant_id=restaurant_id,name=name)

@app.route ('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    prename = session.query(MenuItem).filter_by(id = menu_id).one()
    name = prename.name
    price = prename.price
    description = prename.description
    course = prename.course
    if request.method =='POST':
        if request.form['name']:
            prename.name = request.form['name']
            session.add(prename)
            session.commit()
        elif request.form['price']:
                    prename.price = request.form['price']
                    session.add(prename)
                    session.commit()
        elif request.form['description']:
                        prename.description = request.form['description']
                        session.add(prename)
                        session.commit()
        elif request.form['course']:
                            prename.course = request.form['course']
                            session.add(prename)
                            session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, name = name,
        price = price, description=description, course = course)




@app.route ('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    prename = session.query(MenuItem).filter_by(id = menu_id).one()
    menu_id = prename.id
    name = prename.name
    if request.method =='POST':
            session.delete(prename)
            session.commit()
            return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, name = name)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
