

function ibg() {
   $.each($('.ibg'), function (index, val) {
      if ($(this).find('img').length > 0) {
         $(this).css('background-image', 'url("' + $(this).find('img').attr('src') + '")');
      }
   });
}
ibg();

const headerLinks = document.querySelectorAll('[data-elem="menu"]');

headerLinks.forEach((link) => link.addEventListener('click', function() {
   headerLinks.forEach((link) => link.classList.remove('active'));
   link.classList.add('active');
}));

const liveDrop = document.querySelector('.live-drop__section');
const liveDrops = liveDrop.children;

for (const item of liveDrops) {
   item.addEventListener('click', function() {
      for (const item of liveDrops) {
         item.classList.remove('active')
      }
      item.classList.add('active')
   })
}
//SLIDERS
if($('.slider__body').length>0){
   $('.slider__body').slick({
      //autoplay: true,
      //infinite: false,
      dots: true,
      arrows: false,
      accessibility:false,
      slidesToShow:1,
      autoplaySpeed: 3000,
      nextArrow:'<button type="button" class="slick-next"></button>',
      prevArrow:'<button type="button" class="slick-prev"></button>',
      responsive: [{
         breakpoint: 768,
         settings: {}
      }]
   });
}