# CSCI4131-Final-Project
Submission Guidelines
1. Project Type: Plan A 
2. Group Members Name: Khai Nguyen, Benjamin Nhan, Amanda Wang
3. Link to live Application: https://shielded-eyrie-08354.herokuapp.com/
4. Link to Github Code Repository: https://github.umn.edu/nguy2625/CSCI4131-Final-Project
5. List of Technologies/API's Used: New York Times Search News API
6. Detailed Description of the project (No more than 500 words)
 
We have created an online shopping website selling Clothings and Accessories for both men and women. The user will be able to view top selling items, and latest fashion news. The user will also be able to like the item, and leave a review for the item bought. Four sql tables were used not including the user table that manages login which are “inventory”, “most_liked”, “review”, and “shoppingcart”. 
 
The user will be able to Login in the top right corner of the page. The user is required to create an account before logging in. Once an account has been created, the user will be prompted to sign in. If the user checks “remember me”, it will be managed by flask-login to keep the user logged in even after closing the page, until the user chooses to logout. The login button on the top right corner will then change to logout after signing in, and a shopping cart icon will appear. On the home page, the user will be able to view the top-selling items as well as the latest fashion news. Top-selling items were determined by the highest number of items that were added to the users’ cart. The latest fashion news was implemented using NewYorkTimes API where fashion related articles from year 2019 or later will be generated randomly each time the screen refreshes. 
 
The user will be able to shop in two categories, clothes and accessories and the user will be redirected to the page accordingly. On clicking the item on the page, a single-product view will appear where the image, name of the item, the price, and its quantity on the inventory will appear. The user will be able to add the item to cart by incrementing the quantity and clicking on “add to cart”. This will decrease the quantity of the item in the inventory and the shopping cart of the user will be updated to include the item. On clicking “Love” the button will be changed to “Loved” since users will only be able to like each item only once. and most liked items will be updated on the most_liked database. Below the “Add to Cart” and “Love” button, a review section is available for users to leave a rating and a review. On clicking “Submit now” the rating and review will be added to the review database and will be displayed on the single-product page corresponding to the item. Below that is a list of top 2 best selling items that are in the same category as the one the user clicked on.

7. List of Controllers and their short description (No more than 50 words for each controller)
index() - 
    The home page of the web application. Displays best-selling items using inventory table and the latest fashion news

fashionNews() - 
    Get news headline, abstract, web URL and image from NewYorkTimes API and displays headline, abstract, and image.  Clicking     on the headline will bring you to the actual article. 
    
category(selection) - 
    Determines if user chooses to browse clothes or accessories. Uses inventory table to get corresponding items.

register() - 
    Registers user and stores user into user table. Checks if account has been made under the same username.

login() - 
    Logs in user. Checks if hashed password matches the username. Redirect to the home page if  successful.

logout() - 
    Logs out user. Redirects to homepage.

singleProduct(item) - 
    Manages review table for each item includes review description and the rating. 

cart() - 
    Keeps track of items in shopping cart for each user

add_to_cart(item, amount) - 
    Insert item into shopping cart table 

i_love_this(item) - 
    Puts user id and item chosen in a most_liked table 

save_my_review() - 
    Puts item, user, rating, and description in a review table 
 
8. List of Views and their short description (No more than 50 words for each view)
'/' - 
The Homepage. Shows the top selling items and the latest fashion news. On the left side of the navigation bar, the menu shows “Home”, a dropdown “Shop” for the two categories, and “Contact”. The right side allows user login and a shopping cart after login. 

'/category/<selection>' - 
Page of the category (clothing or accessories) selected by the user. Displays items in selected category.

'/register.html' - 
Allows the user to register with username and password if new to account.

'/login.html' - 
Allows the user to login with username and password after creating the account with the “remember me” option.

'/single-product.html/<item>' - 
Displays the image of the item, name, price, category, quantity. The user will be able to like, purchase, and leave a review.

'/cart.html' - 
Shows items in the user’s cart with price, quantity, and total. Option to continue shopping. Will prompt the user to login if not logged in. 
 
9. List of Tables, their Structure and short description
Inventory - 
Table of all items with its id, item name, image source, category, quantity, and price
Keep track of every item in the shop and its available quantity. The image source contains the path to the image so that the shop can display the image of the item correctly. Category determines the type of item, “Clothes” or “Accessories”
 
Most_liked - 
Table with liked id, user id, and item name
“User_id” and “item_name” are foreign keys that point to inventory and user tables. This table keeps track of the item that the user loved.

Review - 
Table with review id, user id, item_id, rating, and review.
If a rating was given and no reviews were given, default review will be no description. “User_id” and “item_id” are foreign keys that point to inventory and user tables. Keep tracks all reviews, ratings, and the person who wrote the review, and which items the reviews are for.

Shoppingcart - 
Table with cart id, user id, item id, and quantity
“User_id” and “item_id” are foreign keys that point to inventory and user tables. Keep track of items that a user added to the cart.

User_account - User table containing user id, and hashed password
 
10. References/Resources: List all the references, resources or the online templates that were used for the project.
    New York Times API 
    https://developer.nytimes.com/docs/articlesearch-product/1/overview
    
    Bootstrap Online Website Template 
    https://colorlib.com/wp/template/winter/
 
