
var web_url;

async function fashionNews(){

  let init = {
    mode: 'cors',
    method: 'GET',
  }
  url = "/fashionNews";
  let resp = await fetch(url, init);
  const response = await resp.json();

  document.getElementById("pic").innerHTML = "";
  var header = response[0];
  var abstract = response[1];
  web_url = response[2];
  var image = 'https://static01.nyt.com/'.concat(response[3]);
  console.log(image);
  document.getElementById("head").innerHTML = header;
  document.getElementById("abs").innerHTML = abstract;
  var showImg = document.createElement("img");
  showImg.setAttribute("src", image);


  // console.log(link);

  document.getElementById("pic").appendChild(showImg);
  // document.getElementById("head").appendChild(link);
}

function getlink(){
  // var link = header.link(web_url);
  location.replace(web_url);
}

async function add_to_cart(item, quantity) {
     let init = {
          method: 'GET',
     }
     var amount = document.getElementById('cart_amount').value;
     if (amount > quantity)
          $("#out_of_stock").modal("toggle")

     else {
          url = "/add_to_cart/" + item + "/" + amount;
          let resp = await fetch(url, init);
          response = await resp.json();
          if (response == '0')
               $("#please_log_in").modal("toggle");
          else {
               $("#add_to_cart").modal("toggle");
          }
     }
}

async function save_my_review(item) {
     console.log("Saving review for this item: " + item);
     var review = document.getElementById('review_description').value;
     var rating = 0;

     console.log(review);
     if (review == "")
     {
          review = "No description";
     }

     if (document.getElementById('star1').checked) {
          rating = 1;
          console.log("1 stars selected");
     }
     else if (document.getElementById('star2').checked) {
          rating = 2;
          console.log("2 stars selected");
     }
     else if (document.getElementById('star3').checked) {
          rating = 3;
          console.log("3 stars selected");
     }
     else if (document.getElementById('star4').checked) {
          rating = 4;
          console.log("4 stars selected");
     }
     else if (document.getElementById('star5').checked) {
          rating = 5;
          console.log("5 stars selected");
     }

     let init = {
          method: 'GET',
     }

     url = "/save_my_review/" + item + "/" + rating + "/" + review;
     let resp = await fetch(url, init);
     response = await resp.json();
     if (response == '0'){
          $("#please_log_in").modal("toggle");
     }
     else{
          window.location.reload(true);
     }
}

async function i_love_this(item) {
     let init = {
          method: 'GET',
     }

     url = "/i_love_this/" + item;
     let resp = await fetch(url, init);
     response = await resp.json();

     if (response == '0')
          $("#please_log_in").modal("toggle");
     else {
       window.location.reload(true);
     }

}
