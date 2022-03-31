$(document).ready(function() {

const imageBg = new IntersectionObserver((entries, imgObserver) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const lazyBackground = entry.target;
      lazyBackground.style.backgroundImage = `url(${lazyBackground.dataset.image})`;
      lazyBackground.classList.remove('lzy_bg');
      imgObserver.unobserve(lazyBackground);
    }
  });
});
const arrBg = document.querySelectorAll('.lzy_bg');
arrBg.forEach((v) => {
  imageBg.observe(v);
});

// Скролл по клику
function currentYPosition() {
  // Firefox, Chrome, Opera, Safari
  if (self.pageYOffset) return self.pageYOffset;
  // Internet Explorer 6 - standards mode
  if (document.documentElement && document.documentElement.scrollTop)
    return document.documentElement.scrollTop;
  // Internet Explorer 6, 7 and 8init_pointer
  if (document.body.scrollTop) return document.body.scrollTop;
  return 0;
}

function elmYPosition(eID) {
  let elm = document.querySelector(eID);
  let y = elm.offsetTop;
  let node = elm;
  while (node.offsetParent && node.offsetParent != document.body) {
    node = node.offsetParent;
    y += node.offsetTop;
  }
  return y;
}

function smoothScroll(eID) {
  let startY = currentYPosition();
  let stopY = elmYPosition(eID) - 50;
  let distance = stopY > startY ? stopY - startY : startY - stopY;
  if (distance < 100) {
    scrollTo(0, stopY);
    return;
  }
  let speed = Math.round(distance / 100);
  if (speed >= 20) speed = 20;
  let step = Math.round(distance / 30);
  let leapY = stopY > startY ? startY + step : startY - step;
  let timer = 0;
  if (stopY > startY) {
    for (let i = startY; i < stopY; i += step) {
      setTimeout('window.scrollTo(0, ' + leapY + ')', timer * speed);
      leapY += step;
      if (leapY > stopY) leapY = stopY;
      timer++;
    }
    return;
  }
  for (let i = startY; i > stopY; i -= step) {
    setTimeout('window.scrollTo(0, ' + leapY + ')', timer * speed);
    leapY -= step;
    if (leapY < stopY) leapY = stopY;
    timer++;
  }
}
document.querySelectorAll('.scroll_to').forEach((anchor) => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    smoothScroll(this.getAttribute('href'));
  });
});

//
// Lazy load img

const imageBlockObserver = new IntersectionObserver((entries, imgObserver) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const lazyBlock = entry.target;
      const lazyImage = lazyBlock.querySelectorAll('.lzy_img_new');
      lazyImage.forEach((elem) => {
        elem.src = elem.dataset.src;
        elem.classList.remove('lzy_img_new');
      });
      lazyBlock.classList.remove('lzy_img_bl');
      imgObserver.unobserve(lazyBlock);
    }
  });
});
const arrBlockImg = document.querySelectorAll('.lzy_img_bl');
arrBlockImg.forEach((v) => {
  imageBlockObserver.observe(v);
});

const btnBurger = document.querySelectorAll('.menu__burger');
const overlayMenu = document.querySelector('.menu');
const menuLimk = document.querySelectorAll('.nav__item a');

btnBurger.forEach((elem) => {
  elem.onclick = () => {
    document.querySelector('body').classList.toggle('locked');
    overlayMenu.classList.add('open_menu');
    overlayMenu.classList.remove('close__burger');
  };
});
document.querySelectorAll('.menu__close').forEach((elem) => {
  elem.onclick = function (e) {
    overlayMenu.classList.remove('open_menu');
    overlayMenu.classList.add('close__burger');
  };
});
const hasChild = document.querySelectorAll('.menu .menu-item-has-children>a');
const childList = document.querySelectorAll('.menu .sub-menu');

hasChild.forEach((elem, index) => {
  const hasChildBtn = document.createElement('span');
  hasChildBtn.classList.add('open_child_menu');
  elem.append(hasChildBtn);
  hasChildBtn.onclick = (e) => {
    e.preventDefault();
    childList[index].classList.add('active');
  };
});

childList.forEach((elem, index) => {
  const hasChildBtnBack = document.createElement('span');
  hasChildBtnBack.classList.add('close_child_menu');
  elem.append(hasChildBtnBack);
  hasChildBtnBack.onclick = (e) => {
    e.preventDefault();
    elem.classList.remove('active');
  };
});

const headerFixed = document.querySelector('.header');
// const arrowFixed = document.querySelector(".scroll_to_top");
const mainHeadSection = document.querySelector('.head_section_main ');
window.addEventListener('scroll', function () {
  pageYOffset > 200
    ? headerFixed.classList.add('fixed_header')
    : headerFixed.classList.remove('fixed_header');
  // pageYOffset > 750
  //   ? arrowFixed.classList.add("visible_arrow")
  //   : arrowFixed.classList.remove("visible_arrow");
});
if (window.pageYOffset > 450) headerFixed.classList.add('fixed_header');

// if (window.pageYOffset > 450) arrowFixed.classList.add("visible_arrow");

const slideDownPure = (el) => {
  el.style.height = `${el.scrollHeight}px`;
  el.style.opacity = '1';
  el.style.overflow = 'visible';
};

const slideUpPure = (el) => {
  el.style.height = '0';
  el.style.opacity = '0';
  el.style.overflow = 'hidden';
  el.style.marginBottom = '0';
};

function tabs(secondsTransition) {
  const buttons = document.querySelectorAll('[data-tab="button"]');
  const contents = document.querySelectorAll('[data-tab="content"]');

  contents.forEach((content) => {
    content.style.opacity = '0';
    content.style.height = '0';
    content.style.overflow = 'hidden';
    content.style.transition = `all ${secondsTransition}s ease`;
  });

  buttons.forEach((button, index) => {
    if (button.classList.contains('active')) {
      slideDownPure(contents[index]);
    }

    button.onclick = () => {
      if (!button.classList.contains('active')) {
        contents.forEach((content) => slideUpPure(content));
        buttons.forEach((button) => button.classList.remove('active'));
        button.classList.add('active');
        slideDownPure(contents[index]);
      }
    };
  });
}
tabs(0.5)
const userBtn = document.querySelector('.contact__icon_user')
const userPopup = document.querySelector('.user__popup')
if (userBtn) {
  userBtn.onclick = (el) => {
    if(el.target.classList.contains('active'))
    {
      el.target.classList.remove('active')
      userPopup.classList.remove('open')
    } else {
      userPopup.classList.add('open')
      el.target.classList.add('active')
    }
  }
}

// Sidebar 
const openSidebar = document.querySelector('.contact__icon_profile')
const closeSidebar = document.querySelector('.close__sidebar')
const sidebarBg = document.querySelector('.sidebar__bg')
const sidebar = document.querySelector('.personal__sidebar')
if (openSidebar) {
  openSidebar.onclick = () => {
    sidebar.classList.add('open')
    sidebarBg.classList.add('open')
  }
}
if (closeSidebar) {
  closeSidebar.onclick = () => {
    removeOpen()
  }
}
if (sidebarBg) {
  sidebarBg.onclick = () => {
    removeOpen()
  }  
}
function removeOpen() {
  sidebar.classList.remove('open')    
  sidebarBg.classList.remove('open')
}


const reviewSlider = new Swiper('.review__slider', {
  slidesPerView: 2,
  spaceBetween: 37,
  centeredSlides: true,
  loop: true,
  navigation: {
    prevEl: '.swiper__arrow_left',
    nextEl: '.swiper__arrow_right',
  },
  breakpoints: {
    300: {
      slidesPerView: 1.1,
  spaceBetween: 20,
    },
    576: {
      slidesPerView: 1.5,
      spaceBetween: 25,
    },
    768: {
      slidesPerView: 2,
  spaceBetween: 30,
    },
    1024: {
      slidesPerView: 2,
  spaceBetween: 37,
    },
  },
});

//////////////////////////
// Open lang
//////////////////////////

const formWrap = document.querySelectorAll('.input__group');
formWrap.forEach((elem) => {
  let formInput = elem.querySelector('.order__input');
  let formLabel = elem.querySelector('.place_span');
  if (formInput) {
    formInput.onfocus = () => {
      formLabel.classList.add('fixed_span');
    };
    formInput.onfocusout = (e) => {
      if (e.target.value === '') {
        formLabel.classList.remove('fixed_span');
      }
    };
  }
});
const checkWrap = document.querySelectorAll('.wpcf7-acceptance');
checkWrap.forEach((elem) => {
  let checkBox = elem.querySelector('.check_input');
  if (checkBox.checked) {
    elem.classList.add('checked_inp');
  }
  checkBox.onchange = (el) => {
    elem.classList.toggle('checked_inp');
  };
});

const scrollOut = ScrollOut({
  targets: '.xyz_start',
  onShown: (el, ctx, scrollingElement) => {
  console.log(scrollingElement);
    el.classList.add('xyz-in');
  },
});
console.log(ScrollOut);
const filterBtn = document.querySelector('.filter_btn');
const filterClose = document.querySelector('.close_filter');
const filterWrap = document.querySelector('.catalog_filter');
if (filterBtn) {
  filterBtn.onclick = () => {
    filterWrap.classList.toggle('open');
  };
  filterClose.onclick = () => {
    filterWrap.classList.toggle('open');
  };
}

const popupForm = document.querySelector('.consult_popup');
const openForm = document.querySelectorAll('.open__form');

const consultReview = document.querySelector('.consult_review');
const reviewBtn = document.querySelectorAll('.review__btn');

if (popupForm) {
  popupForm.onclick = (e) => {
    if (
      e.target.classList.contains('popup') ||
      e.target.classList.contains('close_popup')
    ) {
      popupForm.classList.remove('open');
    }
  };
  openForm.forEach((elem) => {
    elem.onclick = (e) => {
     
      popupForm.classList.add('open');
    };
  });
}
if (consultReview) {
  consultReview.onclick = (e) => {
    if (
      e.target.classList.contains('popup') ||
      e.target.classList.contains('close_popup')
    ) {
      consultReview.classList.remove('open');
    }
  };
  reviewBtn.forEach((elem) => {
    elem.onclick = (e) => {      
      consultReview.classList.add('open');
    };
  });
}


const selectGroup = document.querySelectorAll('.input__group_select');
selectGroup.forEach((elem, ind) => {
  const selectInput = elem.querySelector('.select__input');
  const orderSelect = elem.querySelector('.order__select');
  const selectSpan = elem.querySelector('.select_span');
  const selectBtn = elem.querySelectorAll('.order__select button');

  selectInput.onfocus = () => {
    selectSpan.classList.add('fixed_span');
    orderSelect.classList.add('show');
  };
  selectBtn.forEach((elem) => {
    elem.onclick = (e) => {
      e.preventDefault();
      selectInput.value = e.target.innerHTML.trim();
      orderSelect.classList.remove('show');
    };
  });
  window.addEventListener('click', function (e) {
    if (!e.target.classList.contains('select__input')) {
      orderSelect.classList.remove('show');
      selectSpan.classList.remove('fixed_span');
      if (selectInput.value === '') {
        selectSpan.classList.remove('fixed_span');
      } else {
        selectSpan.classList.add('fixed_span');
      }
    }
  });
});

const typeItem = document.querySelectorAll('.type__item')
const wrapType = document.querySelectorAll('.radio__wrap_type');
const inputType = document.querySelectorAll('.input__type');

const wrapLonge = document.querySelectorAll('.radio__wrap_long');
const longInput = document.querySelectorAll('.long__input');
const longMin = document.querySelector('.long__input[value="month"]');
const longMax = document.querySelector('.long__input[value="year"]');

const wrapPay = document.querySelectorAll('.radio__wrap_pay');
const typePay = document.querySelectorAll('.type__pay');

inputType.forEach((el, idx) => {
  if (el.checked) {
    wrapType[idx].classList.add('radio__wrap_checked');
    checkElem(el);
    el.closest('.type__item').classList.add('type_check')
    
  }else{
    el.closest('.type__item').classList.remove('type_check')
  }
  radioChange(el, wrapType, idx);
});

function radioChange(radioInput, wrapInput, ind) {
  radioInput.onchange = () => {
    if (radioInput.checked) {
      if (radioInput.classList.contains('input__type')) {
        checkElem(radioInput);
        typeItem.forEach(el => {
          el.classList.remove('type_check')
        })
        radioInput.closest('.type__item').classList.add('type_check')
      }
      if (radioInput.classList.contains('long__input')) {
        resultVal();
      }
      if (radioInput.classList.contains('type__pay')) {
        if (radioInput.value === 'card') {
          document.querySelector('.form__wrap_card').style.display = 'flex';
          document.querySelector('.form__wrap_other').style.display = 'none';
        } else {
          document.querySelector('.form__wrap_other').style.display = 'block';
          document.querySelector('.form__wrap_card').style.display = 'none';
        }
      }
      wrapInput.forEach((item) => {
        item.classList.remove('radio__wrap_checked');
      });
      wrapInput[ind].classList.add('radio__wrap_checked');
    }
  };
}

longInput.forEach((el, idx) => {
  if (el.checked) {
    wrapLonge[idx].classList.add('radio__wrap_checked');
  }
  radioChange(el, wrapLonge, idx);
});

typePay.forEach((el, idx) => {
  if (el.checked) {
    wrapPay[idx].classList.add('radio__wrap_checked');
    if (el.value === 'card') {
      document.querySelector('.form__wrap_card').style.display = 'flex';
      document.querySelector('.form__wrap_other').style.display = 'none';
    } else {
      document.querySelector('.form__wrap_other').style.display = 'block';
      document.querySelector('.form__wrap_card').style.display = 'none';
    }
  }
  radioChange(el, wrapPay, idx);
});

function checkElem(element) {
  $(longMin).attr('data-value', element.dataset.min);
  $(longMax).attr('data-value', element.dataset.max);
  resultVal();
}

function resultVal() {
  if (longMin.checked && $(longMin).attr('data-value')) {
    document.querySelector('.sum__value').innerHTML = `${$(longMin).attr('data-value')}руб`;
  }
  if (longMax.checked && $(longMax).attr('data-value')) {
    document.querySelector('.sum__value').innerHTML = `${$(longMax).attr('data-value')}руб`;
  }
}

$('.order__input_card').mask('XXXX-XXXX-XXXX-XXXX');
$('.order__input_date').mask('XX/XX');

});
