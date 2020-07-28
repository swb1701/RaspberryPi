const get360ViewProps = (image) => ({
  folder: attr(image, 'folder') || attr(image, 'data-folder') || '/',
  filename: attr(image, 'filename') || attr(image, 'data-filename') || 'image-{index}.jpg',
  imageList: attr(image, 'image-list') || attr(image, 'data-image-list') || null,
  indexZeroBase: parseInt(attr(image, 'index-zero-base') || attr(image, 'data-index-zero-base') || 0, 10),
  amount: parseInt(attr(image, 'amount') || attr(image, 'data-amount') || 36, 10),
  speed: parseInt(attr(image, 'speed') || attr(image, 'data-speed') || 80, 10),
  dragSpeed: parseInt(attr(image, 'drag-speed') || attr(image, 'data-drag-speed') || 150, 10),
  keys: isTrue(image, 'keys'),
  boxShadow: attr(image, 'box-shadow') || attr(image, 'data-box-shadow'),
  autoplay: isTrue(image, 'autoplay'),
  autoplayReverse: isTrue(image, 'autoplay-reverse'),
  bottomCircle: isTrue(image, 'bottom-circle'),
  fullScreen: isTrue(image, 'full-screen'),
  magnifier: ((attr(image, 'magnifier') !== null) || (attr(image, 'data-magnifier') !== null)) &&
    parseInt(attr(image, 'magnifier') || attr(image, 'data-magnifier'), 10),
  bottomCircleOffset: parseInt(attr(image, 'bottom-circle-offset') || attr(image, 'data-bottom-circle-offset') || 5, 10),
  ratio: parseFloat(attr(image, 'ratio') || attr(image, 'data-ratio') || 0) || false,
  responsive: isTrue(image, 'responsive'),
  ciToken: attr(image, 'responsive') || attr(image, 'data-responsive') || 'demo',
  ciSize: attr(image, 'size') || attr(image, 'data-size'),
  ciOperation: attr(image, 'operation') || attr(image, 'data-operation') || 'width',
  ciFilters: attr(image, 'filters') || attr(image, 'data-filters') || 'q35',
  lazyload: isTrue(image, 'lazyload'),
  lazySelector: attr(image, 'lazyload-selector') || attr(image, 'data-lazyload-selector') || 'lazyload',
  spinReverse: isTrue(image, 'spin-reverse'),
  controlReverse: isTrue(image, 'control-reverse'),
  stopAtEdges: isTrue(image, 'stop-at-edges')
});

const isTrue = (image, type) => {
  const imgProp = attr(image, type);
  const imgDataProp = attr(image, `data-${type}`);

  return (imgProp !== null && imgProp !== 'false') || (imgDataProp !== null && imgDataProp !== 'false');
};

const attr = (element, attribute) => element.getAttribute(attribute);

const set360ViewIconStyles = (view360Icon) => {
  view360Icon.style.position = 'absolute';
  view360Icon.style.top = '0';
  view360Icon.style.bottom = '0';
  view360Icon.style.left = '0';
  view360Icon.style.right = '0';
  view360Icon.style.width = '100px';
  view360Icon.style.height = '100px';
  view360Icon.style.margin = 'auto';
  view360Icon.style.backgroundColor = 'rgba(255,255,255,0.8)';
  view360Icon.style.borderRadius = '50%';
  view360Icon.style.boxShadow = 'rgb(255, 255, 255, 0.5) 0px 0px 4px';
  view360Icon.style.transition = '0.5s all';
  view360Icon.style.color = 'rgb(80,80,80)';
  view360Icon.style.textAlign = 'center';
  view360Icon.style.lineHeight = '100px';
  view360Icon.style.zIndex = '2';
};

const setView360Icon = (view360Icon) => {
  view360Icon.style.background = `rgba(255,255,255,0.8) url('../360_view.svg') 50% 50% / contain no-repeat`;
}

const set360ViewCircleIconStyles = (view360CircleIcon, bottomCircleOffset) => {
  view360CircleIcon.src = `../360.svg`;
  view360CircleIcon.style.position = 'absolute';
  view360CircleIcon.style.top = 'auto';
  view360CircleIcon.style.bottom = bottomCircleOffset + '%';
  view360CircleIcon.style.left = '0';
  view360CircleIcon.style.right = '0';
  view360CircleIcon.style.width = '80%';
  view360CircleIcon.style.height = 'auto';
  view360CircleIcon.style.margin = 'auto';
  view360CircleIcon.style.transition = '0.5s all';
  view360CircleIcon.style.zIndex = '2';
};

const setLoaderStyles = (loader) => {
  loader.className = 'cloudimage-360-loader';
  loader.style.position = 'absolute';
  loader.style.zIndex = '100';
  loader.style.top = '0';
  loader.style.left = '0';
  loader.style.right = '0';
  loader.style.width = '0%';
  loader.style.height = '8px';
  loader.style.background = 'rgb(165,175,184)';
};

const setBoxShadowStyles = (boxShadow, boxShadowValue) => {
  boxShadow.className = 'cloudimage-360-box-shadow';
  boxShadow.style.position = 'absolute';
  boxShadow.style.zIndex = '99';
  boxShadow.style.top = '0';
  boxShadow.style.left = '0';
  boxShadow.style.right = '0';
  boxShadow.style.bottom = '0';
  boxShadow.style.boxShadow = boxShadowValue;
};

const setMagnifyIconStyles = (magnifyIcon, fullScreen) => {
  magnifyIcon.style.position = 'absolute';
  magnifyIcon.style.top = fullScreen ? '35px' : '5px';
  magnifyIcon.style.right = '5px';
  magnifyIcon.style.width = '25px';
  magnifyIcon.style.height = '25px';
  magnifyIcon.style.zIndex = '101';
  magnifyIcon.style.cursor = 'pointer';
  magnifyIcon.style.background = `url('https://scaleflex.ultrafast.io/https://scaleflex.airstore.io/filerobot/js-cloudimage-360-view/loupe.svg') 50% 50% / cover no-repeat`;
};

const setFullScreenModalStyles = (fullScreenModal) => {
  fullScreenModal.style.position = 'fixed';
  fullScreenModal.style.top = '0';
  fullScreenModal.style.bottom = '0';
  fullScreenModal.style.left = '0';
  fullScreenModal.style.right = '0';
  fullScreenModal.style.width = '100%';
  fullScreenModal.style.height = '100%';
  fullScreenModal.style.zIndex = '999';
  fullScreenModal.style.background = '#fff';
};

const setFullScreenIconStyles = (fullScreenIcon) => {
  fullScreenIcon.style.position = 'absolute';
  fullScreenIcon.style.top = '5px';
  fullScreenIcon.style.right = '5px';
  fullScreenIcon.style.width = '25px';
  fullScreenIcon.style.height = '25px';
  fullScreenIcon.style.zIndex = '101';
  fullScreenIcon.style.cursor = 'pointer';
  fullScreenIcon.style.background = `url('https://scaleflex.ultrafast.io/https://scaleflex.airstore.io/filerobot/js-cloudimage-360-view/full_screen.svg') 50% 50% / cover no-repeat`;
};

const setCloseFullScreenViewStyles = (closeFullScreenIcon) => {
  closeFullScreenIcon.style.position = 'absolute';
  closeFullScreenIcon.style.top = '5px';
  closeFullScreenIcon.style.right = '5px';
  closeFullScreenIcon.style.width = '25px';
  closeFullScreenIcon.style.height = '25px';
  closeFullScreenIcon.style.zIndex = '101';
  closeFullScreenIcon.style.cursor = 'pointer';
  closeFullScreenIcon.style.background = `url('https://scaleflex.ultrafast.io/https://scaleflex.airstore.io/filerobot/js-cloudimage-360-view/cross.svg') 50% 50% / cover no-repeat`;
};

const magnify = (container, src, glass, zoom) => {
  let w, h, bw;
  glass.setAttribute("class", "img-magnifier-glass");
  container.prepend(glass);

  glass.style.backgroundColor = '#fff';
  glass.style.backgroundImage = "url('" + src + "')";
  glass.style.backgroundRepeat = "no-repeat";
  glass.style.backgroundSize = (container.offsetWidth * zoom) + "px " + (container.offsetHeight * zoom) + "px";
  glass.style.position = 'absolute';
  glass.style.border = '3px solid #000';
  glass.style.borderRadius = '50%';
  glass.style.cursor = 'wait';
  glass.style.lineHeight = '200px';
  glass.style.textAlign = 'center';
  glass.style.zIndex = '1000';

  glass.style.width = '250px';
  glass.style.height = '250px';
  glass.style.top = '-75px';
  glass.style.right = '-85px';

  bw = 3;
  w = glass.offsetWidth / 2;
  h = glass.offsetHeight / 2;

  glass.addEventListener("mousemove", moveMagnifier);
  container.addEventListener("mousemove", moveMagnifier);

  glass.addEventListener("touchmove", moveMagnifier);
  container.addEventListener("touchmove", moveMagnifier);

  function moveMagnifier(e) {
    let pos, x, y;

    e.preventDefault();

    pos = getCursorPos(e);
    x = pos.x;
    y = pos.y;

    if (x > container.offsetWidth - (w / zoom)) {
      x = container.offsetWidth - (w / zoom);
    }

    if (x < w / zoom) {
      x = w / zoom;
    }

    if (y > container.offsetHeight - (h / zoom)) {
      y = container.offsetHeight - (h / zoom);
    }

    if (y < h / zoom) {
      y = h / zoom;
    }

    glass.style.left = (x - w) + "px";
    glass.style.top = (y - h) + "px";

    glass.style.backgroundPosition = "-" + ((x * zoom) - w + bw) + "px -" + ((y * zoom) - h + bw) + "px";
  }

  function getCursorPos(e) {
    let a, x = 0, y = 0;
    e = e || window.event;
    a = container.getBoundingClientRect();
    x = e.pageX - a.left;
    y = e.pageY - a.top;
    x = x - window.pageXOffset;
    y = y - window.pageYOffset;

    return { x, y };
  }
};

const getSizeLimit = (currentSize) => {
  if (currentSize <= 25) return '25';
  if (currentSize <= 50) return '50';

  return (Math.ceil(currentSize / 100) * 100).toString();
};

const getSizeAccordingToPixelRatio = size => {
  const splittedSizes = size.toString().split('x');
  const result = [];

  [].forEach.call(splittedSizes, size => {
    result.push(size * Math.round(window.devicePixelRatio || 1));
  });

  return result.join('x');
};

const getResponsiveWidthOfContainer = width => getSizeLimit(width);

const fit = (contains) => {
  return (parentWidth, parentHeight, childWidth, childHeight, scale = 1, offsetX = 0.5, offsetY = 0.5) => {
    const childRatio = childWidth / childHeight
    const parentRatio = parentWidth / parentHeight
    let width = parentWidth * scale
    let height = parentHeight * scale

    if (contains ? (childRatio > parentRatio) : (childRatio < parentRatio)) {
      height = width / childRatio
    } else {
      width = height * childRatio
    }

    return {
      width,
      height,
      offsetX: (parentWidth - width) * offsetX,
      offsetY: (parentHeight - height) * offsetY
    }
  }
};

const contain = fit(true);

const addClass = (el, className) => {
  if (el.classList)
    el.classList.add(className);
  else
    el.className += ' ' + className;
};

const removeClass = (el, className) => {
  if (el.classList)
    el.classList.remove(className);
  else
    el.className = el.className.replace(new RegExp('(^|\\b)' + className.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
};

const pad = (n, width = 0) => {
  n = n + '';

  return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
};

class CI360Viewer {
  constructor(container, fullScreen, ratio) {
    this.container = container;
    this.activeImage = 1;
    this.movementStart = 0;
    this.isClicked = false;
    this.loadedImages = 0;
    this.imagesLoaded = false;
    this.reversed = false;
    this.fullScreenView = !!fullScreen;
    this.ratio = ratio;
    this.images = [];
    this.devicePixelRatio = Math.round(window.devicePixelRatio || 1);
    this.isMobile = !!('ontouchstart' in window || navigator.msMaxTouchPoints);
    this.id = container.id;
    this.init(container);
  }

  mousedown(event) {
    event.preventDefault();

    if (!this.imagesLoaded) return;

    if (this.glass) {
      this.closeMagnifier();
    }

    if (this.view360Icon) {
      this.remove360ViewIcon();
    }

    if (this.autoplay || this.loopTimeoutId) {
      this.stop();
      this.autoplay = false;
    }

    this.movementStart = event.pageX;
    this.isClicked = true;
    this.container.style.cursor = 'grabbing';
  }

  mouseup() {
    if (!this.imagesLoaded) return;

    this.movementStart = 0;
    this.isClicked = false;
    this.container.style.cursor = 'grab';

    if (this.bottomCircle) {
      this.show360ViewCircleIcon();
    }
  }

  mousemove(event) {
    if (!this.isClicked || !this.imagesLoaded) return;

    this.onMove(event.pageX);
  }

  touchstart(event) {
    if (!this.imagesLoaded) return;

    if (this.glass) {
      this.closeMagnifier();
    }

    if (this.view360Icon) {
      this.remove360ViewIcon();
    }

    if (this.autoplay || this.loopTimeoutId) {
      this.stop();
      this.autoplay = false;
    }

    this.movementStart = event.touches[0].clientX;
    this.isClicked = true;
  }

  touchend() {
    if (!this.imagesLoaded) return;

    this.movementStart = 0;
    this.isClicked = false;

    if (this.bottomCircle) this.show360ViewCircleIcon();
  }

  touchmove(event) {
    if (!this.isClicked || !this.imagesLoaded) return;

    this.onMove(event.touches[0].clientX);
  }

  keydownGeneral() {
    if (!this.imagesLoaded) return;

    if (this.glass) {
      this.closeMagnifier();
    }
  }

  keydown(event) {
    if (!this.imagesLoaded) return;

    if (this.glass) {
      this.closeMagnifier();
    }

    if ([37, 39].includes(event.keyCode)) {
      if (37 === event.keyCode) {
        if (this.reversed)
          this.prev();
        else
          this.next();
      } else if (39 === event.keyCode) {
        if (this.reversed)
          this.next();
        else
          this.prev();
      }

      this.onSpin();
    }
  }

  onSpin() {
    if (this.bottomCircle) {
      this.hide360ViewCircleIcon();
    }

    if (this.view360Icon) {
      this.remove360ViewIcon();
    }

    if (this.autoplay || this.loopTimeoutId) {
      this.stop();
      this.autoplay = false;
    }
  }

  keyup(event) {
    if (!this.imagesLoaded) return;

    if ([37, 39].includes(event.keyCode)) {
      this.onFinishSpin();
    }
  }

  onFinishSpin() {
    if (this.bottomCircle) this.show360ViewCircleIcon();
  }

  setActiveIndex(idx) {
    this.activeImage=idx;
    this.update();
  }

  onMove(pageX) {
    if (pageX - this.movementStart >= this.speedFactor) {
      let itemsSkippedRight = Math.floor((pageX - this.movementStart) / this.speedFactor) || 1;

      this.movementStart = pageX;

      if (this.spinReverse) {
        this.moveActiveIndexDown(itemsSkippedRight);
      } else {
        this.moveActiveIndexUp(itemsSkippedRight);
      }

      if (this.bottomCircle) this.hide360ViewCircleIcon();
      this.update();
    } else if (this.movementStart - pageX >= this.speedFactor) {
      let itemsSkippedLeft = Math.floor((this.movementStart - pageX) / this.speedFactor) || 1;

      this.movementStart = pageX;

      if (this.spinReverse) {
        this.moveActiveIndexUp(itemsSkippedLeft);
      } else {
        this.moveActiveIndexDown(itemsSkippedLeft);
      }

      if (this.bottomCircle) this.hide360ViewCircleIcon();
      this.update();
    }
  }

  moveActiveIndexUp(itemsSkipped) {
    const isReverse = this.controlReverse ? !this.spinReverse : this.spinReverse;

    if (this.stopAtEdges) {
      if (this.activeImage + itemsSkipped >= this.amount) {
        this.activeImage = this.amount;

        if (isReverse ? this.prevElem : this.nextElem) {
          addClass(isReverse ? this.prevElem : this.nextElem, 'not-active');
        }
      } else {
        this.activeImage += itemsSkipped;

        if (this.nextElem) {
          removeClass(this.nextElem, 'not-active');
        }

        if (this.prevElem) {
          removeClass(this.prevElem, 'not-active');
        }
      }
    } else {
      this.activeImage = (this.activeImage + itemsSkipped) % this.amount || this.amount;
    }
  }

  moveActiveIndexDown(itemsSkipped) {
    const isReverse = this.controlReverse ? !this.spinReverse : this.spinReverse;

    if (this.stopAtEdges) {
      if (this.activeImage - itemsSkipped <= 1) {
        this.activeImage = 1;

        if (isReverse ? this.nextElem : this.prevElem) {
          addClass(isReverse ? this.nextElem : this.prevElem, 'not-active');
        }
      } else {
        this.activeImage -= itemsSkipped;

        if (this.prevElem) {
          removeClass(this.prevElem, 'not-active');
        }
        if (this.nextElem) {
          removeClass(this.nextElem, 'not-active');
        }
      }
    } else {
      if (this.activeImage - itemsSkipped < 1) {
        this.activeImage = this.amount + (this.activeImage - itemsSkipped);
      } else {
        this.activeImage -= itemsSkipped;
      }
    }
  }

  loop(reversed) {
    reversed ? this.prev() : this.next();
  }

  next() {
    this.moveActiveIndexUp(1);
    this.update();
  }

  prev() {
    this.moveActiveIndexDown(1);
    this.update();
  }

  update() {
    const image = this.images[this.activeImage - 1];
    const ctx = this.canvas.getContext("2d");

    ctx.scale(this.devicePixelRatio, this.devicePixelRatio);

    if (this.fullScreenView) {
      this.canvas.width = window.innerWidth * this.devicePixelRatio;
      this.canvas.style.width = window.innerWidth + 'px';
      this.canvas.height = window.innerHeight * this.devicePixelRatio;
      this.canvas.style.height = window.innerHeight + 'px';

      const { offsetX, offsetY, width, height } =
        contain(this.canvas.width, this.canvas.height, image.width, image.height);

      ctx.drawImage(image, offsetX, offsetY, width, height);
    } else {
      this.canvas.width = this.container.offsetWidth * this.devicePixelRatio;
      this.canvas.style.width = this.container.offsetWidth + 'px';
      this.canvas.height = this.container.offsetWidth * this.devicePixelRatio / image.width * image.height;
      this.canvas.style.height = this.container.offsetWidth / image.width * image.height + 'px';

      ctx.drawImage(image, 0, 0, this.canvas.width, this.canvas.height);
    }
  }

  updatePercentageInLoader(percentage) {
    if (this.loader) {
      this.loader.style.width = percentage + '%';
    }

    if (this.view360Icon) {
      this.view360Icon.innerText = percentage + '%';
    }
  }

  onAllImagesLoaded() {
    this.imagesLoaded = true;
    this.container.style.cursor = 'grab';
    this.removeLoader();

    if (!this.fullScreenView) {
      this.speedFactor = Math.floor(this.dragSpeed / 150 * 36 / this.amount * 25 * this.container.offsetWidth / 1500) || 1;
    } else {
      const containerRatio = this.container.offsetHeight / this.container.offsetWidth;
      let imageOffsetWidth = this.container.offsetWidth;

      if (this.ratio > containerRatio) {
        imageOffsetWidth = this.container.offsetHeight / this.ratio;
      }

      this.speedFactor = Math.floor(this.dragSpeed / 150 * 36 / this.amount * 25 * imageOffsetWidth / 1500) || 1;
    }

    if (this.autoplay) {
      this.play();
    }

    if (this.view360Icon) {
      this.view360Icon.innerText = '';
      setView360Icon(this.view360Icon);
    }

    this.initControls();
  }

  onFirstImageLoaded(event) {
    this.add360ViewIcon();

    if (this.fullScreenView) {
      this.canvas.width = window.innerWidth * this.devicePixelRatio;
      this.canvas.style.width = window.innerWidth + 'px';
      this.canvas.height = window.innerHeight * this.devicePixelRatio;
      this.canvas.style.height = window.innerHeight + 'px';

      const ctx = this.canvas.getContext("2d");

      const { offsetX, offsetY, width, height } =
        contain(this.canvas.width, this.canvas.height, event.target.width, event.target.height);

      ctx.drawImage(event.target, offsetX, offsetY, width, height);
    } else {
      this.canvas.width = this.container.offsetWidth * this.devicePixelRatio;
      this.canvas.style.width = this.container.offsetWidth + 'px';
      this.canvas.height = this.container.offsetWidth * this.devicePixelRatio / event.target.width * event.target.height;
      this.canvas.style.height = this.container.offsetWidth / event.target.width * event.target.height + 'px';

      const ctx = this.canvas.getContext("2d");

      ctx.drawImage(event.target, 0, 0, this.canvas.width, this.canvas.height);
    }

    if (this.lazyload && !this.fullScreenView) {
      this.images
        .forEach((image, index) => {
          if (index === 0) {
            this.innerBox.removeChild(this.lazyloadInitImage);
            return;
          }

          const dataSrc = image.getAttribute('data-src');

          if (dataSrc) {
            image.src = image.getAttribute('data-src');
          }
        });
    }

    if (this.ratio) {
      this.container.style.minHeight = 'auto';
    }

    if (this.magnifier && !this.fullScreenView) {
      this.addMagnifier();
    }

    if (this.boxShadow && !this.fullScreenView) {
      this.addBoxShadow();
    }

    if (this.bottomCircle && !this.fullScreenView) {
      this.add360ViewCircleIcon();
    }

    if (this.fullScreen && !this.fullScreenView) {
      this.addFullScreenIcon();
    } else if (this.fullScreenView) {
      this.addCloseFullScreenView();
    }
  }

  onImageLoad(index, event) {
    const percentage = Math.round(this.loadedImages / this.amount * 100);

    this.loadedImages += 1;
    this.updatePercentageInLoader(percentage);

    if (this.loadedImages === this.amount) {
      this.onAllImagesLoaded(event);
    } else if (index === 0) {
      this.onFirstImageLoaded(event);
    }
  }

  addCloseFullScreenView() {
    const closeFullScreenIcon = document.createElement('div');

    setCloseFullScreenViewStyles(closeFullScreenIcon);

    closeFullScreenIcon.onclick = this.closeFullScreenModal.bind(this);

    this.innerBox.appendChild(closeFullScreenIcon);
  }

  add360ViewIcon() {
    const view360Icon = document.createElement('div');

    set360ViewIconStyles(view360Icon);

    view360Icon.innerText = '0%';

    this.view360Icon = view360Icon;
    this.innerBox.appendChild(view360Icon);
  }

  addFullScreenIcon() {
    const fullScreenIcon = document.createElement('div');

    setFullScreenIconStyles(fullScreenIcon);

    fullScreenIcon.onclick = this.openFullScreenModal.bind(this);

    this.innerBox.appendChild(fullScreenIcon);
  }

  addMagnifier() {
    const magnifyIcon = document.createElement('div');

    setMagnifyIconStyles(magnifyIcon, this.fullScreen);

    magnifyIcon.onclick = this.magnify.bind(this);

    this.innerBox.appendChild(magnifyIcon);
  }

  getOriginalSrc() {
    const currentImage = this.images[this.activeImage - 1];
    const lastIndex = currentImage.src.lastIndexOf('//');

    return lastIndex > 10 ? currentImage.src.slice(lastIndex) : currentImage.src;
  }

  magnify() {
    const image = new Image();
    const src = this.getOriginalSrc();

    image.src = src;
    image.onload = () => {
      if (this.glass) {
        this.glass.style.cursor = 'none';
      }
    };

    this.glass = document.createElement('div');
    this.container.style.overflow = 'hidden';
    magnify(this.container, src, this.glass, this.magnifier || 3);
  }

  closeMagnifier() {
    if (!this.glass) return;

    this.container.style.overflow = 'visible';
    this.container.removeChild(this.glass);
    this.glass = null;
  }

  openFullScreenModal() {
    const fullScreenModal = document.createElement('div');

    setFullScreenModalStyles(fullScreenModal);

    const fullScreenContainer = this.container.cloneNode();
    const image = this.images[0];
    const ratio = image.height / image.width;

    fullScreenContainer.style.height = '100%';
    fullScreenContainer.style.maxHeight = '100%';

    fullScreenModal.appendChild(fullScreenContainer);

    window.document.body.appendChild(fullScreenModal);

    new CI360Viewer(fullScreenContainer, true, ratio);
  }

  closeFullScreenModal() {
    document.body.removeChild(this.container.parentNode);
  }

  add360ViewCircleIcon() {
    const view360CircleIcon = new Image();

    set360ViewCircleIconStyles(view360CircleIcon, this.bottomCircleOffset);

    this.view360CircleIcon = view360CircleIcon;
    this.innerBox.appendChild(view360CircleIcon);
  }

  hide360ViewCircleIcon() {
    if (!this.view360CircleIcon) return;

    this.view360CircleIcon.style.opacity = '0';
  }

  show360ViewCircleIcon() {
    if (!this.view360CircleIcon) return;

    this.view360CircleIcon.style.opacity = '1';
  }

  remove360ViewCircleIcon() {
    if (!this.view360CircleIcon) return;

    this.innerBox.removeChild(this.view360CircleIcon);
    this.view360CircleIcon = null;
  }

  addLoader() {
    const loader = document.createElement('div');

    setLoaderStyles(loader);

    this.loader = loader;
    this.innerBox.appendChild(loader);
  }

  addBoxShadow() {
    const boxShadow = document.createElement('div');

    setBoxShadowStyles(boxShadow, this.boxShadow);

    this.innerBox.appendChild(boxShadow);
  }

  removeLoader() {
    if (!this.loader) return;

    this.innerBox.removeChild(this.loader);
    this.loader = null;
  }

  remove360ViewIcon() {
    if (!this.view360Icon) return;

    this.innerBox.removeChild(this.view360Icon);
    this.view360Icon = null;
  }

  play() {
    if (this.bottomCircle) this.hide360ViewCircleIcon();
    this.remove360ViewIcon();

    this.loopTimeoutId = window.setInterval(() => {
      this.loop(this.reversed);
    }, this.autoplaySpeed);
  }

  stop() {
    if (this.bottomCircle) this.show360ViewCircleIcon();
    window.clearTimeout(this.loopTimeoutId);
  }

  getSrc(responsive, container, folder, filename, { ciSize, ciToken, ciOperation, ciFilters }) {
    let src = `${folder}${filename}`;

    if (responsive) {
      let imageOffsetWidth = container.offsetWidth;

      if (this.fullScreenView) {
        const containerRatio = container.offsetHeight / container.offsetWidth;

        if (this.ratio > containerRatio) {
          imageOffsetWidth = container.offsetHeight / this.ratio;
        }
      }

      const ciSizeNext = getSizeAccordingToPixelRatio(ciSize || getResponsiveWidthOfContainer(imageOffsetWidth));

      src = `https://${ciToken}.cloudimg.io/${ciOperation}/${ciSizeNext}/${ciFilters}/${src}`;
    }

    return src;
  }

  preloadImages(amount, src, lazyload, lazySelector, container, responsive, ciParams) {
    if (this.imageList) {
      try {
        const images = JSON.parse(this.imageList);

        this.amount = images.length;
        images.forEach((src, index) => {
          const folder = /(http(s?)):\/\//gi.test(src) ? '' : this.folder;
          const resultSrc = this.getSrc(responsive, container, folder, src, ciParams);

          this.addImage(resultSrc, lazyload, lazySelector, index);
        });
      } catch (error) {
        console.error(`Wrong format in image-list attribute: ${error.message}`);
      }
    } else {
      [...new Array(amount)].map((_item, index) => {
        const nextZeroFilledIndex = pad(index + 1, this.indexZeroBase);
        const resultSrc = src.replace('{index}', nextZeroFilledIndex);
        this.addImage(resultSrc, lazyload, lazySelector, index);
      });
    }
  }

  addImage(resultSrc, lazyload, lazySelector, index) {
    const image = new Image();

    if (lazyload && !this.fullScreenView) {
      image.setAttribute('data-src', resultSrc);
      image.className = image.className.length ? image.className + ` ${lazySelector}` : lazySelector;

      if (index === 0) {
        this.lazyloadInitImage = image;
        image.style.position = 'absolute';
        image.style.top = '0';
        image.style.left = '0';
        this.innerBox.appendChild(image);
      }
    } else {
      image.src = resultSrc;
    }

    image.onload = this.onImageLoad.bind(this, index);
    image.onerror = this.onImageLoad.bind(this, index);
    this.images.push(image);
  }

  destroy() {
    stop();

    const oldElement = this.container;
    const newElement = oldElement.cloneNode(true);
    const innerBox = newElement.querySelector('.cloudimage-inner-box');

    newElement.className = newElement.className.replace(' initialized', '');
    newElement.style.position = 'relative';
    newElement.style.width = '100%';
    newElement.style.cursor = 'default';
    newElement.setAttribute('draggable', 'false');
    newElement.style.minHeight = 'auto';
    newElement.removeChild(innerBox);
    oldElement.parentNode.replaceChild(newElement, oldElement);
  }

  initControls() {
    const isReverse = this.controlReverse ? !this.spinReverse : this.spinReverse;
    const prev = this.container.querySelector('.cloudimage-360-prev');
    const next = this.container.querySelector('.cloudimage-360-next');

    if (!prev && !next) return;

    const onLeftStart = (event) => {
      event.stopPropagation();
      this.onSpin();
      this.prev();
      this.loopTimeoutId = window.setInterval(this.prev.bind(this), this.autoplaySpeed);
    };
    const onRightStart = (event) => {
      event.stopPropagation();
      this.onSpin();
      this.next();
      this.loopTimeoutId = window.setInterval(this.next.bind(this), this.autoplaySpeed);
    };
    const onLeftEnd = () => {
      this.onFinishSpin();
      window.clearTimeout(this.loopTimeoutId);
    };
    const onRightEnd = () => {
      this.onFinishSpin();
      window.clearTimeout(this.loopTimeoutId);
    };

    if (prev) {
      prev.style.display = 'block';
      prev.addEventListener('mousedown', isReverse ? onRightStart : onLeftStart);
      prev.addEventListener('touchstart', isReverse ? onRightStart : onLeftStart);
      prev.addEventListener('mouseup', isReverse ? onRightEnd : onLeftEnd);
      prev.addEventListener('touchend', isReverse ? onRightEnd : onLeftEnd);

      this.prevElem = prev;
    }

    if (next) {
      next.style.display = 'block';
      next.addEventListener('mousedown', isReverse ? onLeftStart : onRightStart);
      next.addEventListener('touchstart', isReverse ? onLeftStart : onRightStart);
      next.addEventListener('mouseup', isReverse ? onLeftEnd : onRightEnd);
      next.addEventListener('touchend', isReverse ? onLeftEnd : onRightEnd);

      this.nextElem = next;
    }

    if (isReverse ? next : prev) {
      if (this.stopAtEdges) {
        addClass(isReverse ? next : prev, 'not-active');
      }
    }
  }

  addInnerBox() {
    this.innerBox = document.createElement('div');
    this.innerBox.className = 'cloudimage-inner-box';
    this.container.appendChild(this.innerBox);
  }

  addCanvas() {
    this.canvas = document.createElement('canvas');
    this.canvas.style.width = '100%';
    this.canvas.style.fontSize = '0';

    if (this.ratio) {
      this.container.style.minHeight = this.container.offsetWidth * this.ratio + 'px';
      this.canvas.height = parseInt(this.container.style.minHeight);
    }

    this.innerBox.appendChild(this.canvas);
  }

  attachEvents(draggable, swipeable, keys) {
    if (draggable) {
      this.container.addEventListener('mousedown', this.mousedown.bind(this));
      this.container.addEventListener('mouseup', this.mouseup.bind(this));
      this.container.addEventListener('mousemove', this.mousemove.bind(this));
    }

    if (swipeable) {
      this.container.addEventListener('touchstart', this.touchstart.bind(this), { passive: true });
      this.container.addEventListener('touchend', this.touchend.bind(this), { passive: true });
      this.container.addEventListener('touchmove', this.touchmove.bind(this));
    }

    if (keys) {
      document.addEventListener('keydown', this.keydown.bind(this));
      document.addEventListener('keyup', this.keyup.bind(this));
    } else {
      document.addEventListener('keydown', this.keydownGeneral.bind(this));
    }
  }

  applyStylesToContainer() {
    this.container.style.position = 'relative';
    this.container.style.width = '100%';
    this.container.style.cursor = 'wait';
    this.container.setAttribute('draggable', 'false');
    this.container.className = `${this.container.className} initialized`;
  }

  init(container) {
    let {
      folder, filename, imageList, indexZeroBase, amount, draggable = true, swipeable = true, keys, bottomCircle, bottomCircleOffset, boxShadow,
      autoplay, speed, autoplayReverse, fullScreen, magnifier, ratio, responsive, ciToken, ciSize, ciOperation,
      ciFilters, lazyload, lazySelector, spinReverse, dragSpeed, stopAtEdges, controlReverse
    } = get360ViewProps(container);
    const ciParams = { ciSize, ciToken, ciOperation, ciFilters };

    this.addInnerBox();
    this.addLoader();

    this.folder = folder;
    this.filename = filename;
    this.imageList = imageList;
    this.indexZeroBase = indexZeroBase;
    this.amount = amount;
    this.bottomCircle = bottomCircle;
    this.bottomCircleOffset = bottomCircleOffset;
    this.boxShadow = boxShadow;
    this.autoplay = autoplay && !this.isMobile;
    this.speed = speed;
    this.reversed = autoplayReverse;
    this.fullScreen = fullScreen;
    this.magnifier = !this.isMobile && magnifier ? magnifier : false;
    this.lazyload = lazyload;
    this.ratio = ratio;
    this.spinReverse = spinReverse;
    this.controlReverse = controlReverse;
    this.dragSpeed = dragSpeed;
    this.autoplaySpeed = this.speed * 36 / this.amount;
    this.stopAtEdges = stopAtEdges;

    this.applyStylesToContainer();

    this.addCanvas();

    let src = this.getSrc(responsive, container, folder, filename, ciParams);

    this.preloadImages(amount, src, lazyload, lazySelector, container, responsive, ciParams);

    this.attachEvents(draggable, swipeable, keys);
  }
}

function init() {
  const viewers = [];
  const view360Array = document.querySelectorAll('.cloudimage-360:not(.initialized)');

  [].slice.call(view360Array).forEach(container => { viewers.push(new CI360Viewer(container)); });

  window.CI360._viewers = viewers;
}

function destroy() {
  if (isNoViewers()) return;

  window.CI360._viewers.forEach(viewer => { viewer.destroy(); });

  window.CI360._viewers = [];
}

function getActiveIndexByID(id) {
  if (isNoViewers()) return;

  let currentViewer = window.CI360._viewers.filter(viewer => viewer.id === id)[0];

  return currentViewer && (currentViewer.activeImage - 1);
}

function getViewerByID(id) {
  if (isNoViewers()) return;

    let currentViewer = window.CI360._viewers.filter(viewer => viewer.id === id)[0];

    return(currentViewer)
}

function isNoViewers() {
  return !(window.CI360._viewers && window.CI360._viewers.length > 0);
}

window.CI360 = window.CI360 || {};
window.CI360.init = init;
window.CI360.destroy = destroy;
window.CI360.getActiveIndexByID = getActiveIndexByID;
window.CI360.getViewerByID = getViewerByID;

if (!window.CI360.notInitOnLoad) {
  init();
}
