const dateSequenceCheck = (value1, value2, callback) => {
    let date1 = new Date(Date.parse(value1))
    let date2 = new Date(Date.parse(value2))
    if (date1 > date2){
        callback(new Error("Invalid Rental End Date."))
    }
};

export default dateSequenceCheck