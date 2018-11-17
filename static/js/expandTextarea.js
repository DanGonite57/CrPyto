function expandTextarea(element) {
  element.style.overflow = 'hidden';
  element.style.height = "0px";
  element.style.height = element.scrollHeight + 'px';
}
