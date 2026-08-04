const orderData = JSON.parse(localStorage.getItem('bellaVitaOrder'));
if(!orderData){window.location.href='index.html'}
document.getElementById('orderNumber').textContent=orderData.orderNumber;
document.getElementById('confName').textContent=orderData.customer.name;
document.getElementById('confType').textContent=orderData.customer.customerType==='existing'?'Existing Customer':'New Customer';
document.getElementById('confPhone').textContent=orderData.customer.phone;
document.getElementById('confAddress').textContent=`${orderData.customer.address}, ${orderData.customer.city}, ${orderData.customer.postalCode}`;
const confItems=document.getElementById('confItems');confItems.innerHTML=orderData.items.map(item=>`<div class="checkout-item" style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #e8e4dc;font-size:0.95rem;"><span>${item.name} <span style="color:var(--gray-600);font-weight:500;">×${item.quantity}</span></span><span>$${(item.price*item.quantity).toFixed(2)}</span></div>`).join('');
document.getElementById('confSubtotal').textContent=`$${orderData.subtotal.toFixed(2)}`;
document.getElementById('confDelivery').textContent=`$${orderData.deliveryFee.toFixed(2)}`;
document.getElementById('confTax').textContent=`$${orderData.tax.toFixed(2)}`;
document.getElementById('confTotal').textContent=`$${orderData.total.toFixed(2)}`;
document.getElementById('confETA').textContent=orderData.estimatedTime;
document.getElementById('confPayment').textContent=orderData.customer.paymentMethod.split(' ').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');
const loader=document.getElementById('loader');window.addEventListener('load',()=>{loader.classList.add('hidden')});
const steps=document.querySelectorAll('.progress-step');let currentStep=0;function animateProgress(){if(currentStep<steps.length){steps[currentStep].classList.add('active');currentStep++;setTimeout(animateProgress,800)}}setTimeout(animateProgress,600);
document.querySelector('.confirmation-actions .btn-secondary')?.addEventListener('click',()=>{localStorage.removeItem('bellaVitaOrder')});
document.querySelector('.confirmation-actions .btn-primary')?.addEventListener('click',()=>{localStorage.removeItem('bellaVitaOrder')});
