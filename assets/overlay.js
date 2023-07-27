document.querySelector('body').innerHTML += `
<i class="fas fa-bars links-btn"></i>

<div class="links-overlay">

        <a href="/">الرئيسية</a>
        <a href="/add-student">اضافة طالب</a>
        <a href="/exam">الاختبارات</a>
        <a href="/collect-marks">تجميع درجات</a>
        <a href="/change-password">تغير كلمة المرور</a>

</div>
`

var layerBtn = document.querySelector('.links-btn'); 
var layer = document.querySelector('.links-overlay');


layerBtn.addEventListener('click',function(){

    if (layer.className == 'links-overlay') {
        layer.classList.add('view')
        layerBtn.className = 'fas fa-xmark links-btn'
    }else{
        layer.classList.remove('view')
        layerBtn.className = 'fas fa-bars links-btn' ;
    }

    
})