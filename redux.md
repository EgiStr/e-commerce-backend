redux
-> user
-> auth or sesion

        -> detail user
            -> id
            -> profil
            -> username
            -> dll

        -> location
             -> geo point
             -> adress
             -> dll

    -> nofication
        -> unread notif
        -> notif

    -> cart
       -> cartList @parms objects
            -> id
            -> store
            -> title
            -> price
            -> quantity
            -> varian -> fix



<!-- The core Firebase JS SDK is always required and must be listed first -->
<script src="https://www.gstatic.com/firebasejs/8.6.1/firebase-app.js"></script>

<!-- TODO: Add SDKs for Firebase products that you want to use
     https://firebase.google.com/docs/web/setup#available-libraries -->
<script src="https://www.gstatic.com/firebasejs/8.6.1/firebase-analytics.js"></script>

<script>
  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  var firebaseConfig = {
    apiKey: "AIzaSyAoHiKZD-hGj8rfuK4_iWWJK6KV6qNVX5s",
    authDomain: "e-commerce-cd481.firebaseapp.com",
    projectId: "e-commerce-cd481",
    storageBucket: "e-commerce-cd481.appspot.com",
    messagingSenderId: "868424335775",
    appId: "1:868424335775:web:da79c218ad68b83a6f7daa",
    measurementId: "G-R0ZNQV8FVJ"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();
</script>