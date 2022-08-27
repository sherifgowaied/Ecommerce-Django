# Ecommerce-Django
##### supports:
* Login and Register 
* Put items in Cart 
* discount coupons
* Calculate Sales and disscount offers 
* Ready to link the app with stripe or paypal 
* pagination , Product Details
* Saving user info like adress ,Paying addres , billing address 
* Refund request of orders 
* unique Refrence code for every order for refund requests
* Admin Pannel with searching and filtering data feature through database

https://user-images.githubusercontent.com/91483223/186851214-6f97e753-e4e9-412e-b9af-01d4280ffaf6.mov



https://user-images.githubusercontent.com/91483223/186851228-d06556f8-4340-4465-8106-bcb11bca03c0.mov



https://user-images.githubusercontent.com/91483223/186851244-7a08e45b-5ef4-465e-b7a6-adcb16f77fc9.mov



https://user-images.githubusercontent.com/91483223/187027899-02fbeae4-2515-466d-a4ec-acba409d8709.mov



https://user-images.githubusercontent.com/91483223/187027998-aa6f91b1-aa7a-400a-838e-0249b548e6ea.mov

## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```



```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

Then install the project dependencies with

```
pip3 install -r requirements.txt
```

```
python3 manage.py makemigrations
```

```
python manage.py migrate
```

Now you can run the project with this command

```
python manage.py runserver
```

**Note** if you want payments to work you will need to enter your own Stripe API keys into the `.env` file in the settings files.

---


