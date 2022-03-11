function DateFormat(date,format,delimiter){
    var formatLowerCase=format.toLowerCase();
    var formatItems=formatLowerCase.split(delimiter);
    var dateItems=date.split(delimiter);
    var monthIndex=formatItems.indexOf("mm");
    var dayIndex=formatItems.indexOf("dd");
    var yearIndex=formatItems.indexOf("yyyy");
    var month=parseInt(dateItems[monthIndex]);
    month-=1;
    var formatedDate = new Date(dateItems[yearIndex],month,dateItems[dayIndex]);
    return formatedDate;
}

export default DateFormat;