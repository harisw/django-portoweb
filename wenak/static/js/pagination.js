var contentDiv = document.getElementById('recipeContent');
var targetUrl;
var recipeUrl = window.location.origin + "/wenak/recipe/";
var loading = document.getElementById('boxLoading');
var recipeDiv = document.getElementById('recipeDiv');
var page = 1;
var limit = 25;
var max_page = 0;
var paginations = ``;
var initial = true;
var max_reach = 6;
var max_pagination = 12;
function updatePagination(){
    var start_pagination = page <= max_reach ? 1 : page-max_reach;

    var count = 1;
    for(var j=start_pagination; j<=max_page; j++){
        if(count >= max_pagination)
            break;

        paginations += `<button type="button" class="btn main-sec-color page-btn" >${j}</button>`;
        count++;
    }
    $('.page-btn').remove();

    $(paginations).insertAfter(".prev-page-btn");
    paginations = ``;
}

function fetchRecipes(){
    $(contentDiv).empty();
    $(loading).show();
    $.ajax({
        type: "GET",
        url: `${targetUrl}&page=${page}&limit=${limit}`,
        success: (resp) => {
            var recipes = resp.data;
            max_page = resp.max_page;
            
                        
            if(recipes.length == 0){
                Swal.fire(
                    'No result',
                    "Sorry, we can't find what you want",
                    'error'
                )
                return;
            }
            updatePagination();
            $(contentDiv).empty();
            for(var j=0; j<recipes.length; j++){
                var imgSource = recipes[j].image != null ? recipes[j].image : "{%static 'img/placeholder-food.webp' %}";
                var newHtml = `<div class="col-3 text-center">
                                <div class="img-cover">
                                    <img src="${imgSource}"
                                    alt="Food image" class="mx-auto img-link img-poster" width="225" height="275" style="object-fit: cover;" data-url="${recipeUrl}${recipes[j].id}">
                                </div>
                                <div>
                                    <i class="bi bi-star-fill" style="font-size: 1.5rem; color: rgb(250, 226, 5);"></i>
                                    <i class="bi bi-star-fill" style="font-size: 1.5rem; color: rgb(250, 226, 5);"></i>
                                    <i class="bi bi-star-fill" style="font-size: 1.5rem; color: rgb(250, 226, 5);"></i>
                                    <i class="bi bi-star-fill" style="font-size: 1.5rem; color: rgb(250, 226, 5);"></i>
                                    <i class="bi bi-star-fill" style="font-size: 1.5rem; color: rgb(250, 226, 5);"></i>
                                </div>
                                <div class="link-wrapper">
                                    <h4 class="text-center mt-2">
                                        <a href="${recipeUrl}${recipes[j].id}" style="text-decoration: none;">${recipes[j].name}</a>
                                    </h4>
                                </div>
                            </div>`;
                $(contentDiv).append(newHtml);
            }
            $(loading).hide();
            $(recipeDiv).show();
            $(contentDiv).show();
            $('.pagination-text').text(`Page ${page} of ${max_page}`);
        }
    });
}
$(document).on('click', '.page-btn', function(){
    if(page == this.textContent)
        return;

    page = this.textContent;
    fetchRecipes();
    if(page == 1)
        $('.prev-page-btn').disable();
    if(page == max_page)
        $('.next-page-btn').disable();
});
$(document).on('click', '.prev-page-btn', function(){
    if(page == 1)
        return;
    page--;;
    fetchRecipes();
});
$(document).on('click', '.next-page-btn', function(){
    if(page == max_page)
        return;
    page++;
    fetchRecipes();
});
$(document).on('click', '.first-page-btn', function(){
    if(page == 1)
        return;
    page = 1;
    fetchRecipes();
});
$(document).on('click', '.last-page-btn', function(){
    if(page == max_page)
        return;
    page = max_page
    fetchRecipes();
});