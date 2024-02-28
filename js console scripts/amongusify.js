console.log('START');

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
imurl = 'data:image/png;base64,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';
x = 0
while (true) {

const elements = document.querySelectorAll('a, img');
for (const element of elements) {
  // Set the new href or src based on the tag type
  if (element.tagName === 'A') {
    element.href = imurl;
  } else if (element.tagName === 'IMG') {
    element.src = imurl;
  }
}

const images = document.querySelectorAll('img');

for (const image of images) {
   // Set the new image source only if it's initially an image (not a placeholder)
   
   image.src = imurl
 

 // Set the alt attribute if it's currently empty
 image.alt = imurl

}

const pictures = document.querySelectorAll('picture');

for (const picture of pictures) {
  const sources = picture.querySelectorAll('source');
  for (const source of sources) {
    // Modify srcset only if it exists and doesn't already contain a placeholder

    source.srcset = source.srcset.replace(/image\.jpg/g, imurl);
    
  }
}


if (x == 10) {
console.clear()
x = 0
}
x = x + 1

await sleep(1000)
}
