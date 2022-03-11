const usernameFormatCheck = (rule, value, callback) => {
    if(!/^[A-Za-z]/.test(value)){
        callback(new Error("Username should be starting with a letter."));
    } else if (!/^\w+$/.test(value)){
        callback(new Error("Only letter, digit and underline are permitted."));
    } else {
        callback();
    }
}

export default usernameFormatCheck;