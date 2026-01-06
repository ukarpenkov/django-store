from django.http import HttpResponse

# Create your views here.

def home(_request):
    return HttpResponse(
        """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>С Новым 2025 Годом!</title>
</head>
<body style="margin:0;padding:0;font-family:'Arial',sans-serif;background-color:#0a2e36;color:#fff;background-image:radial-gradient(#0d3b47 15%,transparent 16%),radial-gradient(#0d3b47 15%,transparent 16%);background-size:40px 40px;background-position:0 0,20px 20px;">
<div style="max-width:800px;margin:0 auto;padding:20px;text-align:center;">
<header style="padding:30px 0;">
<h1 style="font-size:3.5em;margin-bottom:10px;color:#ffde59;text-shadow:3px 3px 0 #d35400,6px 6px 10px rgba(0,0,0,0.5);letter-spacing:2px;">🎄 С Новым Годом! 🎅</h1>
<p style="font-size:1.5em;color:#a3d9ff;font-style:italic;">Пусть 2025 год принесет счастье, здоровье и удачу!</p>
</header>
<main style="background-color:rgba(13,59,71,0.8);border-radius:15px;padding:30px;box-shadow:0 10px 30px rgba(0,0,0,0.5);margin-bottom:30px;border:2px solid #ffde59;">
<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:20px;margin-bottom:30px;">
<div style="flex:1;min-width:250px;background:#1a5d6e;padding:20px;border-radius:10px;">
<h3 style="color:#ffde59;font-size:1.8em;">🎁 Новогодние традиции</h3>
<p>Украшение елки, бой курантов, поздравление близких, загадывание желаний под бой курантов.</p>
</div>
<div style="flex:1;min-width:250px;background:#1a5d6e;padding:20px;border-radius:10px;">
<h3 style="color:#ffde59;font-size:1.8em;">⏳ Обратный отсчет</h3>
<div id="countdown" style="font-size:2em;font-weight:bold;color:#ffde59;padding:10px;">Загрузка...</div>
<p>до Нового 2025 года!</p>
</div>
</div>
<div style="margin:30px 0;">
<h2 style="color:#ffde59;border-bottom:2px dashed #ffde59;display:inline-block;padding-bottom:5px;">Новогоднее пожелание</h2>
<p style="font-size:1.3em;line-height:1.6;background-color:rgba(255,222,89,0.1);padding:20px;border-radius:10px;border-left:5px solid #ffde59;">Пусть новый год станет страницей новой книги, которую вы напишете сами. Пусть на каждой странице будут только радостные события, приятные встречи и осуществленные мечты. Желаем здоровья, счастья и благополучия вам и вашим близким!</p>
</div>
<div style="display:flex;justify-content:center;flex-wrap:wrap;gap:15px;font-size:3em;margin:30px 0;">
<span>🎄</span><span>🎅</span><span>🤶</span><span>🎁</span><span>🌟</span><span>❄️</span><span>🔥</span>
</div>
</main>
<footer style="padding:20px;border-top:1px solid #1a5d6e;color:#a3d9ff;">
<p>© 2024 Новогодняя открытка. Все права на праздник защищены! 🎉</p>
<p style="margin-top:10px;font-size:0.9em;">С наилучшими пожеланиями в наступающем году!</p>
</footer>
</div>
<script>function updateCountdown(){const e=new Date,t=e.getFullYear(),a=t+1,n=new Date(`January 1, ${a} 00:00:00`),o=n-e,d=Math.floor(o/(1e3*60*60*24)),r=Math.floor(o%(1e3*60*60*24)/(1e3*60*60)),i=Math.floor(o%(1e3*60*60)/(1e3*60)),s=Math.floor(o%(1e3*60)/1e3);document.getElementById("countdown").innerHTML=`${d} д. ${r} ч. ${i} м. ${s} с.`}setInterval(updateCountdown,1e3),updateCountdown();</script>
</body>
</html>
        """,
        content_type="text/html; charset=utf-8"
    )
