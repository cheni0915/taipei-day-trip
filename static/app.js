// 抓取圖片放置位置
let attractions_image = document.getElementsByClassName("attractions__image");
let attractions_name = document.getElementsByClassName("attractions__name");
let attractions_mrt = document.getElementsByClassName("attractions__mrt");
let attractions_cat = document.getElementsByClassName("attractions__cat");

// 12筆資料
console.log(attractions_mrt);


fetch(request, {mode: 'cors'});
fetch(
    "http://18.180.213.40:3000/api/attractions?page=1"
).then(function(response){
    console.log(123);
    return response.json();
}).then(function(data){
    console.log(data);
});