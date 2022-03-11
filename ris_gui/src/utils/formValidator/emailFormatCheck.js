const emailFormatCheck = (rule, value, callback) => {
  let emailRegex =
    /^[a-z]([a-z0-9]*[-_\.]?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,4}([\.][a-z]{2,5}){0,3}$/i;
  if (!emailRegex.test(value)) {
    callback(new Error("Invalid email format."));
  } else {
    callback();
  }
};

export default emailFormatCheck

export const emailSuffix =
  [{ value: "@gmail.com" },
  { value: "@yahoo.com" },
  { value: "@hotmail.com" },
  { value: "@icloud.com" },
  { value: "@aol.com" },
  { value: "@outlook.com" },
  ]




// export const emailComplement = (queryString, callback) => {
//   if (queryString === "") {
//     callback([]);
//   } else if (!/@/.test(queryString)) {
//     const results = new Array();
//     emailSuffix().forEach((element) => {
//       results.push({ value: queryString + element.value });
//     });
//     callback(results);
//   } else {
//     callback([]);
//   }
// }
