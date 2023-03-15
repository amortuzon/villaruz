console.log('hello world')

// get all the starts
const one = document.getElementById('first')
const two = document.getElementById('second')
const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')

const arr = [one, two, three, four, five].filter(Boolean)

arr.forEach(item => {
  item.addEventListener('mouseover', (event) => {
    console.log(event.target)
  })
})