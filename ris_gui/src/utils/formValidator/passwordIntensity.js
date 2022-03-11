const passwordIntensity = (value) => {
  // lowercase, uppercase, digits, symbol, length
  let list = [0, 0, 0, 0, 0];
  if (value.match(/([a-z])+/)) {
    list[0] = 20;
  } else { list[0] = 0; }
  if (value.match(/([A-Z])+/)) {
    list[1] = 20;
  } else { list[1] = 0; }
  if (value.match(/([0-9])+/)) {
    list[2] = 20;
  } else { list[2] = 0; }
  if (value.match(/([\!\@\#\$\%\^\&\*\(\)\_\=\|\{\}\:\<\>\?\-\=\[\]\;\,\.\/\~])+/)) {
    list[3] = 20;
  } else { list[3] = 0; }
  if (value.length > 7 && value.length < 21) {
    list[4] = 20;
  } else { list[4] = 0; }
  let level = list[0] + list[1] + list[2] + list[3] + list[4];
  return level;
}


export default passwordIntensity;