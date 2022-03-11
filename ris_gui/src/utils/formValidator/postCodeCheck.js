const postCodeCheck = (rule, value, callback) => {
    let PostCodeFormat =
      /^[1-9][0-9][0-9][0-9]$/i;
    if (!PostCodeFormat.test(value)) {
      callback(new Error("Invalid Postcode Format format."));
    } else {
      callback();
    }
  };

export default postCodeCheck