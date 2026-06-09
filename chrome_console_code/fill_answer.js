const answers = {
  1:'d',
  2:'c',
  3:'b',
  4:'a',
  5:'d',
  6:'a',
  7:'a',
  8:'a',
  9:'a',
  10:'b',
  11:'a',
  12:'a',
  13:'a',
  14:'c',
  15:'d',
  16:'a',
  17:'c'
};

const map = { a:0, b:1, c:2, d:3 };

for (const [q, ans] of Object.entries(answers)) {
  const radio = document.querySelector(
    `input[id$=":${q}_answer${map[ans]}"]`
  );

  if (radio) {
    radio.click();
  }
}