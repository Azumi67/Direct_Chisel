**این پروژه صرفا برای آموزش و بالا بردن دانش بوده است و هدف دیگری در ان نمیباشد**

![R (2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/a064577c-9302-4f43-b3bf-3d4f84245a6f)
نام پروژه : تانل مستقیم Chisel - برقراری تانل بین چندین سرور با ایپی 4 و ایپی 6 
---------------------------------------------------------------

![check](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/13de8d36-dcfe-498b-9d99-440049c0cf14)
**امکانات**


- تانل مستقیم بین تک سرور و یا چندین سرور خارج و ایران
- ویرایش ریست تایمر ( ساعت یا دقیقه)
- پشتیبانی از TCP و UDP
- قابلیت تانل بر روی تک پورت و چندین پورت 
- امکان تانل بر روی 5 سرور خارج و یک سرور ایران
- مناسب برای V2ray و Openvpn و Wireguard
- استفاده از ایپی 4 و ایپی 6 و هم چنین پرایوت ایپی
- ریستارت سرویس ها در هر سی دقیقه به همراه kill سرویس ها برای حل مشکلات Max conn
- ساختن keygen به صورت اتوماتیک برای تانل
- قابلیت مشاهده جداگانه تمامی سرویس ها
- امکان حذف تمامی تانل ها و سرویس ها
- مدل ریورس تانل chisel در لینک روبرو : https://github.com/Azumi67/Chisel_multipleServers
------------
![Exclamation-Mark-PNG-Clipart](https://github.com/Azumi67/Direct_Chisel/assets/119934376/d3056b73-0811-491d-8478-e9a6a193347f)**نکته مهم**

- **دقت کنید که برای وصل کردن چند سرور خارج به یک سرور ایران ، باید پورت تانل سرور اول با سرور دوم فرق کند وگرنه اختلال خواهید خورد.**
- **مورد دیگر اینکه، اگر ایپی 4 شما فیلتر است از ایپی 6 یا 6to4 استفاده نمایید.**
- **همیشه اگر اختلالی بر روی واتساپ یا یوتیوب و سایر دارید، از وارپ وایرگارد استفاده نمایید.**
- **دستور kill با ریست تایمر سی دقیقه ای برای حل مشکلات max conn و قطعی ها اضافه شد**
- **میتوانید ریست تایمر را از داخل منو تغییر بدید.**
- **دستور bin bash برای سرور های ایرانی که مشکل اجرا نشدن دستور cron را داشتند، اضافه شد. برای کانفیگ دوباره، نخست uninstall کنید که دستورات cron پیشین پاک شود.**
- بر روی سرور هایتان optimizer را نصب کنید.
- اگر اختلالی داشتید لاگ سرویس هاتون را به صورت کامل برای من بفرستید .
```
cd /etc/systemd/system
ls
نام سرویس را بیابید و به جای servicename قرار بدید
systemctl status servicename
journalctl -u servicename.service
```

---------------------

<div align="right">
  <details>
    <summary><strong>توضیحات</strong></summary>
  

- در این اسکریپت بوسیله تانل Chisel میخواهیم ارتباطی مستقیم را بین یک سرور و یا چندین سرور خارج و ایران، ایجاد کنیم.
- لطفا آموزش نوشتاری را با دقت بخوانید و با آزمون و خطا میتوانید تانل را با موفقیت ایجاد کنید.
- در این تانل پورت پیش فرضی استفاده نشده است
- برای هر سرور خارجی که به سرور ایرانتان میخواهید اضافه کنید؛ باید پورت تانل را متفاوت بذارید.
- خودم تمام روش ها را داخل سرور های مختلف تست کردم و جواب داده . بر روی دبیان 12 و اوبونتو 20 تست شده است.
- اگر از پنل v2ray استفاده میکنید و میخواهید با پرایوت ایپی، تانل را بسازید پس لطفا ایپی پرایوت ها را باز کنید.
- پنل شما در خارج باید نصب شده باشد
- میتوانید ریست تایمر را خودتان به راحتی از طریق اسکریپت به صورت دقیقه یا ساعت ویرایش کنید.
- در آخر هر کانفیگ، ایپی 4 سرور ایران شما با پورت نهایی نمایش داده میشود که با استفاده از آن در کلاینت وایرگارد یا V2ray میتوانید به اینترنت متصل شوید.
  
  </details>
</div>


 ------------------------------------------------------

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/V2ray_loadbalance_multipleServers/assets/119934376/98d8c2bd-c9d2-4ecf-8db9-246b90e1ef0f" alt="Image"> </strong>پیش نیازها</summary>
  
  
------------------------------------ 

- لطفا سرور اپدیت شده باشه.
- ایپی 4 و 6 را فوروارد کنید و DNS های خود را نتظیم کنید. همه اینکار ها با optimizer انجام میشود.
- میتوانید از اسکریپت اقای [Hwashemi](https://github.com/hawshemi/Linux-Optimizer) و یا [OPIRAN](https://github.com/opiran-club/VPS-Optimizer) هم برای بهینه سازی سرور در صورت تمایل استفاده نمایید.
  </details>
</div>

----------------------------
  <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/FRP_Reverse_Loadbalance/assets/119934376/ae5b07b8-4d5e-4302-a31f-dec2a79a76b5" alt="Image"> ویدیوهای آموزشی</strong></summary>
    
------------------------------------   

- **ویدیوی آموزشی توسط 69** 
<div align="right">
  <a href="https://www.youtube.com/watch?v=a3yGtZtBv6o">
    <img src="https://img.youtube.com/vi/a3yGtZtBv6o/0.jpg" alt="Video Title" width="300">
  </a>
</div>

  </details>
</div>

---------------
  
  ![6348248](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/398f8b07-65be-472e-9821-631f7b70f783)
**آموزش**
-

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong> تانل مستقیم - ایپی 4 - TCP - تک سرور</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : Chisel TCP [IPV4] >> KHAREJ**


 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/81e681bf-36c6-4963-86e7-d407bd00fa2c" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- کانفیگ سرور را با ایپی 4 و بر روی تک سرور میخواهیم انجام دهیم
- ایپی 4 سرور خارج را وارد میکنم.
- پورت تانل را هم 800 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel TCP [IPV4] >> IRAN**


<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/07892a4b-986f-49fa-8f0f-9669f5e79f48" alt="Image" />
</p>

- میخواهیم سرور ایران را کانفیگ کنیم. کانفیگ تک سرور با ایپی 4 را در سرور خارج، انجام دادیم.
- در سرور خارج، من یک کانفیگ با پورت های 8080 دارم پس تعداد کانفیگ را 1 قرار میدم.اگر تعداد پورت بیشتری دارید ، تعداد بیشتری انتخاب کنید.
- ایپی 4 سرور خارج را وارد میکنم.
- پورت تانل را 800 قرار میدم.
- پورت کانفیگ خارج 8080 بود.
- برای ریست تایمر تعداد کانفیگ خود را وارد نمایید. من یک کانفیگ داشتم پس عدد یک را قرار میدم.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت V2ray استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.
----------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong> تانل مستقیم - ایپی 4 - UDP - تک سرور</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : Chisel UDP [IPV4] << KHAREJ**



 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/8ad6ff25-ed1f-4b01-820f-f1e8a5fff96d" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- کانفیگ سرور را با ایپی 4 و بر روی تک سرور میخواهیم انجام دهیم
- ایپی 4 سرور خارج را وارد میکنم.
- پورت تانل را هم 800 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel UDP [IPV4] << IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/99ca2a83-2073-4754-adbe-14e4f672704f" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنم. کانفیگ تک سرور با ایپی 4 را در سرور خارج، انجام دادیم.
- در سرور خارج، من یک کانفیگ وایرگارد با پورت 50824 دارم پس تعداد کانفیگ را 1 قرار میدهم.اگر تعداد پورت بیشتری دارید ، تعداد بیشتری انتخاب کنید.
- ایپی 4 سرور خارج را وارد میکنم.
- پورت تانل را 800 قرار میدم.
- پورت کانفیگ خارج من 50824 بود.
- برای ریست تایمر تعداد کانفیگ خود را وارد نمایید. من یک کانفیگ داشتم پس عدد یک را قرار میدم.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت وایرگارد استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.
  

----------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong> تانل مستقیم - ایپی 6 - TCP - تک سرور</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : **مسیر : Chisel TCP [IPV6] >> KHAREJ**



 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/c1cbc1b7-f29c-479c-ab3c-e84224b433bb" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- کانفیگ سرور را با ایپی 6 و بر روی تک سرور میخواهیم انجام دهیم
- ایپی 6 سرور خارج را وارد میکنم.
- پورت تانل را هم 443 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel TCP [IPV6] >> IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/d99ed25b-82db-432b-9630-4da684f08dd1" alt="Image" />
</p>


- میخواهیم سرور ایران را کانفیگ کنیم. کانفیگ تک سرور با ایپی 6 را در سرور خارج، انجام دادیم.
- در سرور خارج، من دو کانفیگ با پورت 8080 و 8081 دارم پس تعداد کانفیگ را 2 قرار میدهم.اگر تعداد پورت بیشتری دارید ، تعداد بیشتری انتخاب کنید.
- ایپی 6 سرور خارج را هم وارد میکنم.
- پورت تانل را 443 قرار میدم.
- پورت کانفیگ خارج من 8080 و 8081 بود.
- برای ریست تایمر تعداد کانفیگ خود را وارد نمایید. من دو کانفیگ داشتم پس عدد دو را قرار میدم.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت V2rayNG استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.
----------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong>تانل مستقیم - ایپی 6 - UDP - تک سرور</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج**

**مسیر : **مسیر : Chisel UDP [IPV6] >> KHAREJ**



 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/eba3c692-60df-4f16-adbb-ef22b283e234" alt="Image" />
</p>



- نخست سرور خارج را کانفیگ میکنیم
- کانفیگ سرور را با ایپی 6 و بر روی تک سرور میخواهیم انجام دهیم
- ایپی 6 سرور خارج را وارد میکنم.
- پورت تانل را هم 443 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel UDP [IPV6] >> IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/89977020-145b-4f3f-8521-f1981c089384" alt="Image" />
</p>


- میخواهم سرور ایران را کانفیگ کنم. کانفیگ تک سرور با ایپی 6 را در سرور خارج، انجام دادیم.
- در سرور خارج، من یک کانفیگ وایرگارد با پورت 50824 دارم پس تعداد کانفیگ را 1 قرار میدهم.اگر تعداد پورت بیشتری دارید ، تعداد بیشتری انتخاب کنید.
- ایپی 6 سرور خارج را هم وارد میکنم.
- پورت تانل را 443 قرار میدم.
- پورت کانفیگ خارج من 50824 بود.
- برای ریست تایمر تعداد کانفیگ خود را وارد نمایید. من 1 کانفیگ داشتم پس عدد 1 را قرار میدم.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت وایرگارد استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.
- خب کانفیگ های تک سرور را به پایان رساندیم.
----------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong> تانل مستقیم - ایپی 4 - TCP - پنچ سرور خارج و یک سرور ایران</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج اول**

**مسیر : Chisel TCP [IPV4] [5] Kharej [1] IRAN >> KHAREJ 1**



 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/abea892d-62c4-4398-94e4-5b5c45c4263e" alt="Image" />
</p>


- من 2 سرور خارج و یک سرور ایران دارم و میخواهم از ایپی 4 و TCP استفاده کنم.
- نخست سرور خارج اول را کانفیگ میکنم پس گزینه 1 را انتخاب میکنم تا کانفیگ سرور خارج را آغاز کنم.
- دقت نمایید برای هر سرور خارج که اضافه میکنید باید پورت تانل هم فرق کند.
- ایپی 4 سرور خارج اول را وارد میکنم.
- پورت تانل را هم برای سرور اول 800 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج دوم** 

**مسیر : Chisel TCP [IPV4] [5] Kharej [1] IRAN >> Kharej 2**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/03d73bb6-05c8-4f55-9ceb-163af4f8780e" alt="Image" />
</p>


- سرور دوم خارج را کانفیگ میکنم، پس گرینه دوم را انتخاب میکنم.
-  در این کانفیگ من 2 سرور خارج و 1 سرور ایران داشتم و میخواهم از ایپی 4 و TCP استفاده کنم.
- ایپی 4 سرور خارج دوم را وارد میکنم.
- پورت تانل برای سرور دوم را 801 قرار میدم.


------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel TCP [IPV4] [5] Kharej [1] IRAN >> IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/d96a8d4d-c383-44d4-973e-4d6058638126" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنم، پس گرینه 6 را انتخاب میکنم.
- در این کانفیگ من 2 سرور خارج و 1 سرور ایران داشتم و میخواهم از ایپی 4 و TCP استفاده کنم.
- پورت های کنفیگ های من برای سرور خارج اول 8080 و 8081 و برای سرور خارج دوم ، 8082 و 8083 میباشد
- نخست از ما سوال میشود که برای ریست تایمر چه تعداد سرور و چه تعداد کانفیگ دارم. من 2 عدد سرور خارج و 2 عدد کانفیگ دارم پس این مقادیر را وارد میکنم
- سپس دوباره از ما میپرسد که چه تعداد سرور خارج داریم. این پرسش برای کانفیگ خود سرور میباشد و ربطی به ریست تایمر ندارد.من 2 عدد سرور خارج دارم
- برای سرور اول خارج از من میپرسد که چه تعداد کانفیگ دارم. من 2 عدد کانفیگ با پورت های 8080 و 8081 دارم. پس عدد 2 را وارد میکنم
- سپس ایپی 4 سرور اول خارج را وارد میکنم
- پورت کانفیگ اول 8080 بود پس ان را وارد میکنم
- پورت تانل را 800 قرار داده بودیم. پس ان را وارد میکنم
- پورت کانفیگ دوم 8081 بود. این هم وارد میکنم و پورت تانل هم برای سرور اول 800 بود.
- حالا نوبت کانفیگ سرور دوم میباشد.
- تعداد کانفیگ من در سرور دوم خارج، 2 تا پورت 8082 و 8083 بود. پس عدد 2 را وارد میکنم
- ایپی 4 سرور دوم خارج را وارد میکنم
- پورت کانفیگ اول برای سرور دوم خارج ، 8082 بود پس ان را وارد میکنم . 
- پورت کانفیگ دوم برای سرور دوم خارج ، 8083 بود .
- پورت تانل سرور دوم خارج هم که 801 بود
- خب کار تمام شد. اگر کمی سخت بود دوباره اموزش را بخوانید و ازمون و خطا کنید.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت V2rayng استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.
----------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong> تانل مستقیم - ایپی 6 - TCP - پنچ سرور خارج و یک سرور ایران</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج اول**

**مسیر : Chisel TCP [IPV6] [5] Kharej [1] IRAN >> KHAREJ 1**



 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/d65bdbda-fc00-45b4-8afd-2915a09e74a3" alt="Image" />
</p>


- من 2 سرور خارج و یک سرور ایران دارم و میخواهم از ایپی 6 و TCP استفاده کنم.
- نخست سرور خارج اول را کانفیگ میکنم پس گزینه 1 را انتخاب میکنم تا کانفیگ سرور خارج را آغاز کنم.
- دقت نمایید برای هر سرور خارج که اضافه میکنید باید پورت تانل هم فرق کند.
- ایپی 6 سرور خارج اول را وارد میکنم.
- پورت تانل را هم برای سرور اول خارج 800 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج دوم** 

**مسیر : Chisel TCP [IPV6] [5] Kharej [1] IRAN >> Kharej 2**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/28e2af31-3e3b-44ef-a833-828ff0f4a950" alt="Image" />
</p>


- سرور دوم خارج را کانفیگ میکنم، پس گرینه دوم را انتخاب میکنم.
-  در این کانفیگ من 2 سرور خارج و 1 سرور ایران داشتم و میخواهم از ایپی 6 و TCP استفاده کنم.
- ایپی 6 سرور خارج دوم را وارد میکنم.
- پورت تانل برای سرور دوم را 801 قرار میدم.


------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel TCP [IPV6] [5] Kharej [1] IRAN >> IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/79ecf633-6876-47c5-8cff-40820239f622" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنم، پس گرینه 6 را انتخاب میکنم.
- در این کانفیگ من 2 سرور خارج و 1 سرور ایران داشتم و میخواهم از ایپی 6 و TCP استفاده کنم.
- پورت های کنفیگ های من برای سرور خارج اول 8080  و برای سرور خارج دوم ، 8082  میباشد
- نخست از ما سوال میشود که برای ریست تایمر چه تعداد سرور و چه تعداد کانفیگ دارم. من 2 عدد سرور خارج و 1 عدد کانفیگ دارم پس این مقادیر را وارد میکنم
- سپس دوباره از ما میپرسد که چه تعداد سرور خارج داریم. این پرسش برای کانفیگ خود سرور میباشد و ربطی به ریست تایمر ندارد. من 2 عدد سرور خارج دارم
- برای سرور اول خارج از من میپرسد که چه تعداد کانفیگ دارم. من 1 عدد کانفیگ با پورت های 8080  دارم. پس عدد 1 را وارد میکنم
- سپس ایپی 6 سرور اول خارج را وارد میکنم
- پورت کانفیگ اول 8080 بود پس ان را وارد میکنم
- پورت تانل را 800 قرار داده بودیم. پس ان را وارد میکنم
- حالا نوبت کانفیگ سرور دوم میباشد.
- تعداد کانفیگ من در سرور دوم خارج، 1 پورت 8082 بود. پس عدد 1 را وارد میکنم
- ایپی 6 سرور دوم خارج را وارد میکنم
- پورت کانفیگ اول برای سرور دوم خارج ، 8082 بود پس ان را وارد میکنم . 
- پورت تانل سرور دوم خارج هم که 801 بود
- خب کار تمام شد. اگر کمی سخت بود دوباره اموزش را بخوانید و ازمون و خطا کنید.
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت V2rayng استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.
----------------

  </details>
</div>

 <div align="right">
  <details>
    <summary><strong><img src="https://github.com/Azumi67/Rathole_reverseTunnel/assets/119934376/fcbbdc62-2de5-48aa-bbdd-e323e96a62b5" alt="Image"> </strong> تانل مستقیم - ایپی 6 - UDP - پنچ سرور خارج و یک سرور ایران</summary>
  
  
------------------------------------ 


![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور خارج اول**

**مسیر : Chisel UDP [IPV6] [5] Kharej [1] IRAN >> KHAREJ 1**



 <p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/7ec30395-63bd-4629-8641-25c2f61252a7" alt="Image" />
</p>


- من 1 سرور خارج و یک سرور ایران دارم و میخواهم از ایپی 6 و UDP استفاده کنم.
- نخست سرور خارج را کانفیگ میکنیم پس گزینه 1 را انتخاب میکنم تا کانفیگ سرور خارج را آغاز کنم. 
- ایپی 6 سرور خارج را وارد میکنم.
- پورت تانل را هم 800 قرار میدهم.
----------------------

![green-dot-clipart-3](https://github.com/Azumi67/6TO4-PrivateIP/assets/119934376/902a2efa-f48f-4048-bc2a-5be12143bef3) **سرور ایران** 

**مسیر : Chisel UDP [IPV6] [5] Kharej [1] IRAN >> IRAN**



<p align="right">
  <img src="https://github.com/Azumi67/Direct_Chisel/assets/119934376/cee51f71-e755-4d97-862a-e3b692e3f7be" alt="Image" />
</p>


- سرور ایران را کانفیگ میکنم، پس گرینه 6 را انتخاب میکنم.
- در این کانفیگ من 1 سرور خارج و 1 سرور ایران داشتم و میخواهم از ایپی 6 و UDP استفاده کنم.
- در سرور خارج ، من یک کانفیگ وایرگارد با پورت 50824 دارم پس تعداد کانفیگ را 1 قرار میدهم.اگر تعداد پورت بیشتری دارید ، تعداد بیشتری انتخاب کنید.
- نخست از ما سوال میشود که برای ریست تایمر چه تعداد سرور و چه تعداد کانفیگ دارم. من 1 عدد سرور خارج و 1 عدد کانفیگ دارم پس این مقادیر را وارد میکنم
- سپس دوباره از ما میپرسد که چه تعداد سرور خارج داریم. این پرسش برای کانفیگ خود سرور میباشد و ربطی به ریست تایمر ندارد. من 1 عدد سرور خارج دارم
- ایپی 6 سرور خارج را وارد میکنم.
- پورت کانفیگ اول 50824 بود پس ان را وارد میکنم
- پورت تانل را 800 قرار داده بودیم. پس ان را وارد میکنم
- در آخر، ایپی سرور ایرانتان با پورت مورد نظر را مشاهده میکنید. از این ادرس میتوانید در کلاینت Wireguard استفاده نمایید.
- ایپی ایران شما به طور مثال در اینجا 91.91.91.91 میباشد.

  </details>
</div>

------------------
**اسکرین شات**

<details>
  <summary align="right">Click to reveal image</summary>
  
  <p align="right">
    <img src="https://github.com/Azumi67/Chisel_multipleServers/assets/119934376/e0198041-a57a-4a15-8a9c-73cd42576391" alt="menu screen" />
  </p>
</details>


------------------------------------------
![scri](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/cbfb72ac-eff1-46df-b5e5-a3930a4a6651)
**اسکریپت های کارآمد :**
- این اسکریپت ها optional میباشد.


 
 Opiran Script
```
apt install curl -y && bash <(curl -s https://raw.githubusercontent.com/opiran-club/VPS-Optimizer/main/optimizer.sh --ipv4)
```

Hawshemi script

```
wget "https://raw.githubusercontent.com/hawshemi/Linux-Optimizer/main/linux-optimizer.sh" -O linux-optimizer.sh && chmod +x linux-optimizer.sh && bash linux-optimizer.sh
```

-----------------------------------------------------
![R (a2)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/716fd45e-635c-4796-b8cf-856024e5b2b2)
**اسکریپت من**
----------------

- اسکریپت اصلی
```
sudo apt-get install python3 -y && apt-get install wget -y && apt-get install python3-pip -y && pip3 install colorama && pip3 install netifaces && apt-get install curl -y && python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/Direct_Chisel/main/chiseld.py --ipv4)
```

- اگر با دستور بالا نتوانستید اسکریپت را اجرا کنید، نخست دستور زیر را اجرا نمایید و سپس دستور اول را دوباره اجرا کنید.
- اگر باز هم colorama رو نگرفت پس از اجرای دستور پایین ، همچنین این دستور هم اجرا کنید : pip3 install colorama , pip3 install netifaces

```
sudo apt-get install python-pip -y  &&  apt-get install python3 -y && alias python=python3 && python -m pip install colorama && python -m pip install netifaces
```

--------------------------------------

- دستور زیر برای کسانی هست که پیش نیاز ها را در سرور، نصب شده دارند
 
```
python3 <(curl -Ls https://raw.githubusercontent.com/Azumi67/Direct_Chisel/main/chiseld.py --ipv4)
```
--------------------------------------

- اگر سرور شما خطای externally-managed-environment داد از دستور زیر اقدام به اجرای اسکریپت نمایید
 
```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Azumi67/Direct_Chisel/main/managed.sh)"	
```

---------------------------------------------
![R (7)](https://github.com/Azumi67/PrivateIP-Tunnel/assets/119934376/42c09cbb-2690-4343-963a-5deca12218c1)
**تلگرام** 
![R (6)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/f81bf6e1-cfed-4e24-b944-236f5c0b15d3) [اپیران- OPIRAN](https://t.me/OPIranClubb)

---------------------------------
![R23 (1)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/18d12405-d354-48ac-9084-fff98d61d91c)
**سورس ها**


![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس  CHISEL](https://github.com/jpillora/chisel)

![R (9)](https://github.com/Azumi67/FRP-V2ray-Loadbalance/assets/119934376/33388f7b-f1ab-4847-9e9b-e8b39d75deaa) [سورس  OPIRAN](https://github.com/opiran-club)

![R (9)](https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/assets/119934376/4758a7da-ab54-4a0a-a5a6-5f895092f527)[سورس  Hwashemi](https://github.com/hawshemi/Linux-Optimizer)



-----------------------------------------------------


