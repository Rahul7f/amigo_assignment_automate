const answers = {
  1:'a',
  2:'d',
  3:'a',
  4:'c',
  5:'d',
  6:'d',
  7:'b',
  8:'a',
  9:'d',
  10:'a',
  11:'c',
  12:'a',
  13:'a',
  14:'a',
  15:'d',
  16:'a',
  17:'a'
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