const menuData = [
    {id:1,name:'Margherita',category:'pizza',price:16.90,description:'San Marzano tomato, fresh mozzarella, basil, extra virgin olive oil.',calories:680,prepTime:'15 min',rating:4.9,image:'images/pizza.jpg'},
    {id:2,name:'Diavola',category:'pizza',price:19.90,description:'Spicy salami, San Marzano tomato, mozzarella, chili flakes.',calories:720,prepTime:'18 min',rating:4.8,image:'images/pizza.jpg'},
    {id:3,name:'Quattro Stagioni',category:'pizza',price:21.90,description:'Artichokes, ham, mushrooms, olives, tomato, mozzarella.',calories:750,prepTime:'20 min',rating:4.7,image:'images/pizza.jpg'},
    {id:4,name:'Classic Burger',category:'burgers',price:18.90,description:'Angus beef, cheddar, lettuce, tomato, caramelized onions, brioche bun.',calories:820,prepTime:'12 min',rating:4.8,image:'images/burger.jpg'},
    {id:5,name:'Truffle Burger',category:'burgers',price:24.90,description:'Wagyu beef, truffle aioli, provolone, arugula, truffle butter brioche.',calories:890,prepTime:'15 min',rating:4.9,image:'images/burger.jpg'},
    {id:6,name:'Fettuccine Alfredo',category:'pasta',price:20.90,description:'House-made fettuccine, parmesan cream sauce, fresh parsley.',calories:780,prepTime:'15 min',rating:4.7,image:'images/pasta.jpg'},
    {id:7,name:'Truffle Mushroom Pasta',category:'pasta',price:26.90,description:'Tagliatelle, wild mushrooms, black truffle, parmesan, garlic oil.',calories:710,prepTime:'18 min',rating:4.9,image:'images/pasta.jpg'},
    {id:8,name:'BBQ Ribs',category:'bbq',price:32.90,description:'Slow-cooked pork ribs, house BBQ sauce, crispy onions, cornbread.',calories:1100,prepTime:'25 min',rating:4.8,image:'images/bbq.jpg'},
    {id:9,name:'Grilled Salmon',category:'seafood',price:30.90,description:'Atlantic salmon, garlic butter, asparagus, lemon herb couscous.',calories:620,prepTime:'20 min',rating:4.8,image:'images/seafood.jpg'},
    {id:10,name:'Tiramisu',category:'desserts',price:9.90,description:'Classic Italian tiramisu, mascarpone, espresso, cocoa powder.',calories:380,prepTime:'5 min',rating:4.9,image:'images/dessert.jpg'},
    {id:11,name:'Italian Soda',category:'drinks',price:4.90,description:'Sparkling water, house-made syrup, fresh mint, lemon.',calories:120,prepTime:'3 min',rating:4.5,image:'images/drink.jpg'},
    {id:12,name:'Espresso Martini',category:'drinks',price:14.90,description:'Vodka, fresh espresso, coffee liqueur, coffee beans.',calories:220,prepTime:'5 min',rating:4.7,image:'images/drink.jpg'}
];
let cart = JSON.parse(localStorage.getItem('bellaVitaCart')) || [];
let currentCategory = 'all';
let searchQuery = '';
const menuGrid = document.getElementById('menuGrid');
const featuredGrid = document.getElementById('featuredGrid');
const cartSidebar = document.getElementById('cartSidebar');
const cartOverlay = document.getElementById('cartOverlay');
const cartItems = document.getElementById('cartItems');
const cartCount = document.getElementById('cartCount');
const cartSubtotal = document.getElementById('cartSubtotal');
const cartDelivery = document.getElementById('cartDelivery');
const cartTax = document.getElementById('cartTax');
const cartTotal = document.getElementById('cartTotal');
const cartCheckout = document.getElementById('cartCheckout');
const menuSearch = document.getElementById('menuSearch');
const clearSearch = document.getElementById('clearSearch');
const loader = document.getElementById('loader');
window.addEventListener('load',()=>{loader.classList.add('hidden')});
function renderMenu(){const filtered=menuData.filter(item=>{const matchesCategory=currentCategory==='all'||item.category===currentCategory;const matchesSearch=item.name.toLowerCase().includes(searchQuery.toLowerCase())||item.description.toLowerCase().includes(searchQuery.toLowerCase());return matchesCategory&&matchesSearch});if(filtered.length===0){menuGrid.innerHTML='<p style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-600);font-size:1.1rem;">No dishes found. Try adjusting your search.</p>';return}menuGrid.innerHTML=filtered.map(item=>`<div class="menu-card" data-id="${item.id}"><img src="${item.image}" alt="${item.name}" class="card-image" loading="lazy" /><div class="card-body"><div class="card-header"><h4>${item.name}</h4><span class="price">$${item.price.toFixed(2)}</span></div><p class="card-desc">${item.description}</p><div class="card-meta"><span>⭐ ${item.rating}</span><span>🔥 ${item.calories} cal</span><span>⏱ ${item.prepTime}</span></div><button class="add-btn" data-id="${item.id}">${isInCart(item.id)?'✓ In Cart':'Add to Cart'}</button></div></div>`).join('');document.querySelectorAll('.add-btn').forEach(btn=>{btn.addEventListener('click',(e)=>{const id=parseInt(e.target.dataset.id);toggleCartItem(id)})})}
function renderFeatured(){const featured=menuData.slice(0,4);featuredGrid.innerHTML=featured.map(item=>`<div class="featured-card" data-id="${item.id}"><img src="${item.image}" alt="${item.name}" loading="lazy" /><div class="card-body"><h4>${item.name}</h4><span class="price">$${item.price.toFixed(2)}</span></div></div>`).join('');featuredGrid.querySelectorAll('.featured-card').forEach(card=>{card.addEventListener('click',()=>{const id=parseInt(card.dataset.id);const item=menuData.find(i=>i.id===id);if(item){currentCategory=item.category;searchQuery='';menuSearch.value='';clearSearch.classList.remove('visible');document.querySelectorAll('.category-btn').forEach(b=>{b.classList.toggle('active',b.dataset.category===currentCategory);b.setAttribute('aria-selected',b.dataset.category===currentCategory)});renderMenu();document.getElementById('menu').scrollIntoView({behavior:'smooth'})}})})}
document.querySelectorAll('.category-btn').forEach(btn=>{btn.addEventListener('click',()=>{document.querySelectorAll('.category-btn').forEach(b=>{b.classList.remove('active');b.setAttribute('aria-selected','false')});btn.classList.add('active');btn.setAttribute('aria-selected','true');currentCategory=btn.dataset.category;renderMenu()})});
menuSearch.addEventListener('input',(e)=>{searchQuery=e.target.value;clearSearch.classList.toggle('visible',searchQuery.length>0);renderMenu()});
clearSearch.addEventListener('click',()=>{menuSearch.value='';searchQuery='';clearSearch.classList.remove('visible');renderMenu()});
function isInCart(id){return cart.some(item=>item.id===id)}
function toggleCartItem(id){const index=cart.findIndex(item=>item.id===id);if(index>-1){cart.splice(index,1)}else{const item=menuData.find(i=>i.id===id);if(item){cart.push({...item,quantity:1})}}saveCart();renderCart();renderMenu()}
function updateQuantity(id,delta){const item=cart.find(i=>i.id===id);if(!item)return;item.quantity+=delta;if(item.quantity<=0){cart=cart.filter(i=>i.id!==id)}saveCart();renderCart();renderMenu()}
function removeItem(id){cart=cart.filter(i=>i.id!==id);saveCart();renderCart();renderMenu()}
function saveCart(){localStorage.setItem('bellaVitaCart',JSON.stringify(cart))}
function renderCart(){const count=cart.reduce((sum,i)=>sum+i.quantity,0);cartCount.textContent=count;cartCount.style.display=count>0?'flex':'none';const subtotal=cart.reduce((sum,i)=>sum+i.price*i.quantity,0);const delivery=subtotal>30||cart.length===0?0:5.99;const tax=subtotal*0.085;const total=subtotal+delivery+tax;cartSubtotal.textContent=`$${subtotal.toFixed(2)}`;cartDelivery.textContent=`$${delivery.toFixed(2)}`;cartTax.textContent=`$${tax.toFixed(2)}`;cartTotal.textContent=`$${total.toFixed(2)}`;if(cart.length===0){cartItems.innerHTML='<p class="cart-empty">Your cart is empty.</p>';cartCheckout.disabled=true;cartCheckout.style.opacity='0.5';return}cartCheckout.disabled=false;cartCheckout.style.opacity='1';cartItems.innerHTML=cart.map(item=>`<div class="cart-item"><img src="${item.image}" alt="${item.name}" loading="lazy" /><div class="cart-item-info"><h5>${item.name}</h5><span class="price">$${item.price.toFixed(2)}</span></div><div class="cart-item-actions"><button class="qty-btn" data-id="${item.id}" data-delta="-1">−</button><span class="qty">${item.quantity}</span><button class="qty-btn" data-id="${item.id}" data-delta="1">+</button><button class="cart-item-remove" data-id="${item.id}">✕</button></div></div>`).join('');cartItems.querySelectorAll('.qty-btn').forEach(btn=>{btn.addEventListener('click',()=>{const id=parseInt(btn.dataset.id);const delta=parseInt(btn.dataset.delta);updateQuantity(id,delta)})});cartItems.querySelectorAll('.cart-item-remove').forEach(btn=>{btn.addEventListener('click',()=>{removeItem(parseInt(btn.dataset.id))})})}
function openCart(){cartSidebar.classList.add('open');cartOverlay.classList.add('visible');document.body.style.overflow='hidden'}
function closeCart(){cartSidebar.classList.remove('open');cartOverlay.classList.remove('visible');document.body.style.overflow=''}
document.getElementById('cartToggle').addEventListener('click',openCart);
document.getElementById('cartClose').addEventListener('click',closeCart);
cartOverlay.addEventListener('click',closeCart);
const hamburger=document.getElementById('hamburger');const navLinks=document.getElementById('navLinks');hamburger.addEventListener('click',()=>{const isOpen=navLinks.classList.toggle('open');hamburger.classList.toggle('active');hamburger.setAttribute('aria-expanded',isOpen)});
cartCheckout.addEventListener('click',()=>{if(cart.length===0)return;window.location.href='checkout.html'});
document.getElementById('newsletterForm')?.addEventListener('submit',(e)=>{e.preventDefault();const input=e.target.querySelector('input');if(input.value){alert('Thank you for subscribing! You will receive exclusive offers.');input.value=''}});
renderMenu();renderFeatured();renderCart();
