const telFormatCheck = (rule, value, callback) => {
    let telRegex = 
      /^(04)[0-9]{8}$/i;
    if (!telRegex.test(value)) {
      callback(new Error("Invalid Telephone format."));
    } else {
      callback();
    }
  };

export default telFormatCheck